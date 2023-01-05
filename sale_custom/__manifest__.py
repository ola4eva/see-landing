{
	"name": "Sale custom",
	"description" : """ Customize sales to meet See Landing requirements""",
	"author": "See Landing",
	"website" : "",
	"category" : "sale",


	"depends" : ["base","sale_management","contacts","sale_stock"],

	"data" : [
		"security/ir.model.access.csv",
		"views/brands_view.xml",
		"views/regions_view.xml",
		"views/pricelist_view.xml",
		"views/product_view.xml",
		"views/customer_brands_view.xml",
		"views/sale_order_inherit_view.xml",
		"views/stock_picking_view.xml",
		"views/product_pack.xml",
		"report/delivery_slip_template.xml",
	],
	"version" : "1.0",
	"summary" : "See Landing sales customization",

	'license': 'LGPL-3',
	"application": True,
	"sequence": 10,

}
