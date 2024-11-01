import saashq


def execute():
	saashq.db.sql(
		"""UPDATE `tabUser` SET `home_settings` = REPLACE(`home_settings`, 'Accounting', 'Accounts')"""
	)
	saashq.cache().delete_key("home_settings")
