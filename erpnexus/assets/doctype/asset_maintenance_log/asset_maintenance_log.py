# Copyright (c) 2017, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import saashq
from saashq import _
from saashq.model.document import Document
from saashq.query_builder import DocType
from saashq.utils import getdate, nowdate, today

from erpnexus.assets.doctype.asset_maintenance.asset_maintenance import calculate_next_due_date


class AssetMaintenanceLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		actions_performed: DF.TextEditor | None
		amended_from: DF.Link | None
		asset_maintenance: DF.Link | None
		asset_name: DF.ReadOnly | None
		assign_to_name: DF.ReadOnly | None
		certificate_attachement: DF.Attach | None
		completion_date: DF.Date | None
		description: DF.ReadOnly | None
		due_date: DF.Date | None
		has_certificate: DF.Check
		item_code: DF.ReadOnly | None
		item_name: DF.ReadOnly | None
		maintenance_status: DF.Literal["Planned", "Completed", "Cancelled", "Overdue"]
		maintenance_type: DF.ReadOnly | None
		naming_series: DF.Literal["ACC-AML-.YYYY.-"]
		periodicity: DF.Data | None
		task: DF.Link | None
		task_assignee_email: DF.Data | None
		task_name: DF.Data | None
	# end: auto-generated types

	def validate(self):
		if getdate(self.due_date) < getdate(nowdate()) and self.maintenance_status not in [
			"Completed",
			"Cancelled",
		]:
			self.maintenance_status = "Overdue"

		if self.maintenance_status == "Completed" and not self.completion_date:
			saashq.throw(_("Please select Completion Date for Completed Asset Maintenance Log"))

		if self.maintenance_status != "Completed" and self.completion_date:
			saashq.throw(_("Please select Maintenance Status as Completed or remove Completion Date"))

	def on_submit(self):
		if self.maintenance_status not in ["Completed", "Cancelled"]:
			saashq.throw(_("Maintenance Status has to be Cancelled or Completed to Submit"))
		self.update_maintenance_task()

	def update_maintenance_task(self):
		asset_maintenance_doc = saashq.get_doc("Asset Maintenance Task", self.task)
		if self.maintenance_status == "Completed":
			if asset_maintenance_doc.last_completion_date != self.completion_date:
				next_due_date = calculate_next_due_date(
					periodicity=self.periodicity, last_completion_date=self.completion_date
				)
				asset_maintenance_doc.last_completion_date = self.completion_date
				asset_maintenance_doc.next_due_date = next_due_date
				asset_maintenance_doc.maintenance_status = "Planned"
				asset_maintenance_doc.save()
		if self.maintenance_status == "Cancelled":
			asset_maintenance_doc.maintenance_status = "Cancelled"
			asset_maintenance_doc.save()
		asset_maintenance_doc = saashq.get_doc("Asset Maintenance", self.asset_maintenance)
		asset_maintenance_doc.save()


def update_asset_maintenance_log_status():
	AssetMaintenanceLog = DocType("Asset Maintenance Log")
	(
		saashq.qb.update(AssetMaintenanceLog)
		.set(AssetMaintenanceLog.maintenance_status, "Overdue")
		.where(
			(AssetMaintenanceLog.maintenance_status == "Planned") & (AssetMaintenanceLog.due_date < today())
		)
	).run()


@saashq.whitelist()
@saashq.validate_and_sanitize_search_inputs
def get_maintenance_tasks(doctype, txt, searchfield, start, page_len, filters):
	asset_maintenance_tasks = saashq.db.get_values(
		"Asset Maintenance Task", {"parent": filters.get("asset_maintenance")}, "maintenance_task"
	)
	return asset_maintenance_tasks
