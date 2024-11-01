import saashq


def execute():
	saashq.reload_doc("manufacturing", "doctype", "work_order")

	saashq.db.sql(
		"""
		UPDATE
			`tabWork Order` wo
				JOIN `tabItem` item ON wo.production_item = item.item_code
		SET
			wo.item_name = item.item_name
	"""
	)
	saashq.db.commit()
