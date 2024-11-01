import saashq


def execute():
	if "healthcare" in saashq.get_installed_apps():
		return

	saashq.delete_doc("Workspace", "Healthcare", ignore_missing=True, force=True)

	pages = saashq.get_all("Page", {"module": "healthcare"}, pluck="name")
	for page in pages:
		saashq.delete_doc("Page", page, ignore_missing=True, force=True)

	reports = saashq.get_all("Report", {"module": "healthcare", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		saashq.delete_doc("Report", report, ignore_missing=True, force=True)

	print_formats = saashq.get_all("Print Format", {"module": "healthcare", "standard": "Yes"}, pluck="name")
	for print_format in print_formats:
		saashq.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	saashq.reload_doc("website", "doctype", "website_settings")
	forms = saashq.get_all("Web Form", {"module": "healthcare", "is_standard": 1}, pluck="name")
	for form in forms:
		saashq.delete_doc("Web Form", form, ignore_missing=True, force=True)

	dashboards = saashq.get_all("Dashboard", {"module": "healthcare", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		saashq.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	dashboards = saashq.get_all("Dashboard Chart", {"module": "healthcare", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		saashq.delete_doc("Dashboard Chart", dashboard, ignore_missing=True, force=True)

	saashq.reload_doc("desk", "doctype", "number_card")
	cards = saashq.get_all("Number Card", {"module": "healthcare", "is_standard": 1}, pluck="name")
	for card in cards:
		saashq.delete_doc("Number Card", card, ignore_missing=True, force=True)

	titles = ["Lab Test", "Prescription", "Patient Appointment", "Patient"]
	items = saashq.get_all("Portal Menu Item", filters=[["title", "in", titles]], pluck="name")
	for item in items:
		saashq.delete_doc("Portal Menu Item", item, ignore_missing=True, force=True)

	doctypes = saashq.get_all("DocType", {"module": "healthcare", "custom": 0}, pluck="name")
	for doctype in doctypes:
		saashq.delete_doc("DocType", doctype, ignore_missing=True)

	saashq.delete_doc("Module Def", "Healthcare", ignore_missing=True, force=True)

	custom_fields = {
		"Sales Invoice": ["patient", "patient_name", "ref_practitioner"],
		"Sales Invoice Item": ["reference_dt", "reference_dn"],
		"Stock Entry": ["inpatient_medication_entry"],
		"Stock Entry Detail": ["patient", "inpatient_medication_entry_child"],
	}
	for doc, fields in custom_fields.items():
		filters = {"dt": doc, "fieldname": ["in", fields]}
		records = saashq.get_all("Custom Field", filters=filters, pluck="name")
		for record in records:
			saashq.delete_doc("Custom Field", record, ignore_missing=True, force=True)
