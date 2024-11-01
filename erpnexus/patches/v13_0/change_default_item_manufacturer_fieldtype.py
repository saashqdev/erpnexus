import saashq


def execute():
	# Erase all default item manufacturers that dont exist.
	item = saashq.qb.DocType("Item")
	manufacturer = saashq.qb.DocType("Manufacturer")

	(
		saashq.qb.update(item)
		.set(item.default_item_manufacturer, None)
		.left_join(manufacturer)
		.on(item.default_item_manufacturer == manufacturer.name)
		.where(manufacturer.name.isnull() & item.default_item_manufacturer.isnotnull())
	).run()
