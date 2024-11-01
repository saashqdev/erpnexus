import saashq


def execute():
	saashq.reload_doc("buying", "doctype", "supplier_quotation")
	saashq.db.sql(
		"""UPDATE `tabSupplier Quotation`
		SET valid_till = DATE_ADD(transaction_date , INTERVAL 1 MONTH)
		WHERE docstatus < 2"""
	)
