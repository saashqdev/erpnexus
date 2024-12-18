import saashq


def execute():
	# not using saashq.qb because https://github.com/saashqdev/saashq/issues/20292
	saashq.db.sql(
		"""UPDATE `tabAsset Depreciation Schedule`
        JOIN `tabAsset`
        ON `tabAsset Depreciation Schedule`.`asset`=`tabAsset`.`name`
        SET
            `tabAsset Depreciation Schedule`.`gross_purchase_amount`=`tabAsset`.`gross_purchase_amount`,
            `tabAsset Depreciation Schedule`.`opening_number_of_booked_depreciations`=`tabAsset`.`opening_number_of_booked_depreciations`
        WHERE
        (
            `tabAsset Depreciation Schedule`.`gross_purchase_amount`<>`tabAsset`.`gross_purchase_amount`
            OR
            `tabAsset Depreciation Schedule`.`opening_number_of_booked_depreciations`<>`tabAsset`.`opening_number_of_booked_depreciations`
        )
        AND `tabAsset Depreciation Schedule`.`docstatus`<2"""
	)
