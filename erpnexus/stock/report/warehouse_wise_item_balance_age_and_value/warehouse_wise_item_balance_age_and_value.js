// Copyright (c) 2016, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.query_reports["Warehouse wise Item Balance Age and Value"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			width: "80",
			options: "Company",
			reqd: 1,
			default: saashq.defaults.get_user_default("Company"),
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			width: "80",
			reqd: 1,
			default: saashq.datetime.add_months(saashq.datetime.get_today(), -1),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			width: "80",
			reqd: 1,
			default: saashq.datetime.get_today(),
		},
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			width: "80",
			options: "Item Group",
		},
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "Link",
			width: "80",
			options: "Item",
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			width: "80",
			options: "Warehouse",
			get_query: function () {
				const company = saashq.query_report.get_filter_value("company");
				return {
					filters: { company: company },
				};
			},
		},
		{
			fieldname: "filter_total_zero_qty",
			label: __("Filter Total Zero Qty"),
			fieldtype: "Check",
			default: 1,
		},
	],
};
