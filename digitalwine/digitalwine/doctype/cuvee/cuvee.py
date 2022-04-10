# Copyright (c) 2022, Aurélien Cibrario and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Cuvee(Document):
    """ """

    def autoname(self):

        self.name = f"{self.cepage} ({self.millesime})"

    # def validate(self):

    #     in_qty = 0
    #     for line_no, operation in enumerate(self.ops_in):
    #         in_qty += operation.qty

    #         if operation.type == "Transfer":
    #             # frappe.throw(f"You cannot
    #             if operation.cuvee_from is None:
    #                 frappe.throw(f"Input in line {line_no+1} needs a source")

    #     out_qty = 0
    #     for line_no, operation in enumerate(self.ops_out):
    #         out_qty += operation.qty

    #         if operation.type == "Transfer":
    #             if operation.cuvee_to is None:
    #                 frappe.throw(f"Output in line {line_no+1} needs a destination")

    #     self.total_in = in_qty
    #     self.total_out = out_qty
    #     self.total = in_qty - out_qty

    #     if self.total < 0:
    #         frappe.throw(
    #             f"This would result in negative liters in the Cuvee. You cannot do this"
    #         )

    def before_save(self):

        pass
        # row = self.append(
        #     "ops_out",
        #     {
        #         "date": frappe.utils.today(),
        #         "type": "Transfer",
        #         "qty": 500,
        #         "cuvee_to": self.name,
        #     },
        # )
        # self.save()

        # TRANSFER INPUT FOR SELF
        # for op_in in self.ops_in:

        #     if op_in.type == "Transfer":
        #         # This is a new line because transfer_id is hidden
        #         # and filled here below
        #         if op_in.transfer_id is None:
        #             op_in.transfer_id = frappe.utils.now()

        #             cuvee_from = frappe.get_doc("Cuvee", op_in.cuvee_from)

        #             row = cuvee_src.append(
        #                 "ops_out",
        #                 {
        #                     "date": op_in.date,
        #                     "type": "Transfer",
        #                     "qty": op_in.qty,
        #                     "cuvee_to": self.name,
        #                     "transfer_id": op_in.transfer_id,
        #                 },
        #             )
        #             breakpoint()
        #             # row.save()
        #             # cuvee_src.save()
        #         else:
        #             # This is an update because transfer_id is already filled
        #             pass
        #         # frappe.db.get_list()

    @frappe.whitelist()
    def change_some_value_in_doc(self):

        row = self.append(
            "ops_in",
            {
                "date": frappe.utils.today(),
                "type": "Transfer",
                "qty": 500,
                "cuvee_from": self.name,
            },
        )
        # breakpoint()
        # self.modified = frappe.utils.now()
        # self.notify_update()
        # return {"test": "machin"}
        self.save()
        self.notify_update()

    def update_child_table(self, fieldname, df):

        print(f"update child table : {fieldname=}, {df=}")
        super().update_child_table(fieldname, df)


doc_attrs = [
    "__class__",
    "__delattr__",
    "__dict__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__getstate__",
    "__gt__",
    "__hash__",
    "__init__",
    "__init_subclass__",
    "__last_sync_on",
    "__le__",
    "__lt__",
    "__module__",
    "__ne__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__setattr__",
    "__sizeof__",
    "__str__",
    "__subclasshook__",
    "__weakref__",
    "_action",
    "_cancel",
    "_extract_images_from_text_editor",
    "_fix_numeric_types",
    "_get_missing_mandatory_fields",
    "_init_child",
    "_meta",
    "_original_modified",
    "_sanitize_content",
    "_save",
    "_save_passwords",
    "_set_defaults",
    "_submit",
    "_sync_autoname_field",
    "_validate",
    "_validate_code_fields",
    "_validate_constants",
    "_validate_data_fields",
    "_validate_length",
    "_validate_links",
    "_validate_mandatory",
    "_validate_non_negative",
    "_validate_selects",
    "_validate_update_after_submit",
    "add_comment",
    "add_seen",
    "add_tag",
    "add_viewed",
    "append",
    "apply_fieldlevel_read_permissions",
    "as_dict",
    "as_json",
    "autoname",
    "cancel",
    "cast",
    "cepage",
    "check_docstatus_transition",
    "check_if_latest",
    "check_no_back_links_exist",
    "check_permission",
    "clear_cache",
    "copy_attachments_from_amended_from",
    "creation",
    "db_get",
    "db_insert",
    "db_set",
    "db_update",
    "db_update_all",
    "delete",
    "delete_key",
    "description",
    "docstatus",
    "doctype",
    "dont_update_if_missing",
    "extend",
    "flags",
    "get",
    "get_all_children",
    "get_assigned_users",
    "get_db_value",
    "get_doc_before_save",
    "get_field_name_by_key_name",
    "get_formatted",
    "get_invalid_links",
    "get_label_from_fieldname",
    "get_latest",
    "get_liked_by",
    "get_onload",
    "get_parentfield_of_doctype",
    "get_password",
    "get_permissions",
    "get_permlevel_access",
    "get_signature",
    "get_table_field_doctype",
    "get_tags",
    "get_title",
    "get_url",
    "get_valid_columns",
    "get_valid_dict",
    "get_value",
    "getone",
    "has_permission",
    "has_permlevel_access_to",
    "has_value_changed",
    "hook",
    "idx",
    "ignore_in_setter",
    "in_format_data",
    "init_valid_columns",
    "insert",
    "is_child_table_same",
    "is_dummy_password",
    "is_new",
    "is_print_hide",
    "is_whitelisted",
    "load_doc_before_save",
    "load_from_db",
    "lock",
    "meta",
    "millesime",
    "modified",
    "modified_by",
    "name",
    "notify_update",
    "on_change",
    "on_test_btn_click",
    "operations",
    "ops_in",
    "ops_out",
    "origine",
    "owner",
    "precision",
    "queue_action",
    "raise_no_permission_to",
    "reload",
    "remove",
    "reset_seen",
    "reset_values_if_no_permlevel_access",
    "round_floats_in",
    "run_before_save_methods",
    "run_method",
    "run_notifications",
    "run_post_save_methods",
    "run_trigger",
    "save",
    "save_version",
    "set",
    "set_docstatus",
    "set_fetch_from_value",
    "set_name_in_children",
    "set_new_name",
    "set_onload",
    "set_parent_in_children",
    "set_title_field",
    "set_user_and_timestamp",
    "show_unique_validation_message",
    "submit",
    "test",
    "throw_length_exceeded_error",
    "total",
    "total_in",
    "total_out",
    "unlock",
    "update",
    "update_child_table",
    "update_children",
    "update_if_missing",
    "update_modified",
    "update_single",
    "validate",
    "validate_from_to_dates",
    "validate_higher_perm_levels",
    "validate_set_only_once",
    "validate_table_has_rows",
    "validate_update_after_submit",
    "validate_value",
    "validate_workflow",
    "whitelist",
]
