import saashq


def execute():
	# handle type casting for is_cancelled field
	module_doctypes = (
		("stock", "Stock Ledger Entry"),
		("stock", "Serial No"),
		("accounts", "GL Entry"),
	)

	for module, doctype in module_doctypes:
		if (
			not saashq.db.has_column(doctype, "is_cancelled")
			or saashq.db.get_column_type(doctype, "is_cancelled").lower() == "int(1)"
		):
			continue

		saashq.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_cancelled = 0
				where is_cancelled in ('', 'No') or is_cancelled is NULL"""
		)
		saashq.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_cancelled = 1
				where is_cancelled = 'Yes'"""
		)

		saashq.reload_doc(module, "doctype", saashq.scrub(doctype))
