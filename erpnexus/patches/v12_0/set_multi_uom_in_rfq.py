# Copyright (c) 2017, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	saashq.reload_doc("buying", "doctype", "request_for_quotation_item")

	saashq.db.sql(
		"""UPDATE `tabRequest for Quotation Item`
			SET
				stock_uom = uom,
				conversion_factor = 1,
				stock_qty = qty"""
	)
