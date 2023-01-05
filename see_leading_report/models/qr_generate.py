from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import qrcode
import base64
from io import BytesIO
import codecs

class Invoice(models.Model):
    _inherit = "account.move"

    qr_code = fields.Binary("QR Code", store=True, compute="_generate_qr_code")
    payment_method = fields.Many2one('account.journal',compute="set_journal_id",store=True)
    text_amount = fields.Char(compute="set_amount_text",store=True)

    def set_delivery_address(self):
        for rec in self:
            address = ''
            if rec.partner_shipping_id and rec.partner_shipping_id.parent_id.child_ids:
               
                for ch in rec.partner_shipping_id.parent_id.child_ids:
                    if ch.type == 'delivery':
                        address = ch.street
                return address
            return address

    def set_delivery_name(self):
        for rec in self:
            brand = ''
            if rec.partner_shipping_id and rec.partner_shipping_id.parent_id.brands:
                brand = rec.partner_shipping_id.parent_id.brands.name
            return brand
         

    @api.depends('name','amount_total')
    def set_amount_text(self):
        for rec in self:
            txt = rec.currency_id.amount_to_text(rec.amount_total)
            rec.text_amount = txt

    @api.depends('payment_state','name','state')
    def set_journal_id(self):
        for rec in self:
            payment = self.env['account.payment'].search([])
            for pay in payment:
                if rec.id in pay.reconciled_invoice_ids.ids:
                    rec.payment_method = payment.journal_id.id
                    break
    

    @api.depends("name", "write_date")
    def _generate_qr_code(self):
        for record in self:


            qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=4,border=1,)
            str_value_hex = ''
            str_value_hex += self.getHex(1, str(record.company_id.name))
            str_value_hex += self.getHex(2, record.company_id.vat)
            str_value_hex += self.getHex(3, str(record.create_date))
            str_value_hex += self.getHex(4, str("{:.2f}".format(round(record.amount_total, 2))))
            str_value_hex += self.getHex(5, str("{:.2f}".format(round(record.amount_total - record.amount_untaxed, 2))))
            base64_value = codecs.encode(codecs.decode(str_value_hex, 'hex'), 'base64').decode()
            # raise ValidationError(base64_value)
            # data = "Invoice Number: "+ record.name + "\n" + "Invoice Date: " + str(record.invoice_date) + "\n" + "Company: " + record.company_id.name + "\n" +"VAT No.: " + str(record.company_id.vat) + "\n" + "Total VAT: " + str(record.amount_tax) + "\n" + "Total Amount Due: " + str(record.amount_residual)

            qr.add_data(base64_value)
            
            qr.make()
            img = qr.make_image()
            temp = BytesIO()
            #img.resize((24, 24))
            #img = resizeimage.resize_cover(img, [20, 10])
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            record.qr_code = qr_image
          
    def getHex(self, tag, value):
        if type(tag) != int or type(value) != str or len(str(value)) < 1:
            return False
        length = len(value)
        length_hex = format(length, 'x')
        if len(length_hex) == 1:
            length_hex = '0' + length_hex
        tag_hex = format(int(tag), 'x')
        if len(tag_hex) == 1:
            tag_hex = '0' + tag_hex
        value_hex = bytes(value, 'utf-8').hex()
        return tag_hex + length_hex + value_hex
