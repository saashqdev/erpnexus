import saashq


def execute():
	saashq.reload_doc("core", "doctype", "scheduled_job_type")
	if saashq.db.exists("Scheduled Job Type", "repost_item_valuation.repost_entries"):
		saashq.db.set_value("Scheduled Job Type", "repost_item_valuation.repost_entries", "stopped", 0)
