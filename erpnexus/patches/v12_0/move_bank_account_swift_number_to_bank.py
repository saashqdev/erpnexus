import saashq


def execute():
	saashq.reload_doc("accounts", "doctype", "bank", force=1)

	if (
		saashq.db.table_exists("Bank")
		and saashq.db.table_exists("Bank Account")
		and saashq.db.has_column("Bank Account", "swift_number")
	):
		try:
			saashq.db.sql(
				"""
				UPDATE `tabBank` b, `tabBank Account` ba
				SET b.swift_number = ba.swift_number WHERE b.name = ba.bank
			"""
			)
		except Exception:
			saashq.log_error("Bank to Bank Account patch migration failed")

	saashq.reload_doc("accounts", "doctype", "bank_account")
	saashq.reload_doc("accounts", "doctype", "payment_request")
