import saashq


def execute():
	saashq.reload_doc("projects", "doctype", "project")

	saashq.db.sql(
		"""UPDATE `tabProject`
		SET
			naming_series = 'PROJ-.####'
		WHERE
			naming_series is NULL"""
	)
