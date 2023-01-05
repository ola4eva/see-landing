import string
from odoo import api, fields, models, _


class CustomerBrand(models.Model):
    _inherit  = "res.partner"
    

    brands = fields.Many2one("brand.brand", string="Customer Brand")
    region = fields.Many2one("region.region",string="Region")
    cr_number = fields.Char(string="CR number")
