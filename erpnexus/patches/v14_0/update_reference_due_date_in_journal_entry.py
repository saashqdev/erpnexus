import saashq


def execute():
	if saashq.db.get_value("Journal Entry Account", {"reference_due_date": ""}):
		saashq.db.sql(
			"""
			UPDATE `tabJournal Entry Account`
			SET reference_due_date = NULL
			WHERE reference_due_date = ''
		"""
		)
