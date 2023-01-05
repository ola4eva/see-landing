# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Stock_Move_reports(models.Model):
    _inherit = 'stock.picking'

    def get_report_data(self):
        for rec in self:
            sale_order = self.env['sale.order'].search([('name', '=', rec.origin)])
            stock_picking = self.env['stock.picking'].search([('origin', '=', rec.origin)])
            dic = []
            lines = []
            for so in sale_order:
                due = ''
                pay = ''
                if so.invoice_ids:
                    if so.invoice_ids[0]:
                        due = so.invoice_ids[0].invoice_date_due
                        pay = so.invoice_ids[0].payment_method.name

                for pick in so.picking_ids:
                    for move in pick.move_ids_without_package:
                        if pick.state == 'done':
                            
                           
                            lines.append({
                                'product_id': move.product_id.name ,
                                'item_code': move.product_id.default_code,
                                'unit_price': move.sale_line_id.price_unit,
                                'tax_id': move.sale_line_id.price_tax ,
                                'subtotal': move.sale_line_id.price_subtotal ,
                                'product_uom_qty': move.product_uom_qty ,
                                'product_uom': move.product_uom_qty,
                                'quantity_done': move.quantity_done,
                                'product_uom': move.product_uom.name,
                                'price_subtotal':move.sale_line_id.price_subtotal,
                                'customer_po': move.sale_line_id.order_id.po_refernce,
                                'tax_id_name': move.sale_line_id.tax_id[0].name

                            })
                    dic.append({
                        'SO_total': so.amount_total,
                        'po_reference':so.po_refernce,
                        'invoice_due': due,
                        'invoice_payment': pay,
                        'lines': lines


                    })

        return dic
