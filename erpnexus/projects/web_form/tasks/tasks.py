import saashq


def get_context(context):
	if saashq.form_dict.project:
		context.parents = [
			{"title": saashq.form_dict.project, "route": "/projects?project=" + saashq.form_dict.project}
		]
		context.success_url = "/projects?project=" + saashq.form_dict.project

	elif context.doc and context.doc.get("project"):
		context.parents = [
			{"title": context.doc.project, "route": "/projects?project=" + context.doc.project}
		]
		context.success_url = "/projects?project=" + context.doc.project
