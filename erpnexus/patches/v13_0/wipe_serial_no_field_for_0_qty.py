import saashq


def execute():
	doctype = "Stock Reconciliation Item"

	if not saashq.db.has_column(doctype, "current_serial_no"):
		# nothing to fix if column doesn't exist
		return

	sr_item = saashq.qb.DocType(doctype)

	(saashq.qb.update(sr_item).set(sr_item.current_serial_no, None).where(sr_item.current_qty == 0)).run()
