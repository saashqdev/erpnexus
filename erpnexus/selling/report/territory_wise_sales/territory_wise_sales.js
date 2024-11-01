// Copyright (c) 2016, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.query_reports["Territory-wise Sales"] = {
	breadcrumb: "Selling",
	filters: [
		{
			fieldname: "transaction_date",
			label: __("Transaction Date"),
			fieldtype: "DateRange",
			default: [
				saashq.datetime.add_months(saashq.datetime.get_today(), -1),
				saashq.datetime.get_today(),
			],
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
		},
	],
};
