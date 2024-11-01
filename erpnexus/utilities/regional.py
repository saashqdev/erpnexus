from contextlib import contextmanager

import saashq


@contextmanager
def temporary_flag(flag_name, value):
	flags = saashq.local.flags
	flags[flag_name] = value
	try:
		yield
	finally:
		flags.pop(flag_name, None)
