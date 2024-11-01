import saashq
from saashq.query_builder import DocType


def execute():
	if saashq.db.has_column("Asset Maintenance Log", "task_assignee_email"):
		asset_maintenance_log = DocType("Asset Maintenance Log")
		asset_maintenance_task = DocType("Asset Maintenance Task")
		try:
			(
				saashq.qb.update(asset_maintenance_log)
				.set(asset_maintenance_log.task_assignee_email, asset_maintenance_task.assign_to)
				.join(asset_maintenance_task)
				.on(asset_maintenance_log.task == asset_maintenance_task.name)
				.run()
			)
		except Exception:
			saashq.log_error("Failed to update Task Assignee Email Field.")
