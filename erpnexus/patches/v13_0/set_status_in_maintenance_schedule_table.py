import saashq


def execute():
	saashq.reload_doc("maintenance", "doctype", "Maintenance Schedule Detail")
	saashq.db.sql(
		"""
		UPDATE `tabMaintenance Schedule Detail`
		SET completion_status = 'Pending'
		WHERE docstatus < 2
	"""
	)
