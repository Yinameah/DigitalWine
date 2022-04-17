// Copyright (c) 2022, Aurélien Cibrario and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cuvee', {
  //refresh: function(frm) {
  //}
  setup : function(frm) {

    frm.set_query('other_cuvee', 'ops_in', function(frm) {
      return {
        filters: [
          ['Cuvee','name','!=',frm.name]
          // in simple '=' version, can use the simpler version 
          // field : 'value' in a dict
          // {
          //cepage: selected_cepage,
          //millesime: '2021'
          // }
        ]
      }
    })
  },

  refresh: function(frm) {
    let current_cuvee = frm.docname;
    frm.add_custom_button('Create Product', () => {
      frappe.prompt(
        [
          {
            label: 'Bottle',
            fieldname: 'bottle_capacity',
            fieldtype: 'Link',
            options: 'Bottle Capacity',
            reqd:1
          },
          {
            label: 'Price',
            fieldname: 'price',
            fieldtype: 'Float',
          },
        ],
        function(args){
          args['cuvee'] = current_cuvee;
          frappe.call({
            method: 'digitalwine.digitalwine.doctype.cuvee.cuvee.create_product',
            args: args,
            freeze: true,
          }).then(r => {
            // This is not called in case of server error
            // Here, r.message is what the python function returns
            console.log(r)
            frappe.show_alert(
              "Created product in "+args['bottle_capacity']+" for "+current_cuvee
            );
            frappe.set_route('product-wine',r.message)
          })
        },
        'Create new product for '+frm.docname,
        'Create'
      )
    })
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


// FOR REFERENCE : UI Operation on former operations field
//frappe.ui.form.on('Cuvee Operation', {

//    operations_add(frm, cdt, cdn) { // "links" is the name of the table field in ToDo, "_add" is the event
//        // frm: current ToDo form
//        // cdt: child DocType 'Dynamic Link'
//        // cdn: child docname (something like 'a6dfk76')
//        // cdt and cdn are useful for identifying which row triggered this event
//        //frappe.msgprint('You added a Cuvee operation ! 🎉 ');
//    },

//    form_render(frm,cdt,cdn){
//        // this gets the row itself, not sure what we can do with this
//        let row = frappe.get_doc(cdt, cdn);

//    }

//});

frappe.ui.form.on('Cuvee Op In', {

	before_ops_in_remove(frm, cdt, cdn){
		let row = frappe.get_doc(cdt, cdn);
		if (row.type === 'Transfer'){
			//frappe.msgprint('Row rewoved !');
			//
		}
	},

});

frappe.ui.form.on('Cuvee Op Out', {

  ops_out_remove(frm, cdt, cdn){
      //frappe.msgprint('Row rewoved !');
  },

});
