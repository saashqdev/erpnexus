import click
import saashq


def execute():
	if "education" in saashq.get_installed_apps():
		return

	saashq.delete_doc("Workspace", "Education", ignore_missing=True, force=True)

	pages = saashq.get_all("Page", {"module": "education"}, pluck="name")
	for page in pages:
		saashq.delete_doc("Page", page, ignore_missing=True, force=True)

	reports = saashq.get_all("Report", {"module": "education", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		saashq.delete_doc("Report", report, ignore_missing=True, force=True)

	print_formats = saashq.get_all("Print Format", {"module": "education", "standard": "Yes"}, pluck="name")
	for print_format in print_formats:
		saashq.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	saashq.reload_doc("website", "doctype", "website_settings")
	forms = saashq.get_all("Web Form", {"module": "education", "is_standard": 1}, pluck="name")
	for form in forms:
		saashq.delete_doc("Web Form", form, ignore_missing=True, force=True)

	dashboards = saashq.get_all("Dashboard", {"module": "education", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		saashq.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	dashboards = saashq.get_all("Dashboard Chart", {"module": "education", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		saashq.delete_doc("Dashboard Chart", dashboard, ignore_missing=True, force=True)

	saashq.reload_doc("desk", "doctype", "number_card")
	cards = saashq.get_all("Number Card", {"module": "education", "is_standard": 1}, pluck="name")
	for card in cards:
		saashq.delete_doc("Number Card", card, ignore_missing=True, force=True)

	doctypes = saashq.get_all("DocType", {"module": "education", "custom": 0}, pluck="name")

	for doctype in doctypes:
		saashq.delete_doc("DocType", doctype, ignore_missing=True)

	titles = [
		"Fees",
		"Student Admission",
		"Grant Application",
		"Chapter",
		"Certification Application",
	]
	items = saashq.get_all("Portal Menu Item", filters=[["title", "in", titles]], pluck="name")
	for item in items:
		saashq.delete_doc("Portal Menu Item", item, ignore_missing=True, force=True)

	saashq.delete_doc("Module Def", "Education", ignore_missing=True, force=True)

	click.secho(
		"Education Module is moved to a separate app"
		"Please install the app to continue using the module: https://github.com/saashqdev/education",
		fg="yellow",
	)
