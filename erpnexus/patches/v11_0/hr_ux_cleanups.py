import saashq


def execute():
	saashq.reload_doctype("Employee")
	saashq.db.sql("update tabEmployee set first_name = employee_name")

	# update holiday list
	saashq.reload_doctype("Holiday List")
	for holiday_list in saashq.get_all("Holiday List"):
		holiday_list = saashq.get_doc("Holiday List", holiday_list.name)
		holiday_list.db_set("total_holidays", len(holiday_list.holidays), update_modified=False)
