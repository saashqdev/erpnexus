import saashq
from saashq import _
from saashq.utils.nestedset import rebuild_tree


def execute():
	"""assign lft and rgt appropriately"""
	saashq.reload_doc("setup", "doctype", "department")
	if not saashq.db.exists("Department", _("All Departments")):
		saashq.get_doc(
			{"doctype": "Department", "department_name": _("All Departments"), "is_group": 1}
		).insert(ignore_permissions=True, ignore_mandatory=True)

	saashq.db.sql(
		"""update `tabDepartment` set parent_department = '{}'
		where is_group = 0""".format(_("All Departments"))
	)

	rebuild_tree("Department")
