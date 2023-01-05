# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Account_Move_Line(models.Model):
    _inherit = 'account.move.line'

    so_line_id = fields.Many2one('sale.order.line')
    


class Account_Move_reports(models.Model):
    _inherit = 'account.move'


    tag_brands = fields.Char(string='Brands',
                             copy=False,
                             compute='_get_brands',
                             
                             )
    tag_regions = fields.Char(string='Regions',
                              copy=False,
                              compute='_get_brands',
                            
                              )

    multi_invoice = fields.Boolean()
    brand = fields.Many2one(comodel_name="brand.brand", string="Brand", related="partner_shipping_id.parent_id.brands")
    region = fields.Many2one(comodel_name="region.region", string="Region",related="partner_shipping_id.parent_id.region" )



    @api.model
    def _get_brands(self):
        tag_brands = ''
        tag_regions = ''
        for rec in self:
            if rec.partner_id:
                if rec.partner_id.brands:
                    tag_brands = ','.join([p.name for p in rec.partner_id.brands])
                else:
                    tag_brands = ','.join([p.name for p in rec.partner_id.parent_id.brands])
                tag_regions = ','.join([p.name for p in rec.partner_id.region])
            else:
                tag_brands = ''
                tag_regions = ''
            rec.tag_brands = tag_brands
            rec.tag_regions = tag_regions



    def get_delivery_data_from_quotation(self):

        for rec in self:
            dic = []
            so_list = []
            if rec.invoice_origin:
                origin = rec.invoice_origin.split()
                
                for org in origin:
                    org_name = org.split(',')
                    
                    for ori in org_name:
                        so_list.append(ori)
            
            sale_order = self.env['sale.order'].search([('name', 'in', so_list)])
           
            stock_picking = self.env['stock.picking'].search([('origin', 'in', so_list)])
           
            for so in sale_order:
                for pick in so.picking_ids:
                    if pick.state == 'done':
                        dic.append({
                            'SO_total': so.amount_total,
                            'invoice_date': pick.date_done,
                            'delivery': pick.name,
                            'po_reference':so.po_refernce,
                            'branch':so.partner_id.name,
                            'region':so.partner_id.region.name,

                        })

        return dic
