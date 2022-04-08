// Copyright (c) 2022, Aurélien Cibrario and contributors
// For license information, please see license.txt

frappe.ui.form.on('Parcelle', {
	// refresh: function(frm) {

	// }
});

// Seems that's the way to hide the name from list view.
// Doesn't seem to work.
// https://discuss.erpnext.com/t/same-field-in-list-view-3-times-how-to-really-change-the-name-of-name-hide-name-from-list-view/75719
// I will get back to it when I get the JS framework a bit better
frappe.listview_settings['Parcelle'] = {
  hide_name_column: true
  }
