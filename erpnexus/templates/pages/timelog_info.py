import saashq


def get_context(context):
	context.no_cache = 1

	timelog = saashq.get_doc("Time Log", saashq.form_dict.timelog)

	context.doc = timelog
