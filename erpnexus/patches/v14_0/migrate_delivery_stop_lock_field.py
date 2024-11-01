import saashq
from saashq.model.utils.rename_field import rename_field


def execute():
	if saashq.db.has_column("Delivery Stop", "lock"):
		rename_field("Delivery Stop", "lock", "locked")
