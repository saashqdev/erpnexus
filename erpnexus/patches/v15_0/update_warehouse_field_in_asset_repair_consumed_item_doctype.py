import saashq


# not able to use saashq.qb because of this bug https://github.com/saashqdev/saashq/issues/20292
def execute():
	if saashq.db.has_column("Asset Repair", "warehouse"):
		# nosemgrep
		saashq.db.sql(
			"""UPDATE `tabAsset Repair Consumed Item` ar_item
			JOIN `tabAsset Repair` ar
			ON ar.name = ar_item.parent
			SET ar_item.warehouse = ar.warehouse
			WHERE ifnull(ar.warehouse, '') != ''"""
		)
