import saashq


def execute():
	saashq.delete_doc("Module Def", "Non Profit", ignore_missing=True, force=True)

	saashq.delete_doc("Workspace", "Non Profit", ignore_missing=True, force=True)

	print_formats = saashq.get_all("Print Format", {"module": "Non Profit", "standard": "Yes"}, pluck="name")
	for print_format in print_formats:
		saashq.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	print_formats = ["80G Certificate for Membership", "80G Certificate for Donation"]
	for print_format in print_formats:
		saashq.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	reports = saashq.get_all("Report", {"module": "Non Profit", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		saashq.delete_doc("Report", report, ignore_missing=True, force=True)

	dashboards = saashq.get_all("Dashboard", {"module": "Non Profit", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		saashq.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	doctypes = saashq.get_all("DocType", {"module": "Non Profit", "custom": 0}, pluck="name")
	for doctype in doctypes:
		saashq.delete_doc("DocType", doctype, ignore_missing=True)

	doctypes = ["Tax Exemption 80G Certificate", "Tax Exemption 80G Certificate Detail"]
	for doctype in doctypes:
		saashq.delete_doc("DocType", doctype, ignore_missing=True)

	forms = ["grant-application", "certification-application", "certification-application-usd"]
	for form in forms:
		saashq.delete_doc("Web Form", form, ignore_missing=True, force=True)

	custom_records = [
		{"doctype": "Party Type", "name": "Member"},
		{"doctype": "Party Type", "name": "Donor"},
	]
	for record in custom_records:
		try:
			saashq.delete_doc(record["doctype"], record["name"], ignore_missing=True)
		except saashq.LinkExistsError:
			pass

	custom_fields = {
		"Member": ["pan_number"],
		"Donor": ["pan_number"],
		"Company": [
			"non_profit_section",
			"company_80g_number",
			"with_effect_from",
			"non_profit_column_break",
			"pan_details",
		],
	}

	for doc, fields in custom_fields.items():
		filters = {"dt": doc, "fieldname": ["in", fields]}
		records = saashq.get_all("Custom Field", filters=filters, pluck="name")
		for record in records:
			saashq.delete_doc("Custom Field", record, ignore_missing=True, force=True)
