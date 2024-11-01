// Copyright (c) 2023, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
saashq.ui.form.on("Asset Shift Allocation", {
	onload: function (frm) {
		frm.events.make_schedules_editable(frm);
	},

	make_schedules_editable: function (frm) {
		frm.toggle_enable("depreciation_schedule", true);
		frm.fields_dict["depreciation_schedule"].grid.toggle_enable("schedule_date", false);
		frm.fields_dict["depreciation_schedule"].grid.toggle_enable("depreciation_amount", false);
		frm.fields_dict["depreciation_schedule"].grid.toggle_enable("shift", true);
	},
});
