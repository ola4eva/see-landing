from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, html_keep_url, is_html_empty

class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    tag_brands = fields.Many2one(related="partner_id.brands",store=True)
    tag_regions = fields.Char(string='Regions', store=True)
    po_refernce = fields.Char(string="PO#")

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment terms
        - Invoice address
        - Delivery address
        - Sales Team
        """
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'fiscal_position_id': False,
            })
            return

        self = self.with_company(self.company_id)

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        partner_user = self.partner_id.user_id or self.partner_id.commercial_partner_id.user_id
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': self.partner_id.parent_id.id or addr['invoice'],
            'partner_shipping_id': addr['delivery'],
        }
        user_id = partner_user.id
        if not self.env.context.get('not_self_saleperson'):
            user_id = user_id or self.env.context.get('default_user_id', self.env.uid)
        if user_id and self.user_id.id != user_id:
            values['user_id'] = user_id

        if self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms'):
            if self.terms_type == 'html' and self.env.company.invoice_terms_html:
                baseurl = html_keep_url(self.get_base_url() + '/terms')
                values['note'] = _('Terms & Conditions: %s', baseurl)
            elif not is_html_empty(self.env.company.invoice_terms):
                values['note'] = self.with_context(lang=self.partner_id.lang).env.company.invoice_terms
        if not self.env.context.get('not_self_saleperson') or not self.team_id:
            values['team_id'] = self.env['crm.team'].with_context(
                default_team_id=self.partner_id.team_id.id
            )._get_default_team_id(domain=['|', ('company_id', '=', self.company_id.id), ('company_id', '=', False)], user_id=user_id)
        self.update(values)


    # @api.model
    # @api.depends('partner_id')
    # def _get_brands(self):
    #     tag_brand = ''
    #     tag_regions = ''
    #     for rec in self:
    #         if rec.partner_id:
    #             if rec.partner_id.brands:
    #                 tag_brand += ','.join([p for p in rec.partner_id.brands])
    #             else:
    #                 tag_brand += ','.join([p for p in rec.partner_id.parent_id.brands])

    #             tag_regions += ','.join([p for p in rec.partner_id.region])
    #         else:
    #             tag_brand = ''
    #             tag_regions = ''
    #         rec.tag_brands = tag_brand
    #         rec.tag_regions = tag_regions


class saleOrdersInvoice(models.TransientModel):
    _name = 'sale.multi.invoice'
    _description = "Mulri invoice on so"

    brand_id = fields.Many2one(comodel_name="brand.brand", string="Brand", )
    region_id = fields.Many2one(comodel_name="region.region", string="Region", )

    def sort_SO_with_brand(self):
        so_list = []
        so_region_list = []
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        for so in sale_orders:
            for brand in so.partner_id.parent_id.brands:
                if self.brand_id:
                    if brand == self.brand_id:
                        so_list.append(so)

        return so_list

    def sort_SO_with_region(self):
        so_region_list = []
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        for so in sale_orders:
            for brand in so.partner_id.parent_id.brands:
                if self.region_id:
                    for reg in brand.regions:
                        if reg == self.region_id:
                            so_region_list.append(so)

        return so_region_list

    def create_invoices(self):   
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        orig = ''
        for so in sale_orders:
            orig += so.name +','
        band_list = []
        
        brand_list = self.sort_SO_with_brand()
        li_lines = []
       
        invoice = self.env['account.move'].create({
                'partner_id': sale_orders[0].partner_id.parent_id.id,
                'move_type': 'out_invoice',
                'multi_invoice': True  ,
                'invoice_origin':orig,
                'brand':self.brand_id.id,
                'region':self.region_id.id
            })

        invoice_lines = []
        for order in sale_orders:
            if order.invoice_status == 'invoiced':
                raise UserError(_('Sale Order  %s already invoiced', order.name))

            order.invoice_status = 'invoiced'
            invoice_lines = []
            analytic_tag_ids = []
            
            invoice_lines = []

            for line in order.order_line:
                invoice_lines = (0,0,{
                    'product_id': line.product_id.id,
                    'quantity': line.qty_delivered,
                    'account_id': line.product_id.property_account_income_id.id or line.product_id.categ_id.property_account_income_categ_id.id,
                    'product_uom_id': line.product_uom.id,
                    'tax_ids':line.tax_id.ids,
                    'move_id':invoice.id,
                    'price_unit': line.price_unit,
                    'sale_line_ids': [(6, 0, [line.id])],
                   
                    'exclude_from_invoice_tab':False
                })
                li_lines.append(invoice_lines)

        
        invoice['invoice_line_ids'] = li_lines


        if self._context.get('open_invoices', False):
            return {
                'name': _('Customer Invoice'),
                'view_mode': 'form',
                'view_id': self.env.ref('account.view_move_form').id,
                'res_model': 'account.move',
                'context': "{'type':'out_invoice'}",
                'type': 'ir.actions.act_window',
                'res_id': invoice.id,
        }
        return {'type': 'ir.actions.act_window_close'}



