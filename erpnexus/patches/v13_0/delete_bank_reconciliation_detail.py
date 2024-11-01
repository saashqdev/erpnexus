# Copyright (c) 2019, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	if saashq.db.exists("DocType", "Bank Reconciliation Detail") and saashq.db.exists(
		"DocType", "Bank Clearance Detail"
	):
		saashq.delete_doc("DocType", "Bank Reconciliation Detail", force=1)
