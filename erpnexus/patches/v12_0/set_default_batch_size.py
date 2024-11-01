import saashq


def execute():
	saashq.reload_doc("manufacturing", "doctype", "bom_operation")
	saashq.reload_doc("manufacturing", "doctype", "work_order_operation")

	saashq.db.sql(
		"""
        UPDATE
            `tabBOM Operation` bo
        SET
            bo.batch_size = 1
    """
	)
	saashq.db.sql(
		"""
        UPDATE
            `tabWork Order Operation` wop
        SET
            wop.batch_size = 1
    """
	)
