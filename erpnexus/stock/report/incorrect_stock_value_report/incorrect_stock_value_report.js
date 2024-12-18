// Copyright (c) 2016, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.query_reports["Incorrect Stock Value Report"] = {
	filters: [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: saashq.defaults.get_user_default("Company"),
		},
		{
			label: __("Account"),
			fieldname: "account",
			fieldtype: "Link",
			options: "Account",
			get_query: function () {
				var company = saashq.query_report.get_filter_value("company");
				return {
					filters: {
						account_type: "Stock",
						company: company,
					},
				};
			},
		},
		{
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
		},
	],
};
