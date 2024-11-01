import saashq


def execute():
	saashq.reload_doctype("Payment Entry")
	saashq.db.sql(
		"""update `tabPayment Entry` set status = CASE
		WHEN docstatus = 1 THEN 'Submitted'
		WHEN docstatus = 2 THEN 'Cancelled'
		ELSE 'Draft'
		END;"""
	)
