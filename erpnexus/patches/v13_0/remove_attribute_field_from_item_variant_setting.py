import saashq


def execute():
	"""Remove has_variants and attribute fields from item variant settings."""
	saashq.reload_doc("stock", "doctype", "Item Variant Settings")

	saashq.db.sql(
		"""delete from `tabVariant Field`
			where field_name in ('attributes', 'has_variants')"""
	)
