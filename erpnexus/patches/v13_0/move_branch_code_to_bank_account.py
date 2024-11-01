# Copyright (c) 2019, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	saashq.reload_doc("accounts", "doctype", "bank_account")
	saashq.reload_doc("accounts", "doctype", "bank")

	if saashq.db.has_column("Bank", "branch_code") and saashq.db.has_column("Bank Account", "branch_code"):
		saashq.db.sql(
			"""UPDATE `tabBank` b, `tabBank Account` ba
			SET ba.branch_code = b.branch_code
			WHERE ba.bank = b.name AND
			ifnull(b.branch_code, '') != '' AND ifnull(ba.branch_code, '') = ''"""
		)
