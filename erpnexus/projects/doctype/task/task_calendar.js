// Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

saashq.views.calendar["Task"] = {
	field_map: {
		start: "exp_start_date",
		end: "exp_end_date",
		id: "name",
		title: "subject",
		allDay: "allDay",
		progress: "progress",
	},
	gantt: true,
	filters: [
		{
			fieldtype: "Link",
			fieldname: "project",
			options: "Project",
			label: __("Project"),
		},
	],
	get_events_method: "saashq.desk.calendar.get_events",
};
