// Copyright (c) 2016, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.query_reports["COGS By Item Group"] = {
	filters: [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			mandatory: true,
			default: saashq.defaults.get_user_default("Company"),
		},
		{
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			mandatory: true,
			default: saashq.datetime.year_start(),
		},
		{
			label: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Date",
			mandatory: true,
			default: saashq.datetime.get_today(),
		},
	],
};
