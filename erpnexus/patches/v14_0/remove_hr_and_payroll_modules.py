import saashq


def execute():
	if "hrms" in saashq.get_installed_apps():
		return

	saashq.delete_doc("Module Def", "HR", ignore_missing=True, force=True)
	saashq.delete_doc("Module Def", "Payroll", ignore_missing=True, force=True)

	saashq.delete_doc("Workspace", "HR", ignore_missing=True, force=True)
	saashq.delete_doc("Workspace", "Payroll", ignore_missing=True, force=True)

	print_formats = saashq.get_all(
		"Print Format", {"module": ("in", ["HR", "Payroll"]), "standard": "Yes"}, pluck="name"
	)
	for print_format in print_formats:
		saashq.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	reports = saashq.get_all(
		"Report", {"module": ("in", ["HR", "Payroll"]), "is_standard": "Yes"}, pluck="name"
	)
	for report in reports:
		saashq.delete_doc("Report", report, ignore_missing=True, force=True)

	# reports moved from Projects, Accounts, and Regional module to HRMS app
	for report in [
		"Project Profitability",
		"Employee Hours Utilization Based On Timesheet",
		"Unpaid Expense Claim",
		"Professional Tax Deductions",
		"Provident Fund Deductions",
	]:
		saashq.delete_doc("Report", report, ignore_missing=True, force=True)

	doctypes = saashq.get_all("DocType", {"module": ("in", ["HR", "Payroll"]), "custom": 0}, pluck="name")
	for doctype in doctypes:
		saashq.delete_doc("DocType", doctype, ignore_missing=True, force=True)

	saashq.delete_doc("DocType", "Salary Slip Loan", ignore_missing=True, force=True)
	saashq.delete_doc("DocType", "Salary Component Account", ignore_missing=True, force=True)

	notifications = saashq.get_all(
		"Notification", {"module": ("in", ["HR", "Payroll"]), "is_standard": 1}, pluck="name"
	)
	for notifcation in notifications:
		saashq.delete_doc("Notification", notifcation, ignore_missing=True, force=True)

	saashq.delete_doc("User Type", "Employee Self Service", ignore_missing=True, force=True)

	for dt in ["Web Form", "Dashboard", "Dashboard Chart", "Number Card"]:
		records = saashq.get_all(dt, {"module": ("in", ["HR", "Payroll"]), "is_standard": 1}, pluck="name")
		for record in records:
			saashq.delete_doc(dt, record, ignore_missing=True, force=True)

	custom_fields = {
		"Salary Component": ["component_type"],
		"Employee": ["ifsc_code", "pan_number", "micr_code", "provident_fund_account"],
		"Company": [
			"hra_section",
			"basic_component",
			"hra_component",
			"hra_column_break",
			"arrear_component",
		],
		"Employee Tax Exemption Declaration": [
			"hra_section",
			"monthly_house_rent",
			"rented_in_metro_city",
			"salary_structure_hra",
			"hra_column_break",
			"annual_hra_exemption",
			"monthly_hra_exemption",
		],
		"Employee Tax Exemption Proof Submission": [
			"hra_section",
			"house_rent_payment_amount",
			"rented_in_metro_city",
			"rented_from_date",
			"rented_to_date",
			"hra_column_break",
			"monthly_house_rent",
			"monthly_hra_exemption",
			"total_eligible_hra_exemption",
		],
	}

	for doc, fields in custom_fields.items():
		filters = {"dt": doc, "fieldname": ["in", fields]}
		records = saashq.get_all("Custom Field", filters=filters, pluck="name")
		for record in records:
			saashq.delete_doc("Custom Field", record, ignore_missing=True, force=True)
