// Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

saashq.provide("erpnexus");

// preferred modules for breadcrumbs
$.extend(saashq.breadcrumbs.preferred, {
	"Item Group": "Stock",
	"Customer Group": "Selling",
	"Supplier Group": "Buying",
	Territory: "Selling",
	"Sales Person": "Selling",
	"Sales Partner": "Selling",
	Brand: "Stock",
	"Maintenance Schedule": "Support",
	"Maintenance Visit": "Support",
});

$.extend(saashq.breadcrumbs.module_map, {
	"ERPNexus Integrations": "Integrations",
	Geo: "Settings",
	Portal: "Website",
	Utilities: "Settings",
	"E-commerce": "Website",
	Contacts: "CRM",
});
