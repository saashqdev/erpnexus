import saashq


def execute():
	company = saashq.get_all("Company", filters={"country": "India"})
	if not company:
		return

	saashq.reload_doc("regional", "doctype", "lower_deduction_certificate")

	ldc = saashq.qb.DocType("Lower Deduction Certificate").as_("ldc")
	supplier = saashq.qb.DocType("Supplier")

	saashq.qb.update(ldc).inner_join(supplier).on(ldc.supplier == supplier.name).set(
		ldc.tax_withholding_category, supplier.tax_withholding_category
	).where(ldc.tax_withholding_category.isnull()).run()
