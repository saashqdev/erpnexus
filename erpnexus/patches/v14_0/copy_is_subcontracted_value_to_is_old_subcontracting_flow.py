# Copyright (c) 2022, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import saashq


def execute():
	for doctype in ["Purchase Order", "Purchase Receipt", "Purchase Invoice"]:
		tab = saashq.qb.DocType(doctype).as_("tab")
		saashq.qb.update(tab).set(tab.is_old_subcontracting_flow, 1).where(tab.is_subcontracted == 1).run()
