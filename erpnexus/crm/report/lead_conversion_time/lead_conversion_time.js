// Copyright (c) 2018, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.query_reports["Lead Conversion Time"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
			default: saashq.datetime.add_days(saashq.datetime.nowdate(), -30),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
			default: saashq.datetime.nowdate(),
		},
	],
};
