# Copyright (c) 2020, Saashq and Contributors
# License: GNU General Public License v3. See license.txt

import saashq

from erpnexus.regional.south_africa.setup import add_permissions, make_custom_fields


def execute():
	company = saashq.get_all("Company", filters={"country": "South Africa"})
	if not company:
		return

	saashq.reload_doc("regional", "doctype", "south_africa_vat_settings")
	saashq.reload_doc("regional", "report", "vat_audit_report")
	saashq.reload_doc("accounts", "doctype", "south_africa_vat_account")

	make_custom_fields()
	add_permissions()
