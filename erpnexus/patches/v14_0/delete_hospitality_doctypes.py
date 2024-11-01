import saashq


def execute():
	modules = ["Hotels", "Restaurant"]

	for module in modules:
		saashq.delete_doc("Module Def", module, ignore_missing=True, force=True)

		saashq.delete_doc("Workspace", module, ignore_missing=True, force=True)

		reports = saashq.get_all("Report", {"module": module, "is_standard": "Yes"}, pluck="name")
		for report in reports:
			saashq.delete_doc("Report", report, ignore_missing=True, force=True)

		dashboards = saashq.get_all("Dashboard", {"module": module, "is_standard": 1}, pluck="name")
		for dashboard in dashboards:
			saashq.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

		doctypes = saashq.get_all("DocType", {"module": module, "custom": 0}, pluck="name")
		for doctype in doctypes:
			saashq.delete_doc("DocType", doctype, ignore_missing=True)

	custom_fields = [
		{"dt": "Sales Invoice", "fieldname": "restaurant"},
		{"dt": "Sales Invoice", "fieldname": "restaurant_table"},
		{"dt": "Price List", "fieldname": "restaurant_menu"},
	]

	for field in custom_fields:
		custom_field = saashq.db.get_value("Custom Field", field)
		saashq.delete_doc("Custom Field", custom_field, ignore_missing=True)
