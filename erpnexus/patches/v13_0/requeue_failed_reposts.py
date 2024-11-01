import saashq
from saashq.utils import cstr


def execute():
	reposts = saashq.get_all(
		"Repost Item Valuation",
		{"status": "Failed", "modified": [">", "2021-10-05"]},
		["name", "modified", "error_log"],
	)

	for repost in reposts:
		if "check_freezing_date" in cstr(repost.error_log):
			saashq.db.set_value("Repost Item Valuation", repost.name, "status", "Queued")
