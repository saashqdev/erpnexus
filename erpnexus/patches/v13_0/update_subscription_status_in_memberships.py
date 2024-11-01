import saashq


def execute():
	if saashq.db.exists("DocType", "Member"):
		saashq.reload_doc("Non Profit", "doctype", "Member")

		if saashq.db.has_column("Member", "subscription_activated"):
			saashq.db.sql(
				'UPDATE `tabMember` SET subscription_status = "Active" WHERE subscription_activated = 1'
			)
			saashq.db.sql_ddl("ALTER table `tabMember` DROP COLUMN subscription_activated")
