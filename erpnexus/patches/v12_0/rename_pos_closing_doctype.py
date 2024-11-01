# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	if saashq.db.table_exists("POS Closing Voucher"):
		if not saashq.db.exists("DocType", "POS Closing Entry"):
			saashq.rename_doc("DocType", "POS Closing Voucher", "POS Closing Entry", force=True)

		if not saashq.db.exists("DocType", "POS Closing Entry Taxes"):
			saashq.rename_doc("DocType", "POS Closing Voucher Taxes", "POS Closing Entry Taxes", force=True)

		if not saashq.db.exists("DocType", "POS Closing Voucher Details"):
			saashq.rename_doc(
				"DocType", "POS Closing Voucher Details", "POS Closing Entry Detail", force=True
			)

		saashq.reload_doc("Accounts", "doctype", "POS Closing Entry")
		saashq.reload_doc("Accounts", "doctype", "POS Closing Entry Taxes")
		saashq.reload_doc("Accounts", "doctype", "POS Closing Entry Detail")

	if saashq.db.exists("DocType", "POS Closing Voucher"):
		saashq.delete_doc("DocType", "POS Closing Voucher")
		saashq.delete_doc("DocType", "POS Closing Voucher Taxes")
		saashq.delete_doc("DocType", "POS Closing Voucher Details")
		saashq.delete_doc("DocType", "POS Closing Voucher Invoices")
