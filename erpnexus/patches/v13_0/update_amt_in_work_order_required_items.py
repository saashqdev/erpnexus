import saashq


def execute():
	"""Correct amount in child table of required items table."""

	saashq.reload_doc("manufacturing", "doctype", "work_order")
	saashq.reload_doc("manufacturing", "doctype", "work_order_item")

	saashq.db.sql(
		"""UPDATE `tabWork Order Item` SET amount = ifnull(rate, 0.0) * ifnull(required_qty, 0.0)"""
	)
