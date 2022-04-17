# Copyright (c) 2022, Aurélien Cibrario and Contributors
# See license.txt

import frappe
import unittest


class TestCuvee(unittest.TestCase):
    """
    NOTE
    methods setUp & tearDown are automatically called for each test
    methods setUpClass & tearDownClass are automatically called for the class
    """

    @classmethod
    def setUpClass(cls):

        frappe.set_user("Administrator")

        doc = frappe.get_doc(
            {
                "doctype": "Cuvee",
                "cepage": "Cepage1",
                "millesime": "2020",
            }
        ).insert()
        doc = frappe.get_doc(
            {
                "doctype": "Cuvee",
                "cepage": "Cepage2",
                "millesime": "2050",
            }
        ).insert()

    @classmethod
    def tearDownClass(cls):
        doc = frappe.get_doc("Cuvee", "Cepage1 (2020)")
        doc.update({"ops_in": [], "ops_out": []})
        doc.save()
        doc.delete()

        frappe.delete_doc("Cuvee", "Cepage2 (2050)")

    def test_naming_scheme(self):
        """
        Check that cuvees are named {cepage} ({millesime})
        """

        doc = frappe.get_doc("Cuvee", "Cepage1 (2020)")
        self.assertEqual(doc.cepage, "Cepage1")
        self.assertEqual(doc.millesime, "2020")

        doc = frappe.get_doc("Cuvee", "Cepage2 (2050)")
        self.assertEqual(doc.cepage, "Cepage2")
        self.assertEqual(doc.millesime, "2050")

    def test_out_op_on_empty_fails(self):
        """
        Check that cannot add a transfer out on empty cuvee
        """
        doc = frappe.get_doc("Cuvee", "Cepage1 (2020)")
        other_cuvee = frappe.get_doc("Cuvee", "Cepage2 (2050)")

        row = doc.append(
            "ops_out",
            {
                "date": frappe.utils.today(),
                "type": "Transfer",
                "qty": 500,
                "other_cuvee": other_cuvee.name,
            },
        )
        self.assertRaises(frappe.exceptions.ValidationError, doc.save)

    def test_twin_op_creation_modif_delete(self):
        """
        Create a transfer, check twin is created, and total liter match.
        Modify transfer from both sides, and check that other op is modified
        Delete one op, and check that both ops AND twin_track are deleted
        """

        cuvee_from = frappe.get_doc("Cuvee", "Cepage1 (2020)")
        cuvee_to = frappe.get_doc("Cuvee", "Cepage2 (2050)")

        # Creation
        cuvee_from.append(
            "ops_in",
            {
                "date": frappe.utils.today(),
                "type": "Harvest",
                "qty": 500,
            },
        )
        cuvee_from.save()
        self.assertEqual(cuvee_from.total, 500)

        cuvee_from.append(
            "ops_out",
            {
                "date": frappe.utils.today(),
                "type": "Transfer",
                "qty": 500,
                "other_cuvee": cuvee_to.name,
            },
        )
        cuvee_from.save()
        cuvee_to.reload()

        self.assertEqual(len(cuvee_from.ops_out), 1)
        self.assertEqual(len(cuvee_to.ops_in), 1)
        self.assertEqual(cuvee_to.ops_in[0].other_cuvee, cuvee_from.name)
        self.assertEqual(cuvee_to.ops_in[0].qty, 500)

        self.assertEqual(
            cuvee_to.ops_in[0].transfer_id, cuvee_from.ops_out[0].transfer_id
        )

        twin_track = frappe.get_doc("Cuvee Twin Ops", cuvee_to.ops_in[0].transfer_id)
        self.assertEqual(cuvee_from.ops_out[0].name, twin_track.op1)
        self.assertEqual(cuvee_from.ops_out[0].type, "Transfer")
        self.assertEqual(cuvee_to.ops_in[0].name, twin_track.op2)
        self.assertEqual(cuvee_to.ops_in[0].type, "Transfer")

        self.assertEqual(cuvee_from.total, 0)
        self.assertEqual(cuvee_to.total, 500)

        # Modification
        cuvee_from.ops_out[0].date = frappe.utils.getdate("2000-01-01")
        cuvee_from.ops_out[0].qty = 200

        cuvee_from.save()
        cuvee_to.reload()

        self.assertEqual(cuvee_to.ops_in[0].date, frappe.utils.getdate("2000-01-01"))
        self.assertEqual(cuvee_to.ops_in[0].qty, 200)

        self.assertEqual(cuvee_from.total, 300)
        self.assertEqual(cuvee_to.total, 200)

        # Modif other direction
        cuvee_to.ops_in[0].date = frappe.utils.getdate("2005-05-06")
        cuvee_to.ops_in[0].qty = 150

        cuvee_to.save()
        cuvee_from.reload()

        self.assertEqual(cuvee_from.ops_out[0].date, frappe.utils.getdate("2005-05-06"))
        self.assertEqual(cuvee_from.ops_out[0].qty, 150)

        self.assertEqual(cuvee_from.total, 350)
        self.assertEqual(cuvee_to.total, 150)

        # Delete

        cuvee_from.update({"ops_out": []})
        cuvee_from.save()
        cuvee_to.reload()

        self.assertEqual(len(cuvee_to.ops_in), 0)

        self.assertEqual(cuvee_from.total, 500)
        self.assertEqual(cuvee_to.total, 0)

        self.assertRaises(frappe.exceptions.DoesNotExistError, twin_track.reload)
