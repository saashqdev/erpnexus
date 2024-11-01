import saashq


def get_context(context):
	context.no_cache = 1

	task = saashq.get_doc("Task", saashq.form_dict.task)

	context.comments = saashq.get_all(
		"Communication",
		filters={"reference_name": task.name, "comment_type": "comment"},
		fields=["subject", "sender_full_name", "communication_date"],
	)

	context.doc = task
