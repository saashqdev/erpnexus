# Copyright (c) 2017, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq

from erpnexus.manufacturing.doctype.work_order.work_order import create_job_card


def execute():
	saashq.reload_doc("manufacturing", "doctype", "work_order")
	saashq.reload_doc("manufacturing", "doctype", "work_order_item")
	saashq.reload_doc("manufacturing", "doctype", "job_card")
	saashq.reload_doc("manufacturing", "doctype", "job_card_item")

	fieldname = saashq.db.get_value(
		"DocField", {"fieldname": "work_order", "parent": "Timesheet"}, "fieldname"
	)
	if not fieldname:
		fieldname = saashq.db.get_value(
			"DocField", {"fieldname": "production_order", "parent": "Timesheet"}, "fieldname"
		)
		if not fieldname:
			return

	for d in saashq.get_all(
		"Timesheet", filters={fieldname: ["!=", ""], "docstatus": 0}, fields=[fieldname, "name"]
	):
		if d[fieldname]:
			doc = saashq.get_doc("Work Order", d[fieldname])
			for row in doc.operations:
				create_job_card(doc, row, auto_create=True)
			saashq.delete_doc("Timesheet", d.name)
