# Copyright (c) 2018, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	if saashq.db.table_exists("Bank Reconciliation"):
		saashq.rename_doc("DocType", "Bank Reconciliation", "Bank Clearance", force=True)
		saashq.reload_doc("Accounts", "doctype", "Bank Clearance")

		saashq.rename_doc("DocType", "Bank Reconciliation Detail", "Bank Clearance Detail", force=True)
		saashq.reload_doc("Accounts", "doctype", "Bank Clearance Detail")
