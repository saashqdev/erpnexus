# Copyright (c) 2019, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	"""`sales_invoice` field from loyalty point entry is splitted into `invoice_type` & `invoice` fields"""

	saashq.reload_doc("Accounts", "doctype", "loyalty_point_entry")

	if not saashq.db.has_column("Loyalty Point Entry", "sales_invoice"):
		return

	saashq.db.sql(
		"""UPDATE `tabLoyalty Point Entry` lpe
		SET lpe.`invoice_type` = 'Sales Invoice', lpe.`invoice` = lpe.`sales_invoice`
		WHERE lpe.`sales_invoice` IS NOT NULL
		AND (lpe.`invoice` IS NULL OR lpe.`invoice` = '')"""
	)
