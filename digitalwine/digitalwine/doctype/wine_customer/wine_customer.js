// Copyright (c) 2022, Aurélien Cibrario and contributors
// For license information, please see license.txt

frappe.ui.form.on('Wine Customer', {

  refresh : function(frm) {

    frappe.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Customer'}

    if(!frm.doc.__islocal) {

      /////////////////////
      // Addresse à la ERPNEXT
      /////////////////////
      // Following python code required first :
      // from frappe.contacts.address_and_contact import load_address_and_contact
      // class Customer(Document):
      //     def onload(self):
      //         load_address_and_contact(self, key=None)
      //
      // Then, this can work :
      frappe.contacts.render_address_and_contact(frm);
      // It actually grab the field named 'address_html', below the relevant code :
      // render_address_and_contact: function(frm) {
      //   if (frm.fields_dict["address_html"] && "addr_list" in frm.doc.__onload) {
      //     $(frm.fields_dict["address_html"].wrapper).html(
      //       frappe.render_template(
      //         "address_list",
      //         frm.doc.__onload
      //       )
      //     ).find(".btn-address").on("click", function() {
      //       frappe.new_doc("Address");
      //     });
      //   }
      // }
    }
  }
});
