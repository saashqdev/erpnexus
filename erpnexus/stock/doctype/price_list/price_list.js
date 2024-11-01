// Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

saashq.ui.form.on("Price List", {
	refresh: function (frm) {
		let me = this;
		frm.add_custom_button(
			__("Add / Edit Prices"),
			function () {
				saashq.route_options = {
					price_list: frm.doc.name,
				};
				saashq.set_route("Report", "Item Price");
			},
			"fa fa-money"
		);
	},
});
