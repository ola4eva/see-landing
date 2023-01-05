from odoo import api, fields, models, _


class Brand(models.Model):
    _name = "brand.brand"
    _description = "products brands"

    name = fields.Char("Name" , required=True,)
    regions = fields.Many2many("region.region")
