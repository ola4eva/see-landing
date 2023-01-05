from odoo import api, fields, models, _


class Region(models.Model):
    _name = "region.region"
    _description = "products regions"

    name = fields.Char("Name" , required=True,)
    branches = fields.Many2many("res.partner",domain="[('customer_rank','>', 0),]")
