// Copyright (c) 2016, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
saashq.query_reports["Campaign Efficiency"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: erpnexus.utils.get_fiscal_year(saashq.datetime.get_today(), true)[1],
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: erpnexus.utils.get_fiscal_year(saashq.datetime.get_today(), true)[2],
		},
	],
};
