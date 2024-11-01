# Copyright (c) 2017, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	saashq.reload_doc("setup", "doctype", "target_detail")
	saashq.reload_doc("core", "doctype", "prepared_report")

	for d in ["Sales Person", "Sales Partner", "Territory"]:
		saashq.db.sql(
			"""
            UPDATE `tab{child_doc}`, `tab{parent_doc}`
            SET
                `tab{child_doc}`.distribution_id = `tab{parent_doc}`.distribution_id
            WHERE
                `tab{child_doc}`.parent = `tab{parent_doc}`.name
                and `tab{parent_doc}`.distribution_id is not null and `tab{parent_doc}`.distribution_id != ''
        """.format(parent_doc=d, child_doc="Target Detail")
		)

	saashq.delete_doc("Report", "Sales Partner-wise Transaction Summary")
	saashq.delete_doc("Report", "Sales Person Target Variance Item Group-Wise")
	saashq.delete_doc("Report", "Territory Target Variance Item Group-Wise")
