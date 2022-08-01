# Copyright (c) 2022, Aurélien Cibrario and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

import ast
import time


@frappe.whitelist()
def server_call(*args, **kwargs):
    """
    This is called by an action, i.e.
    a "Server Action" defined in "Actions" of Cuvee Doctype

    kwargs['doc'] is the dict of the current doc, where the action has been called
    kwargs['cmd'] is the Action/Route that has been called. In our case :
        'digitalwine.digitalwine.doctype.cuvee.cuvee.create_product'

    Note that a function like this could be in digitalwine/api.py.
    The action could be called from anywhere, so with theses two kwargs, we do know
    exactly from where the action was called.

    In my case, it seems like it's an action that makes senses only in the context of
    one Cuvee open, so it feel more natural to have the method here. We'll see.

    Note that this is actually very cool. Both flexible and KISS, like it.

    BUT ! kwargs['doc'] is actually a string ! So here I use ast.litteral_eval,
    but it definitly feels super weird. I guess it's not the right way.

    Other note : this actually raise errors in the JS part, I guess I'm supposed to
    return something, but what ... ?
    """
    frappe.msgprint(f"Hello from python")


@frappe.whitelist()
def create_product(bottle_capacity, price, cuvee):
    """
    This is called by the JS button created in cuvee.js

    Frappe uses python signature function to distribute only the required kwargs ...

    Note that a simple stuff like this could probably be done entirely in JS with
    frappe.db...., which is just a shortcut for this kind of stuff
    """

    doc = frappe.new_doc("Product Wine")
    doc.cuvee = cuvee
    doc.price = price
    doc.bottle_capacity = bottle_capacity
    doc.save()

    return doc.name


class Cuvee(Document):
    """ """

    def autoname(self):

        self.name = f"{self.cepage} ({self.millesime})"

    def validate(self):

        ############
        # Operations validation
        ############
        def op_common_validation(op):
            if op.date is None:
                op.date = frappe.utils.today()
            if op.type == "Transfer":
                if not op.other_cuvee:
                    if op.parentfield == "ops_in":
                        frappe.throw(
                            f"Input transfer (line {op.idx}) miss the other cuvee"
                        )
                    else:
                        frappe.throw(
                            f"Output transfer (line {op.idx}) miss the other cuvee"
                        )
                if op.other_cuvee == self.name:
                    frappe.throw(
                        "You cannot transfer to the same cuvee."
                        "This would harldy be a transfer ;-)"
                    )

        ############
        # INPUTS OP
        ############
        in_qty = 0
        for op in self.ops_in:
            in_qty += op.qty

            op_common_validation(op)

        ############
        # OUTPUTS OP
        ############
        out_qty = 0
        for op in self.ops_out:

            if op.type == "Bottling":
                cl = frappe.get_doc("Bottle Capacity", op.bottle_capacity).capacity_cl
                litres = cl * op.bottle_amount / 100
                op.qty = litres

            out_qty += op.qty

            op_common_validation(op)

        ############
        # Other Fields validation
        ############
        self.total_in = in_qty
        self.total_out = out_qty
        self.total = in_qty - out_qty

        if self.total < 0:
            frappe.throw(
                f"This would result in negative liters in the Cuvee {self.name}. "
                "You cannot do this"
            )

        # Sort by date (seems atrociously inefficient, but recommended way on some forum.
        for i, op in enumerate(sorted(self.ops_in, key=lambda op: op.date)):
            op.idx = i + 1
        for i, op in enumerate(sorted(self.ops_out, key=lambda op: op.date)):
            op.idx = i + 1

    def save(self, *args, **kwargs):
        """
        Override save method to act both before and after
        and provide the ability to save related cuvees without the
        validation, otherwise, I end up in a recursion problem
        """

        try:
            update_twin_ops = kwargs.pop("update_twin_ops")
        except KeyError:
            update_twin_ops = True

        if update_twin_ops:
            self.prepare_update_operations()

        super().save(*args, **kwargs)

        if update_twin_ops:
            self.update_operations()

    def prepare_update_operations(self):
        """
        Get infos about the child Cuvee Operation of Doc about to be save.
        Save them for later (after the actual save operation of self)
        """

        previous_ops = set(
            frappe.db.get_list(
                "Cuvee Operation",
                filters={"type": "Transfer", "parent": self.name},
                pluck="name",
            )
        )
        pending_ops = {
            op.name for op in self.ops_in + self.ops_out if op.type == "Transfer"
        }

        self.updated_ops = previous_ops.intersection(pending_ops)

        self.deleted_ops = previous_ops.difference(pending_ops)

        new_ops_list = {
            op
            for op in self.ops_in + self.ops_out
            if op.name is None and op.type == "Transfer"
        }

        self.new_ops = []
        for op in new_ops_list:
            # Define a new twin tracking for a new op
            twin = frappe.new_doc("Cuvee Twin Ops")
            # Save to generate the name
            twin.save()
            # weird, but correct, I use the twin tracking name as transfer_id
            op.transfer_id = twin.name
            self.new_ops.append((op, twin))

    def update_operations(self):

        # First we add the new ones
        for op1, twin in self.new_ops:

            twin.op1 = op1.name
            op2 = frappe.new_doc("Cuvee Operation")

            if op1.parentfield == "ops_in":
                op2_field = "ops_out"
            else:
                op2_field = "ops_in"
            op2.update(
                {
                    "date": op1.date,
                    "qty": op1.qty,
                    "parent": op1.other_cuvee,
                    "other_cuvee": op1.parent,
                    "parenttype": "Cuvee",
                    "parentfield": op2_field,
                    "type": "Transfer",
                    "transfer_id": twin.name,
                }
            )
            # Specifing parent/parenttype/parentfield, we do create a child
            op2.insert()
            # However, we still want to validate and protect again
            # a non refreshed target cuvee view
            frappe.get_doc("Cuvee", op2.parent).save(update_twin_ops=False)
            # And save the twin to keep track
            twin.op2 = op2.name
            twin.save()

        # Now, let's deal with updates
        updated_cuvees = set()
        for op in self.updated_ops:
            op = frappe.get_doc("Cuvee Operation", op)
            twin = frappe.get_doc("Cuvee Twin Ops", op.transfer_id)
            if op.name == twin.op1:
                op2 = twin.op2
            else:
                op2 = twin.op1
            op2 = frappe.get_doc("Cuvee Operation", op2)
            op2.update({"date": op.date, "qty": op.qty})
            op2.save()
            updated_cuvees.add(op2.parent)

        # And at last with deletions
        for op in self.deleted_ops:

            data = frappe.db.sql(
                "SELECT op1,op2 FROM `tabCuvee Twin Ops` WHERE op1=%(op)s OR op2=%(op)s",
                values={"op": op},
                as_dict=1,
            )
            assert len(data) == 1

            try:
                op2 = frappe.get_doc("Cuvee Operation", data[0]["op1"])
            except frappe.exceptions.DoesNotExistError:
                op2 = frappe.get_doc("Cuvee Operation", data[0]["op2"])

            twin = frappe.get_doc("Cuvee Twin Ops", op2.transfer_id)
            updated_cuvees.add(op2.parent)
            op2.delete()
            twin.delete()

        # And mark the updated cuvees to prevent refresh stuff
        for cuvee in updated_cuvees:
            cuvee = frappe.get_doc("Cuvee", cuvee)
            cuvee.save(update_twin_ops=False)

    @frappe.whitelist()
    def test_button(self):

        randoms = []
        count = 0
        while True:
            rand = frappe.utils.random_string(3)
            if rand not in randoms:
                randoms.append(rand)
                count += 1
            else:
                break
        print(f"{randoms=}")
        frappe.throw(f"Found collision after {count} generation")

    # def update_child_table(self, fieldname, df):
    #     """
    #     Taken by reading the source code. Might be better not to use.

    #     Seems that Frappe logic makes childs very integrated, they very own logic
    #     is actually checking for missing keys in child dict to find deleted items.

    #     Seems bad for perfs, but maybe it's just a very simple and effective way
    #     to deal with it. Anyway, kept for reference.
    #     """
    #     print(f"update child table : {fieldname=}, {df=}")
    #     super().update_child_table(fieldname, df)


# doc_attrs = [
#     "__class__",
#     "__delattr__",
#     "__dict__",
#     "__dir__",
#     "__doc__",
#     "__eq__",
#     "__format__",
#     "__ge__",
#     "__getattribute__",
#     "__getstate__",
#     "__gt__",
#     "__hash__",
#     "__init__",
#     "__init_subclass__",
#     "__last_sync_on",
#     "__le__",
#     "__lt__",
#     "__module__",
#     "__ne__",
#     "__new__",
#     "__reduce__",
#     "__reduce_ex__",
#     "__repr__",
#     "__setattr__",
#     "__sizeof__",
#     "__str__",
#     "__subclasshook__",
#     "__weakref__",
#     "_action",
#     "_cancel",
#     "_extract_images_from_text_editor",
#     "_fix_numeric_types",
#     "_get_missing_mandatory_fields",
#     "_init_child",
#     "_meta",
#     "_original_modified",
#     "_sanitize_content",
#     "_save",
#     "_save_passwords",
#     "_set_defaults",
#     "_submit",
#     "_sync_autoname_field",
#     "_validate",
#     "_validate_code_fields",
#     "_validate_constants",
#     "_validate_data_fields",
#     "_validate_length",
#     "_validate_links",
#     "_validate_mandatory",
#     "_validate_non_negative",
#     "_validate_selects",
#     "_validate_update_after_submit",
#     "add_comment",
#     "add_seen",
#     "add_tag",
#     "add_viewed",
#     "append",
#     "apply_fieldlevel_read_permissions",
#     "as_dict",
#     "as_json",
#     "autoname",
#     "cancel",
#     "cast",
#     "cepage",
#     "check_docstatus_transition",
#     "check_if_latest",
#     "check_no_back_links_exist",
#     "check_permission",
#     "clear_cache",
#     "copy_attachments_from_amended_from",
#     "creation",
#     "db_get",
#     "db_insert",
#     "db_set",
#     "db_update",
#     "db_update_all",
#     "delete",
#     "delete_key",
#     "description",
#     "docstatus",
#     "doctype",
#     "dont_update_if_missing",
#     "extend",
#     "flags",
#     "get",
#     "get_all_children",
#     "get_assigned_users",
#     "get_db_value",
#     "get_doc_before_save",
#     "get_field_name_by_key_name",
#     "get_formatted",
#     "get_invalid_links",
#     "get_label_from_fieldname",
#     "get_latest",
#     "get_liked_by",
#     "get_onload",
#     "get_parentfield_of_doctype",
#     "get_password",
#     "get_permissions",
#     "get_permlevel_access",
#     "get_signature",
#     "get_table_field_doctype",
#     "get_tags",
#     "get_title",
#     "get_url",
#     "get_valid_columns",
#     "get_valid_dict",
#     "get_value",
#     "getone",
#     "has_permission",
#     "has_permlevel_access_to",
#     "has_value_changed",
#     "hook",
#     "idx",
#     "ignore_in_setter",
#     "in_format_data",
#     "init_valid_columns",
#     "insert",
#     "is_child_table_same",
#     "is_dummy_password",
#     "is_new",
#     "is_print_hide",
#     "is_whitelisted",
#     "load_doc_before_save",
#     "load_from_db",
#     "lock",
#     "meta",
#     "millesime",
#     "modified",
#     "modified_by",
#     "name",
#     "notify_update",
#     "on_change",
#     "on_test_btn_click",
#     "operations",
#     "ops_in",
#     "ops_out",
#     "origine",
#     "owner",
#     "precision",
#     "queue_action",
#     "raise_no_permission_to",
#     "reload",
#     "remove",
#     "reset_seen",
#     "reset_values_if_no_permlevel_access",
#     "round_floats_in",
#     "run_before_save_methods",
#     "run_method",
#     "run_notifications",
#     "run_post_save_methods",
#     "run_trigger",
#     "save",
#     "save_version",
#     "set",
#     "set_docstatus",
#     "set_fetch_from_value",
#     "set_name_in_children",
#     "set_new_name",
#     "set_onload",
#     "set_parent_in_children",
#     "set_title_field",
#     "set_user_and_timestamp",
#     "show_unique_validation_message",
#     "submit",
#     "test",
#     "throw_length_exceeded_error",
#     "total",
#     "total_in",
#     "total_out",
#     "unlock",
#     "update",
#     "update_child_table",
#     "update_children",
#     "update_if_missing",
#     "update_modified",
#     "update_single",
#     "validate",
#     "validate_from_to_dates",
#     "validate_higher_perm_levels",
#     "validate_set_only_once",
#     "validate_table_has_rows",
#     "validate_update_after_submit",
#     "validate_value",
#     "validate_workflow",
#     "whitelist",
# ]
