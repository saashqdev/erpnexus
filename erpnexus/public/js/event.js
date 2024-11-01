// Copyright (c) 2018, Saashq Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt
saashq.provide("saashq.desk");

saashq.ui.form.on("Event", {
	refresh: function (frm) {
		frm.set_query("reference_doctype", "event_participants", function () {
			return {
				filters: {
					name: ["in", ["Contact", "Lead", "Customer", "Supplier", "Employee", "Sales Partner"]],
				},
			};
		});

		frm.add_custom_button(
			__("Add Leads"),
			function () {
				new saashq.desk.eventParticipants(frm, "Lead");
			},
			__("Add Participants")
		);

		frm.add_custom_button(
			__("Add Customers"),
			function () {
				new saashq.desk.eventParticipants(frm, "Customer");
			},
			__("Add Participants")
		);

		frm.add_custom_button(
			__("Add Suppliers"),
			function () {
				new saashq.desk.eventParticipants(frm, "Supplier");
			},
			__("Add Participants")
		);

		frm.add_custom_button(
			__("Add Employees"),
			function () {
				new saashq.desk.eventParticipants(frm, "Employee");
			},
			__("Add Participants")
		);

		frm.add_custom_button(
			__("Add Sales Partners"),
			function () {
				new saashq.desk.eventParticipants(frm, "Sales Partners");
			},
			__("Add Participants")
		);
	},
});
