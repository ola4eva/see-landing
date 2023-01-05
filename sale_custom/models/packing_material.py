from odoo import api, fields, models, _


class Packing(models.Model):
    _name = "packing.materials"
    _description = "Packing Materials"

    name = fields.Char("Name", required=True,)
    description = fields.Text()

