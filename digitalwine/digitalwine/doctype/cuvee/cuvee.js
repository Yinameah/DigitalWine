// Copyright (c) 2022, Aurélien Cibrario and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cuvee', {
   //refresh: function(frm) {
   //}
	setup : function(frm) {

		frm.set_query('other_cuvee', 'ops_in', function(frm) {
			debugger
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
