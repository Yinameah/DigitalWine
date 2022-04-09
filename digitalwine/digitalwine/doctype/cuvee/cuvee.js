// Copyright (c) 2022, Aurélien Cibrario and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cuvee', {
   //refresh: function(frm) {
   //}
  setup : function(frm) {

    // Not sure of the scope of this variable, but it works 
    // in filter below
    //let selected_cepage = 'Merlot';

    frm.set_query('cuvee_dest', 'operations', () => {
        return {
            filters: [
              // But this is not the same as OR !! Cannot do this
              //['Cuvee', 'cepage', '!=','Arvine'],
              //['Cuvee', 'millesime', '!=', '2021']
              
              // in simple '=' version, can use the simpler version 
              // field : 'value' in a dict
              // {
              //cepage: selected_cepage,
              //millesime: '2021'
              // }
            ]
        }
    })
  }
});


frappe.ui.form.on('Cuvee Operation', { 

    operations_add(frm, cdt, cdn) { // "links" is the name of the table field in ToDo, "_add" is the event
        // frm: current ToDo form
        // cdt: child DocType 'Dynamic Link'
        // cdn: child docname (something like 'a6dfk76')
        // cdt and cdn are useful for identifying which row triggered this event
        //frappe.msgprint('You added a Cuvee operation ! 🎉 ');
    },

    form_render(frm,cdt,cdn){
        // this gets the row itself, not sure what we can do with this
        let row = frappe.get_doc(cdt, cdn);

    }

});

