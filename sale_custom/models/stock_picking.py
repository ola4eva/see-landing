import string
from odoo import api, fields, models, _


class CustomerBrand(models.Model):
    _inherit  = "stock.picking"
    
    brand = fields.Many2one("brand.brand", compute="set_brand")
    region = fields.Many2one("region.region", compute="set_brand")


    @api.depends('partner_id')
    def set_brand(self):
        for rec in self:

            br = False
            reg = False

            if rec.partner_id and rec.partner_id.parent_id and rec.partner_id.parent_id.brands:
                br = rec.partner_id.parent_id.brands.id 
            if rec.partner_id and rec.partner_id.brands :
                br = rec.partner_id.brands.id 
               
            if rec.partner_id and rec.partner_id.parent_id and rec.partner_id.parent_id.region:
                reg = rec.partner_id.parent_id.region.id 
            if rec.partner_id and rec.partner_id.region :
                reg = rec.partner_id.region.id 

            rec.brand = br
            rec.region = reg
