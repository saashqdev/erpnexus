// Copyright (c) 2018, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.ui.form.on("Item Alternative", {
	setup: function (frm) {
		frm.fields_dict.item_code.get_query = () => {
			return {
				filters: {
					allow_alternative_item: 1,
				},
			};
		};
	},
});
