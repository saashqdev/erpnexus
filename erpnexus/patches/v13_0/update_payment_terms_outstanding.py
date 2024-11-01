# Copyright (c) 2020, Saashq Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


import saashq


def execute():
	saashq.reload_doc("accounts", "doctype", "Payment Schedule")
	if saashq.db.count("Payment Schedule"):
		saashq.db.sql(
			"""
			UPDATE
				`tabPayment Schedule` ps
			SET
				ps.outstanding = (ps.payment_amount - ps.paid_amount)
		"""
		)
