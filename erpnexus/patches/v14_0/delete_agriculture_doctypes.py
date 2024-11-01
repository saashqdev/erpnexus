import saashq


def execute():
	if "agriculture" in saashq.get_installed_apps():
		return

	saashq.delete_doc("Module Def", "Agriculture", ignore_missing=True, force=True)

	saashq.delete_doc("Workspace", "Agriculture", ignore_missing=True, force=True)

	reports = saashq.get_all("Report", {"module": "agriculture", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		saashq.delete_doc("Report", report, ignore_missing=True, force=True)

	dashboards = saashq.get_all("Dashboard", {"module": "agriculture", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		saashq.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	doctypes = saashq.get_all("DocType", {"module": "agriculture", "custom": 0}, pluck="name")
	for doctype in doctypes:
		saashq.delete_doc("DocType", doctype, ignore_missing=True)

	saashq.delete_doc("Module Def", "Agriculture", ignore_missing=True, force=True)
