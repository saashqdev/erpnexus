import saashq


def execute():
	sabb = saashq.get_all("Serial and Batch Bundle", filters={"docstatus": ("<", 2)}, limit=1)
	if not sabb:
		saashq.db.set_single_value("Stock Settings", "use_serial_batch_fields", 1)
