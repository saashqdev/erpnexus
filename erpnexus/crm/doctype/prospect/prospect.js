// Copyright (c) 2021, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.ui.form.on("Prospect", {
	refresh(frm) {
		if (!frm.is_new() && saashq.boot.user.can_create.includes("Customer")) {
			frm.add_custom_button(
				__("Customer"),
				function () {
					saashq.model.open_mapped_doc({
						method: "erpnexus.crm.doctype.prospect.prospect.make_customer",
						frm: frm,
					});
				},
				__("Create")
			);
		}
		if (!frm.is_new() && saashq.boot.user.can_create.includes("Opportunity")) {
			frm.add_custom_button(
				__("Opportunity"),
				function () {
					saashq.model.open_mapped_doc({
						method: "erpnexus.crm.doctype.prospect.prospect.make_opportunity",
						frm: frm,
					});
				},
				__("Create")
			);
		}

		if (!frm.is_new()) {
			saashq.contacts.render_address_and_contact(frm);
		} else {
			saashq.contacts.clear_address_and_contact(frm);
		}
		frm.trigger("show_notes");
		frm.trigger("show_activities");
	},

	show_notes(frm) {
		const crm_notes = new erpnexus.utils.CRMNotes({
			frm: frm,
			notes_wrapper: $(frm.fields_dict.notes_html.wrapper),
		});
		crm_notes.refresh();
	},

	show_activities(frm) {
		const crm_activities = new erpnexus.utils.CRMActivities({
			frm: frm,
			open_activities_wrapper: $(frm.fields_dict.open_activities_html.wrapper),
			all_activities_wrapper: $(frm.fields_dict.all_activities_html.wrapper),
			form_wrapper: $(frm.wrapper),
		});
		crm_activities.refresh();
	},
});
