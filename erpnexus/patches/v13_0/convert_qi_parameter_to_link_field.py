import saashq


def execute():
	saashq.reload_doc("stock", "doctype", "quality_inspection_parameter")
	params = set()

	# get all parameters from QI readings table
	for (p,) in saashq.db.get_all("Quality Inspection Reading", fields=["specification"], as_list=True):
		params.add(p.strip())

	# get all parameters from QI Template as some may be unused in QI
	for (p,) in saashq.db.get_all(
		"Item Quality Inspection Parameter", fields=["specification"], as_list=True
	):
		params.add(p.strip())

	# because db primary keys are case insensitive, so duplicates will cause an exception
	params = set({x.casefold(): x for x in params}.values())

	for parameter in params:
		if saashq.db.exists("Quality Inspection Parameter", parameter):
			continue

		saashq.get_doc(
			{"doctype": "Quality Inspection Parameter", "parameter": parameter, "description": parameter}
		).insert(ignore_permissions=True)
