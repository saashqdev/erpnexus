import saashq
from saashq.utils import flt


def execute():
	for project in saashq.get_all("Project", fields=["name", "percent_complete_method"]):
		total = saashq.db.count("Task", dict(project=project.name))
		if project.percent_complete_method == "Task Completion" and total > 0:
			completed = saashq.db.sql(
				"""select count(name) from tabTask where
					project=%s and status in ('Cancelled', 'Completed')""",
				project.name,
			)[0][0]
			percent_complete = flt(flt(completed) / total * 100, 2)
			if project.percent_complete != percent_complete:
				saashq.db.set_value("Project", project.name, "percent_complete", percent_complete)
				if percent_complete == 100:
					saashq.db.set_value("Project", project.name, "status", "Completed")
