from odoo import api, fields, models, _


class PackingInherit(models.Model):
    _inherit = "product.template"

    packing_materials = fields.Many2many('packing.materials')
