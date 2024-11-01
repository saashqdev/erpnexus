# Copyright (c) 2019, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq

from erpnexus.regional.united_arab_emirates.setup import make_custom_fields


def execute():
	company = saashq.get_all("Company", filters={"country": ["in", ["Saudi Arabia", "United Arab Emirates"]]})
	if not company:
		return

	saashq.reload_doc("accounts", "doctype", "pos_invoice")
	saashq.reload_doc("accounts", "doctype", "pos_invoice_item")

	make_custom_fields()