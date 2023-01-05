import string
from odoo import api, fields, models, _


class Product(models.Model):
    _inherit  = "product.product"
    
    brand = fields.Many2one("brand.brand", string="Product Brand")

class ProductTemplate(models.Model):
    _inherit  = "product.template"
    
    brand = fields.Many2one("brand.brand", string="Product Brand")
