# Copyright (c) 2019, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	"""Move credit limit and bypass credit limit to the child table of customer credit limit"""
	saashq.reload_doc("Selling", "doctype", "Customer Credit Limit")
	saashq.reload_doc("Selling", "doctype", "Customer")
	saashq.reload_doc("Setup", "doctype", "Customer Group")

	if saashq.db.a_row_exists("Customer Credit Limit"):
		return

	move_credit_limit_to_child_table()


def move_credit_limit_to_child_table():
	"""maps data from old field to the new field in the child table"""

	companies = saashq.get_all("Company", "name")
	for doctype in ("Customer", "Customer Group"):
		fields = ""
		if doctype == "Customer" and saashq.db.has_column(
			"Customer", "bypass_credit_limit_check_at_sales_order"
		):
			fields = ", bypass_credit_limit_check_at_sales_order"

		credit_limit_records = saashq.db.sql(
			f"""
			SELECT name, credit_limit {fields}
			FROM `tab{doctype}` where credit_limit > 0
		""",
			as_dict=1,
		)  # nosec

		for record in credit_limit_records:
			doc = saashq.get_doc(doctype, record.name)
			for company in companies:
				row = saashq._dict({"credit_limit": record.credit_limit, "company": company.name})
				if doctype == "Customer":
					row.bypass_credit_limit_check = record.bypass_credit_limit_check_at_sales_order

				doc.append("credit_limits", row)

			for row in doc.credit_limits:
				row.db_insert()
