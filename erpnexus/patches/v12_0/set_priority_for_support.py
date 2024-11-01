import saashq


def execute():
	saashq.reload_doc("support", "doctype", "issue_priority")
	saashq.reload_doc("support", "doctype", "service_level_priority")
	saashq.reload_doc("support", "doctype", "issue")

	set_issue_priority()
	set_priority_for_issue()
	set_priorities_service_level()
	set_priorities_service_level_agreement()


def set_issue_priority():
	# Adds priority from issue to Issue Priority DocType as Priority is a new DocType.
	for priority in saashq.get_meta("Issue").get_field("priority").options.split("\n"):
		if priority and not saashq.db.exists("Issue Priority", priority):
			saashq.get_doc({"doctype": "Issue Priority", "name": priority}).insert(ignore_permissions=True)


def set_priority_for_issue():
	# Sets priority for Issues as Select field is changed to Link field.
	issue_priority = saashq.get_list("Issue", fields=["name", "priority"])
	saashq.reload_doc("support", "doctype", "issue")

	for issue in issue_priority:
		saashq.db.set_value("Issue", issue.name, "priority", issue.priority)


def set_priorities_service_level():
	# Migrates "priority", "response_time", "response_time_period", "resolution_time", "resolution_time_period" to Child Table
	# as a Service Level can have multiple priorities
	try:
		service_level_priorities = saashq.get_list(
			"Service Level",
			fields=[
				"name",
				"priority",
				"response_time",
				"response_time_period",
				"resolution_time",
				"resolution_time_period",
			],
		)

		saashq.reload_doc("support", "doctype", "service_level")
		saashq.reload_doc("support", "doctype", "support_settings")
		saashq.db.set_single_value("Support Settings", "track_service_level_agreement", 1)

		for service_level in service_level_priorities:
			if service_level:
				doc = saashq.get_doc("Service Level", service_level.name)
				if not doc.priorities:
					doc.append(
						"priorities",
						{
							"priority": service_level.priority,
							"default_priority": 1,
							"response_time": service_level.response_time,
							"response_time_period": service_level.response_time_period,
							"resolution_time": service_level.resolution_time,
							"resolution_time_period": service_level.resolution_time_period,
						},
					)
					doc.flags.ignore_validate = True
					doc.save(ignore_permissions=True)
	except saashq.db.TableMissingError:
		saashq.reload_doc("support", "doctype", "service_level")


def set_priorities_service_level_agreement():
	# Migrates "priority", "response_time", "response_time_period", "resolution_time", "resolution_time_period" to Child Table
	# as a Service Level Agreement can have multiple priorities
	try:
		service_level_agreement_priorities = saashq.get_list(
			"Service Level Agreement",
			fields=[
				"name",
				"priority",
				"response_time",
				"response_time_period",
				"resolution_time",
				"resolution_time_period",
			],
		)

		saashq.reload_doc("support", "doctype", "service_level_agreement")

		for service_level_agreement in service_level_agreement_priorities:
			if service_level_agreement:
				doc = saashq.get_doc("Service Level Agreement", service_level_agreement.name)

				if doc.customer:
					doc.entity_type = "Customer"
					doc.entity = doc.customer

				doc.append(
					"priorities",
					{
						"priority": service_level_agreement.priority,
						"default_priority": 1,
						"response_time": service_level_agreement.response_time,
						"response_time_period": service_level_agreement.response_time_period,
						"resolution_time": service_level_agreement.resolution_time,
						"resolution_time_period": service_level_agreement.resolution_time_period,
					},
				)
				doc.flags.ignore_validate = True
				doc.save(ignore_permissions=True)
	except saashq.db.TableMissingError:
		saashq.reload_doc("support", "doctype", "service_level_agreement")
