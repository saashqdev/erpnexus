import saashq
from saashq.query_builder.functions import IfNull


def execute():
	columns = saashq.db.get_table_columns("Stock Reservation Entry")

	if set(["against_pick_list", "against_pick_list_item"]).issubset(set(columns)):
		sre = saashq.qb.DocType("Stock Reservation Entry")
		(
			saashq.qb.update(sre)
			.set(sre.from_voucher_type, "Pick List")
			.set(sre.from_voucher_no, sre.against_pick_list)
			.set(sre.from_voucher_detail_no, sre.against_pick_list_item)
			.where((IfNull(sre.against_pick_list, "") != "") & (IfNull(sre.against_pick_list_item, "") != ""))
		).run()
