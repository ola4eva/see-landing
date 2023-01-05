import string
from odoo import api, fields, models, _


class Product(models.Model):
    _inherit  = "product.pricelist"
    
    brand = fields.Many2one("brand.brand")
