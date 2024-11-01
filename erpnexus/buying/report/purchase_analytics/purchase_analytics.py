# Copyright (c) 2013, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from erpnexus.selling.report.sales_analytics.sales_analytics import Analytics


def execute(filters=None):
	return Analytics(filters).run()
