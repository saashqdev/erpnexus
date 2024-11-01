// Copyright (c) 2016, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.query_reports["Support Hour Distribution"] = {
	filters: [
		{
			lable: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			default: saashq.datetime.nowdate(),
			reqd: 1,
		},
		{
			lable: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Date",
			default: saashq.datetime.nowdate(),
			reqd: 1,
		},
	],
};
