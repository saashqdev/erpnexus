// Copyright (c) 2016, Saashq Technologies and contributors
// For license information, please see license.txt

saashq.ui.form.on("Party Type", {
	setup: function (frm) {
		frm.fields_dict["party_type"].get_query = function (frm) {
			return {
				filters: {
					istable: 0,
					is_submittable: 0,
				},
			};
		};
	},
});
