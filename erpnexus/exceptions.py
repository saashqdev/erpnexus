import saashq


# accounts
class PartyFrozen(saashq.ValidationError):
	pass


class InvalidAccountCurrency(saashq.ValidationError):
	pass


class InvalidCurrency(saashq.ValidationError):
	pass


class PartyDisabled(saashq.ValidationError):
	pass


class InvalidAccountDimensionError(saashq.ValidationError):
	pass


class MandatoryAccountDimensionError(saashq.ValidationError):
	pass
