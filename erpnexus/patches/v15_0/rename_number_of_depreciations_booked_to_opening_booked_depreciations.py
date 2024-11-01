import saashq
from saashq.model.utils.rename_field import rename_field


def execute():
	if saashq.db.has_column("Asset", "number_of_depreciations_booked"):
		rename_field("Asset", "number_of_depreciations_booked", "opening_number_of_booked_depreciations")
