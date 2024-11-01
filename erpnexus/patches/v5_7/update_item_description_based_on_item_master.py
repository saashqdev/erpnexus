import saashq


def execute():
	name = saashq.db.sql(
		""" select name from `tabPatch Log` \
		where \
			patch like 'execute:saashq.db.sql("update `tabProduction Order` pro set description%' """
	)
	if not name:
		saashq.db.sql(
			"update `tabProduction Order` pro \
			set \
				description = (select description from tabItem where name=pro.production_item) \
			where \
				ifnull(description, '') = ''"
		)
