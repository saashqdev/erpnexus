// Copyright (c) 2016, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.query_reports["Gross and Net Profit Report"] = $.extend({}, erpnexus.financial_statements);

saashq.query_reports["Gross and Net Profit Report"]["filters"].push({
	fieldname: "accumulated_values",
	label: __("Accumulated Values"),
	fieldtype: "Check",
});
