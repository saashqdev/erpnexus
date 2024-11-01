// Copyright (c) 2021, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.ui.form.on("Campaign", {
	refresh: function (frm) {
		erpnexus.toggle_naming_series();

		if (frm.is_new()) {
			frm.toggle_display(
				"naming_series",
				saashq.boot.sysdefaults.campaign_naming_by == "Naming Series"
			);
		} else {
			frm.add_custom_button(
				__("View Leads"),
				function () {
					saashq.route_options = { utm_source: "Campaign", utm_campaign: frm.doc.name };
					saashq.set_route("List", "Lead");
				},
				"fa fa-list",
				true
			);
		}
	},
});
