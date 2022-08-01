// Copyright (c) 2022, Aurélien Cibrario and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cuvee", {
  //refresh: function(frm) {
  //}
  setup(frm) {
    frm.set_query("other_cuvee", "ops_in", function (frm) {
      return {
        filters: [
          ["Cuvee", "name", "!=", frm.name],
          // in simple '=' version, can use the simpler version
          // field : 'value' in a dict
          // {
          //cepage: selected_cepage,
          //millesime: '2021'
          // }
        ],
      };
    });
  },

  refresh(frm) {
    // Add custom button that launch a prompt
    let current_cuvee = frm.docname;
    frm.add_custom_button("Create Product", () => {
      frappe.prompt(
        [
          {
            label: "Bottle",
            fieldname: "bottle_capacity",
            fieldtype: "Link",
            options: "Bottle Capacity",
            reqd: 1,
          },
          {
            label: "Price",
            fieldname: "price",
            fieldtype: "Float",
          },
        ],
        function (args) {
          args["cuvee"] = current_cuvee;
          frappe
            .call({
              method:
                "digitalwine.digitalwine.doctype.cuvee.cuvee.create_product",
              args: args,
              freeze: true,
            })
            .then((r) => {
              // This is not called in case of server error
              // Here, r.message is what the python function returns
              console.log(r);
              frappe.show_alert(
                "Created product in " +
                  args["bottle_capacity"] +
                  " for " +
                  current_cuvee
              );
              frappe.set_route("product-wine", r.message);
            });
        },
        "Create new product for " + frm.docname,
        "Create"
      );
    });
  },
  //primary_action(values) {
  //  console.log(values);
  //  d.hide();
  //  frappe.call('digitalwine.digitalwine.doctype.cuvee.cuvee.create_product',values);
  //}
  //})
  //d.show();
  //})
  //},
});

// Events in the child tables
// See https://frappeframework.com/docs/v13/user/en/api/form#child-table-events
frappe.ui.form.on("Cuvee Operation", {
  // When the row is OPENED as a form
  form_render(frm, cdt, cdn) {
    // NOTE : cdt = current document type, cdn = current document name

    // Could get the operation document like this.
    // Still confused when the child or the parent is in
    // charge of the data. But below, for setting "Transfer" as
    // default value, this approach seems to work ....
    let row = frappe.get_doc(cdt, cdn);
  },

  // NOTE : This is {fieldname}_add, and is trigger, well, when adding a row
  ops_in_add(frm, cdt, cdn) {
    // NOTE : cdt & cdn refer to the row itself
    frm.set_df_property(
      "ops_in",
      "options",
      ["Harvest", "Transfer", "Buy"],
      frm.doc.name,
      "type",
      cdn
    );
  },
  ops_out_add(frm, cdt, cdn) {
    frm.set_df_property(
      "ops_out",
      "options",
      ["Transfer", "Sell", "Bottling", "Loss"],
      frm.doc.name,
      "type",
      cdn
    );

    // Now set default to transfer, as Harvest is not ok for ops_out
    let row = frappe.get_doc(cdt, cdn);
    row.type = "Transfer";
    frm.refresh_field("ops_out");
  },
});
