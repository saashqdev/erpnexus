# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# GPL v3 License. See license.txt

import click


def call_command(cmd, context):
	return click.Context(cmd, obj=context).forward(cmd)


commands = []
