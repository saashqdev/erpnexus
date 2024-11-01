saashq.provide("saashq.dashboards.chart_sources");

saashq.dashboards.chart_sources["Warehouse wise Stock Value"] = {
	method: "erpnexus.stock.dashboard_chart_source.warehouse_wise_stock_value.warehouse_wise_stock_value.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: saashq.defaults.get_user_default("Company"),
		},
	],
};
