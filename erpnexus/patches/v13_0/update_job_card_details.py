# Copyright (c) 2019, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	saashq.reload_doc("manufacturing", "doctype", "job_card")
	saashq.reload_doc("manufacturing", "doctype", "job_card_item")
	saashq.reload_doc("manufacturing", "doctype", "work_order_operation")

	saashq.db.sql(
		""" update `tabJob Card` jc, `tabWork Order Operation` wo
		SET	jc.hour_rate =  wo.hour_rate
		WHERE
			jc.operation_id = wo.name and jc.docstatus < 2 and wo.hour_rate > 0
	"""
	)
