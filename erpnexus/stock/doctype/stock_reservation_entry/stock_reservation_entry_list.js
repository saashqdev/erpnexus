// Copyright (c) 2023, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.listview_settings["Stock Reservation Entry"] = {
	get_indicator: function (doc) {
		const status_colors = {
			Draft: "red",
			"Partially Reserved": "orange",
			Reserved: "blue",
			"Partially Delivered": "purple",
			Delivered: "green",
			Cancelled: "red",
		};

		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	},
};
