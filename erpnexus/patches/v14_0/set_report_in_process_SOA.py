# Copyright (c) 2022, Saashq Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import saashq


def execute():
	process_soa = saashq.qb.DocType("Process Statement Of Accounts")
	q = saashq.qb.update(process_soa).set(process_soa.report, "General Ledger")
	q.run()
