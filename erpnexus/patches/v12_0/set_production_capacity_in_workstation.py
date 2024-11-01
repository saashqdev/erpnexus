import saashq


def execute():
	saashq.reload_doc("manufacturing", "doctype", "workstation")

	saashq.db.sql(
		""" UPDATE `tabWorkstation`
        SET production_capacity = 1 """
	)
