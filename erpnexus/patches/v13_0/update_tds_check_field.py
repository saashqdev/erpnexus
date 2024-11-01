import saashq


def execute():
	if saashq.db.has_table("Tax Withholding Category") and saashq.db.has_column(
		"Tax Withholding Category", "round_off_tax_amount"
	):
		saashq.db.sql(
			"""
			UPDATE `tabTax Withholding Category` set round_off_tax_amount = 0
			WHERE round_off_tax_amount IS NULL
		"""
		)
