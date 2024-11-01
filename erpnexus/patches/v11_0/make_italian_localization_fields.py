# Copyright (c) 2017, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq

from erpnexus.regional.italy import state_codes
from erpnexus.regional.italy.setup import make_custom_fields, setup_report


def execute():
	company = saashq.get_all("Company", filters={"country": "Italy"})
	if not company:
		return

	saashq.reload_doc("regional", "report", "electronic_invoice_register")
	make_custom_fields()
	setup_report()

	# Set state codes
	condition = ""
	for state, code in state_codes.items():
		condition += f" when {saashq.db.escape(state)} then {saashq.db.escape(code)}"

	if condition:
		condition = f"state_code = (case state {condition} end),"

	saashq.db.sql(
		f"""
		UPDATE tabAddress set {condition} country_code = UPPER(ifnull((select code
			from `tabCountry` where name = `tabAddress`.country), ''))
			where country_code is null and state_code is null
	"""
	)

	saashq.db.sql(
		"""
		UPDATE `tabSales Invoice Item` si, `tabSales Order` so
			set si.customer_po_no = so.po_no, si.customer_po_date = so.po_date
		WHERE
			si.sales_order = so.name and so.po_no is not null
	"""
	)
