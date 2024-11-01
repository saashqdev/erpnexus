import saashq


def execute():
	saashq.reload_doc("crm", "doctype", "lead")
	saashq.db.sql(
		"""
		UPDATE
			`tabLead`
		SET
			title = IF(organization_lead = 1, company_name, lead_name)
	"""
	)
