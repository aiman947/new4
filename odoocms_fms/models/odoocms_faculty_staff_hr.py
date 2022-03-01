from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import pdb

# Passport DB Table

class OdooCMSPassport(models.Model):
    _name = 'odoocms.passport'
    _description = 'Faculty Passport'

    faculity_staff_child_id = fields.Many2one('odoocms.faculty.staff', string ='Faculty id')
    fms_passport_no = fields.Char(string="Passport.No")
    fms_passport_dt_issue = fields.Date(string="Date of Issue")
    fms_passport_dt_expiry = fields.Date(string="Valid upto")
    fms_passport_booklet_no = fields.Char(string="Booklet No")
    fms_passport_country = fields.Many2one('res.country', string='Passport(Country)', )
    fms_passport_issue_body = fields.Many2one('res.country', string='Issuing(Country)', )

