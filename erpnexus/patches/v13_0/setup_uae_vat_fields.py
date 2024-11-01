# Copyright (c) 2019, Saashq and Contributors
# License: GNU General Public License v3. See license.txt

import saashq

from erpnexus.regional.united_arab_emirates.setup import setup


def execute():
	company = saashq.get_all("Company", filters={"country": "United Arab Emirates"})
	if not company:
		return

	saashq.reload_doc("regional", "report", "uae_vat_201")
	saashq.reload_doc("regional", "doctype", "uae_vat_settings")
	saashq.reload_doc("regional", "doctype", "uae_vat_account")

	setup()
