// Copyright (c) 2016, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.query_reports["BOM Variance Report"] = {
	filters: [
		{
			fieldname: "bom_no",
			label: __("BOM No"),
			fieldtype: "Link",
			options: "BOM",
		},
		{
			fieldname: "work_order",
			label: __("Work Order"),
			fieldtype: "Link",
			options: "Work Order",
			get_query: function () {
				var bom_no = saashq.query_report.get_filter_value("bom_no");
				return {
					query: "erpnexus.manufacturing.report.bom_variance_report.bom_variance_report.get_work_orders",
					filters: {
						bom_no: bom_no,
					},
				};
			},
		},
	],
};
