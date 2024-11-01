import saashq


def execute():
	user_permissions = saashq.db.sql(
		"""select name, for_value from `tabUser Permission`
        where allow='Department'""",
		as_dict=1,
	)
	for d in user_permissions:
		user_permission = saashq.get_doc("User Permission", d.name)
		for new_dept in saashq.db.sql(
			"""select name from tabDepartment
            where ifnull(company, '') != '' and department_name=%s""",
			d.for_value,
		):
			try:
				new_user_permission = saashq.copy_doc(user_permission)
				new_user_permission.for_value = new_dept[0]
				new_user_permission.save()
			except saashq.DuplicateEntryError:
				pass

	saashq.reload_doc("hr", "doctype", "department")
	saashq.db.sql("update tabDepartment set disabled=1 where ifnull(company, '') = ''")
