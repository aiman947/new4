from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import logging
import re
import pdb
import sys
import ftplib
import os
import time
import base64
import codecs
from datetime import datetime, date

_logger = logging.getLogger(__name__)


class OdooCMSStudentTag(models.Model):
    _name = 'odoocms.student.tag'
    _description = 'Student Tag'

    name = fields.Char(string="Student Tag", required=True)
    color = fields.Integer(string='Color Index')
    student_ids = fields.Many2many('odoocms.student',  string='Students')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

    
class OdooCMSStudent(models.Model):
    _name = 'odoocms.student'
    _description = 'Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}
    _order = 'code'
   

    @api.depends('first_name','last_name')
    def _get_student_name(self):
        for student in self:
            student.name = (student.first_name or '') + ' ' + (student.last_name or '')

    first_name = fields.Char('First Name', required=True, track_visibility='onchange')
    last_name = fields.Char('Last Name', track_visibility='onchange')
    father_name = fields.Char(string="Father Name", track_visibility='onchange')
    cnic = fields.Char('CNIC', size=15, track_visibility='onchange')
    cnic_expiry_date = fields.Date('CNIC Expiry Date')
    passport_expiry_date = fields.Date('Passport Expiry Date',track_visibility='onchange')
    passport_no = fields.Char('Passport Number',track_visibility='onchange')
    passport_issue_date = fields.Date("Passport Issue Date")
    u_id_no = fields.Char("U.I.D")
    visa_issue_date = fields.Date("Visa Issue Date")
    visa_expiry_date = fields.Date('Visa Expiry Date',track_visibility='onchange')
    domicile_id = fields.Many2one('odoocms.domicile','Domicile',track_visibility='onchange')
    
    date_of_birth = fields.Date('Birth Date', required=True, track_visibility='onchange',
        default=lambda self: self.compute_previous_year_date(fields.Date.context_today(self)))
    gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], 'Gender', required=True, track_visibility='onchange')
    marital_status = fields.Many2one('odoocms.marital.status','Marital Status',track_visibility='onchange')
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group', track_visibility='onchange')
    religion_id = fields.Many2one('odoocms.religion', string="Religion", track_visibility='onchange')
    nationality = fields.Many2one('res.country', string='Nationality', ondelete='restrict', track_visibility='onchange')
    nationality_name = fields.Char(related = 'nationality.name', store = True)
    
    admission_no = fields.Char(string="Admission Number", readonly=True)
    id_number = fields.Char('Student ID', size=64, track_visibility='onchange')
    entryID = fields.Char('Entry ID', size=64, track_visibility='onchange')
    code = fields.Char(compute='_get_code',store=True, track_visibility='onchange')
    
    emergency_contact = fields.Char('Emergency Contact', track_visibility='onchange')
    emergency_mobile = fields.Char('Emergency Mobile', track_visibility='onchange')
    emergency_email = fields.Char('Emergency Email', track_visibility='onchange')
    emergency_address = fields.Char('Em. Address', track_visibility='onchange')
    emergency_city = fields.Char('Em. Street', track_visibility='onchange')
    
    visa_info = fields.Char('Visa Info', size=64)
    company_id = fields.Many2one('res.company', string='Company')
    
    is_same_address = fields.Boolean(string="Is same Address?", track_visibility='onchange')
    per_street = fields.Char()
    per_street2 = fields.Char()
    per_city = fields.Char()
    per_zip = fields.Char(change_default=True)
    per_state_id = fields.Many2one("res.country.state", string='Per State', ondelete='restrict',
        domain="[('country_id', '=?', per_country_id)]")
    per_country_id = fields.Many2one('res.country', string='Per. Country', ondelete='restrict')

    tag_ids = fields.Many2many('odoocms.student.tag', 'student_tag_rel','student_id', 'tag_id', string='Tag')
    
    partner_id = fields.Many2one('res.partner', 'Partner', required=True, ondelete="cascade")

    career_id = fields.Many2one('odoocms.career','Career', readonly=True, states={'draft': [('readonly', False)]})
    program_id = fields.Many2one('odoocms.program','Academic Program', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]})
    institute_id = fields.Many2one('odoocms.institute', 'Institute', required=True)
    #campus_id = fields.Many2one('odoocms.campus','Campus',related='institute_id.campus_id',store=True)
    study_scheme_id = fields.Many2one('odoocms.study.scheme','Study Scheme',compute='_get_study_scheme',store=True)
    academic_semester_id = fields.Many2one('odoocms.academic.term','Current Academic Term', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]})
    academic_session_id = fields.Many2one('odoocms.academic.session','Academic Session', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]})
    academic_ids = fields.One2many('odoocms.student.academic', 'student_id', 'Academics')
    stream_id = fields.Many2one('odoocms.program.stream','Stream')
    semester_id = fields.Many2one('odoocms.semester', 'Semester')

    new_id_number = fields.Char('New Student ID', size=64)

    award_ids = fields.One2many('odoocms.award', 'student_id', 'Honor/Awards')
    publication_ids = fields.One2many('odoocms.publication', 'student_id', 'Publications')

    language_ids = fields.Many2many('odoocms.language', string='Languages')

    extra_activity_ids = fields.One2many('odoocms.extra.activity', 'student_id', 'Activites')
    
    state = fields.Selection([
            ('draft', 'Draft'), ('enroll', 'Enroll'), ('elumni', 'Elumni'), ('cancel', 'Cancel'), ('suspend', 'Suspend'),('struck', 'Struck Off'), ('freezed', 'Freezed'),
        ], 'Status', default='draft', track_visibility='onchange')

    import_identifier = fields.Many2one('ir.model.data', 'Import Identifier', compute='_get_import_identifier',
        store=True)
    
    _sql_constraints = [
        ('admission_no', 'unique(admission_no)', "Another Student already exists with this Admission number!"),
    ]

    def name_get(self):
        res = []
        for record in self:
            name = record.code + ' - ' + record.name
            res.append((record.id, name))
        return res
    
    @api.depends('id_number','entryID')
    def _get_code(self):
        for rec in self:
            rec.code = rec.id_number or rec.entryID or ('ST.'+str(rec.id))
        
    def get_student_id(self):
        if self.batch_id and self.batch_id.sequence_id:
            self.id_number = self.batch_id.sequence_id.next_by_id()
        
    # @api.depends('program_id')
    # def _get_study_scheme(self):
    #     for rec in self:
    #         if rec.program_id:
    #             study_schemes = self.env['odoocms.study.scheme'].search(
    #                 [('academic_session_id', '=', rec.academic_session_id.id)])
    #             # , ('program_ids', 'in', rec.program_id.ids)
    #             for study_scheme in study_schemes:
    #                 if rec.program_id.id in study_scheme.program_ids.ids:
    #                     rec.study_scheme_id = study_scheme.id
    #                     break
    #
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search([('name', operator, name)] + (args or []), limit=limit)
            if not recs:
                recs = self.search([('code', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super(OdooCMSStudent, self).name_search(name, args=args, operator=operator, limit=limit)

    @api.model
    def create(self, vals):
        if vals.get('first_name',False) or vals.get('last_name',False):
            name = vals.get('first_name','')
            if vals.get('last_name',''):
                name = name + ' ' + vals.get('last_name','')
            vals['name'] =  name
        
        res = super(OdooCMSStudent, self).create(vals)
        _logger.info('Student Create with id %s', res.id)
        return res


    def write(self, vals):
        if vals.get('first_name', False) or vals.get('last_name', False):
            vals['name'] = vals.get('first_name', self.first_name or '') + ' ' + vals.get('last_name', self.last_name or '')
        
        res = super(OdooCMSStudent, self).write(vals)
        return res


    @api.constrains('cnic')
    def _check_cnic(self):
        for rec in self:
            if rec.cnic:
                cnic_com = re.compile('^[0-9+]{5}-[0-9+]{7}-[0-9]{1}$')
                a = cnic_com.search(rec.cnic)
                if a:
                    return True
                else:
                    raise UserError(_("CNIC Format is Incorrect. Format Should like this 00000-0000000-0"))
        return True
        

    @api.constrains('date_of_birth')
    def _check_birthdate(self):
        for record in self:
            if record.date_of_birth > fields.Date.today():
                raise ValidationError(_("Birth Date can't be greater than Current Date!"))

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Students'),
            'template': '/odoocms/static/xls/odoocms_student.xlsx'
        }]


    def create_user(self):
        group_portal = self.env.ref('base.group_portal')
        for record in self:
            if not record.user_id:
                data = {
                    #'name': record.name + ' ' + (record.last_name or ''),
                    'partner_id': record.partner_id.id,
                    'login': record.id_number or record.entryID or record.email,
                    'password': record.mobile or '654321',
                    'groups_id': group_portal,
                }
                user = self.env['res.users'].create(data)
                record.user_id = user.id
    
    def compute_previous_year_date(self, strdate):
        tenyears = relativedelta(years=16)
        start_date = fields.Date.from_string(strdate)
        return fields.Date.to_string(start_date - tenyears)


    @api.depends('code')
    def _get_import_identifier(self):
        for rec in self:
            identifier = self.env['ir.model.data'].search(
                [('model', '=', 'odoocms.student'), ('res_id', '=', rec.id)])
            if identifier:
                identifier.module = 'ST'
                identifier.name = rec.code or rec.id
            else:
                data = {
                    'name': rec.code or rec.id,
                    'module': 'ST',
                    'model': 'odoocms.student',
                    'res_id': rec.id,
                }
                identifier = self.env['ir.model.data'].create(data)

            rec.import_identifier = identifier.id
    

    def lock(self):
        for rec in self:
            if rec.batch_id:
                rec.state = 'enroll'
            else:
                raise UserError('Please Assign Batch to Student.')
                
    def cron_account(self):
        recs = self.env['res.partner'].search(['|', ('property_account_receivable_id', '=', False), ('property_account_payable_id', '=', False)])
        for rec in recs:
            rec.property_account_receivable_id = 3
            rec.property_account_payable_id = 229

    def cron_pass(self):
        for rec in self:
            if rec.mobile:
                rec.mobile = rec.mobile.replace('-', '')
                if rec.user_id:
                    rec.user_id.password = rec.mobile
    
    # def cron_reg(self):
    #     for rec in self.env['odoocms.assesment.obe.summary'].search([('registration_id','=',False)]):
    #         reg = self.env['odoocms.student.subject'].search([('student_id','=',rec.student_id.id),])
    #         rec.registration_id = rec.id


    def process_images(self):
        # source = "ftp/files/"
        source = self.env['ir.config_parameter'].sudo().get_param('odoocms.ftp_server_source')
        destination = "/tmp/"
        self.downloadFiles(source, destination)
        os.chdir(destination + source)
        image_list = os.listdir()
        students = self.env['odoocms.student'].search([])
        for img in image_list:
            for rec in students:
                if rec.id_number and rec.id_number == os.path.splitext(img)[0]:
                    pic = open(destination + source + img, 'rb')
                    pic_binary = pic.read()
                    pic_binary2 = bytearray(pic_binary)
                    if pic_binary:
                        rec.image = codecs.encode(pic_binary, 'base64')
                        # pic_binary2 = base64.b64encode(pic.read())
                        # pic_binary2 = pic_binary.decode('base64')

    def downloadFiles(self, path, destination):
        # server = "127.0.0.1"
        # user = "testftp"
        # password = "123"

        server = self.env['ir.config_parameter'].sudo().get_param('odoocms.ftp_server_address')
        user = self.env['ir.config_parameter'].sudo().get_param('odoocms.ftp_server_user')
        password = self.env['ir.config_parameter'].sudo().get_param('odoocms.ftp_server_password')

        interval = 0.05
    
        ftp = ftplib.FTP(server)
        ftp.login(user, password)
    
        try:
            ftp.cwd(path)
            os.chdir(destination)
            self.mkdir_p(destination[0:len(destination)] + path)
            print("Created: " + destination[0:len(destination)] + path)
        except OSError:
            pass
        except ftplib.error_perm:
            print("Error: could not change to " + path)
            sys.exit("Ending Application")
    
        filelist = ftp.nlst()
    
        for file in filelist:
            time.sleep(interval)
            try:
                ftp.cwd(path + file + "/")
                self.downloadFiles(path + file + "/", destination[0:len(destination)] + path)
            except ftplib.error_perm:
                os.chdir(destination[0:len(destination)])
            
                try:
                    ftp.retrbinary("RETR " + file, open(os.path.join(destination[0:len(destination)] + path, file), "wb").write)
                    print("Downloaded: " + file)
                except:
                    print("Error: File could not be downloaded " + file)
        return

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if os.path.isdir(path):
                pass
            else:
                raise


class OdooCMSStudentAcademic(models.Model):
    _name = 'odoocms.student.academic'
    _description = 'Student Academics'
    
    degree_level = fields.Selection([('matric', 'Matric'),('o-level', 'O-Level'),('dae', 'DAE'), ('inter', 'Intermediate'),('a-level', 'A-Level')], 'Degree Level', required=1)
    degree = fields.Char('Degree', required=1)
    year = fields.Char('Passing Year')
    board = fields.Char('Board Name')
    subjects = fields.Char('Subjects')
    total_marks = fields.Integer('Total Marks', required=1)
    obtained_marks = fields.Integer('Obtained Marks', required=1)
    student_id = fields.Many2one('odoocms.student', 'Student')
    
        
class OdooCmsStChangeStateRule(models.Model):
    _name = 'odoocms.student.change.state.rule'
    _description = "Reason for Changing Student State"

    name = fields.Text(string='Reason', help='Define the Reason To Change the State of Student')


class OdooCmsStudentProfileAttribute(models.Model):
    _name = 'odoocms.student.profilechange.attribute'
    _description = "Attributes Allowed for Student Profile Change"

    name = fields.Char('Name')
    field_name_id = fields.Many2one('ir.model.fields', 'Change Allowed In', required= True)


class OdooCMSStudentComment(models.Model):
    _name = 'odoocms.student.comment'
    _description = 'Student Comment'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'student_id'

    student_id = fields.Many2one('odoocms.student', 'Student', required=True)
    name = fields.Char(string = 'Student Name', related = 'student_id.name', readonly=True, store = True)
    message_from = fields.Char(string='Message From', readonly=True)
    program_id = fields.Many2one('odoocms.program', string = 'Program', related = 'student_id.program_id', readonly=True, store = True)
    comment = fields.Html(string="Comment", required=True)

    date = fields.Date('Comment Date', default=date.today(), readonly=1)
    notfication_date = fields.Date('Notification Date', default=date.today())
    message_ref = fields.Char(string="Reference Number", required=True)

    cms_ref = fields.Char(string="CMS Reference Number", required=True)

