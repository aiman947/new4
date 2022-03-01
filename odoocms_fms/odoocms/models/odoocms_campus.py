
from odoo import fields, models, api, _
import pdb


# class OdooCMSFaculty(models.Model):
#     _name = 'odoocms.faculty'
#     _description = 'CMS Faculty'
#     _inherit = ['mail.thread','mail.activity.mixin']
#
#     name = fields.Char(string="Faculty", help="Faculty Name")
#     code = fields.Char(string="Code", help="Faculty Code")
#     department_id = fields.Many2one('odoocms.department',string='Departments')
#
#     _sql_constraints = [
#         ('code', 'unique(code)', "Code already exists "),]


class OdooCMSDiscipline(models.Model):
    _name = 'odoocms.discipline'
    _description = 'CMS Discipline'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Discipline", help="Discipline Name")
    code = fields.Char(string="Code", help="Discipline Code")
    description = fields.Text(string='Description', help="Short Description about the Discipline")
    program_ids = fields.One2many('odoocms.program','discipline_id','Academic Programs')
    
    _sql_constraints = [
        ('code', 'unique(code)', "Code already exists "),
    ]


class OdooCMSCampus(models.Model):
    _name = 'odoocms.campus'
    _description = 'CMS Campus'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', help='Campus City Code')
    effective_date = fields.Date(string='Effective Date', help='Effective Date of Campus')
    active = fields.Boolean('Active', default=True,
                            help="Current Status of Course")
    description = fields.Text(string='Description', help="Description about the Campus")
    short_description = fields.Text(string='Short Description', help="Short Description about the Campus")
    formal_description = fields.Text(string='Formal Description', help="Formal Description about the Campus")
    street = fields.Char(string='Address 1')
    street2 = fields.Char(string='Address 2')
    zip = fields.Char(change_default=True)
    city = fields.Char('City')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    company_id = fields.Many2one('res.company', string='Company')
    institute_ids = fields.One2many('odoocms.institute', 'campus_id', string='Institutes')

    _sql_constraints = [
        ('code', 'unique(code)', "Campus Code already exists."),
    ]


class OdooCMSInstitute(models.Model):
    _name = 'odoocms.institute'
    _description = 'CMS Institute'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', help='Institute City Code')
    effective_date = fields.Date(string='Effective Date', help='Effective Date of Institute')
    active = fields.Boolean('Active', default=True, help="Current Status of Institute")
    website = fields.Char(string='Website')
    phone = fields.Char(string='Phone')

    department_ids = fields.One2many('odoocms.department', 'institute_id', string='Departments')
    campus_id = fields.Many2one('odoocms.campus', string='Campus')

    parent_id = fields.Many2one('odoocms.institute', string='Parent Institute')
    parent_name = fields.Char(related='parent_id.name', readonly=True, string='Parent name')
    child_ids = fields.One2many('odoocms.institute', 'parent_id', string='SubInstitutes',
        domain=[('active', '=', True)])
    

class OdooCMSDepartment(models.Model):
    _name = 'odoocms.department'
    _description = 'CMS Department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Name", help="Department Name", required=True)
    code = fields.Char(string="Code", help="Department Code", required=True)
    effective_date = fields.Date(string="Effective Date", help="Effective Date", required=True)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean('Active', default=True,
                            help="Current Status of Department")
    
    program_ids = fields.One2many('odoocms.program', 'department_id', string="Programs")
    faculty_ids = fields.One2many('odoocms.department.line', 'department_id', string="Faculty")
    
    institute_id = fields.Many2one("odoocms.institute", string="Institute")
    hod_id = fields.Many2one("hr.employee", string="HOD")
    
    _sql_constraints = [
        ('code', 'unique(code)', "Department Code already exists."), ]

    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.code:
                name = record.code + ' - ' + name
            res.append((record.id, name))
        return res


class OdooCMSDepartmentLineTag(models.Model):
    _name = 'odoocms.department.line.tag'
    _description = 'Department Line Tag'

    name = fields.Char(string="Faculty Tag", required=True)
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
    
    
class OdooCMSDepartmentLine(models.Model):
    _name = 'odoocms.department.line'
    _description = 'CMS Department Line'
    
    department_id = fields.Many2one('odoocms.department',string='Department')
    employee_id = fields.Many2one('hr.employee',string='Employee')
    employee_name = fields.Char(related = 'employee_id.name', store=True,string='Employee Name')
    employee_work_phone = fields.Char(related = 'employee_id.work_phone', store=True,string='Work Phone')
    employee_work_email = fields.Char(related = 'employee_id.work_email', store=True,string='Work Email')
    employee_department_id = fields.Many2one(related = 'employee_id.department_id', store=True,string='Department')
    employee_job_id = fields.Many2one(related = 'employee_id.job_id', store=True,string='Job Position')
    employee_parent_id = fields.Many2one(related = 'employee_id.parent_id', store=True,string='Manager')
    employee_tag_id = fields.Many2many('odoocms.department.line.tag','department_line_tag_rel','department_line_id','tag_id','Tags')
    
    
class OdooCMSCareer(models.Model):
    _name = "odoocms.career"
    _description = "CMS Career"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description  = fields.Text(string='Description')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search([('name', operator, name)] + (args or []), limit=limit)
            if not recs:
                recs = self.search([('code', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super(OdooCMSCareer, self).name_search(name, args=args, operator=operator, limit=limit)


class OdooCMSProgram(models.Model):
    _name = "odoocms.program"
    _description = "CMS Program"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    short_code = fields.Char('Short Code',size=4)
    color = fields.Integer(string='Color Index')
    duration = fields.Char('Duration')
    credit_hours = fields.Integer('Credit Hours')
    effective_date = fields.Date(string="Effective Date", help="Effective Date", required=True)
    description = fields.Text(string='Formal Description')
    active = fields.Boolean('Active', default=True,
                            help="Current Status of Department")
    department_id = fields.Many2one('odoocms.department', string="Department")
    career_id = fields.Many2one('odoocms.career', string="Career")
    discipline_id = fields.Many2one('odoocms.discipline', string="Discipline")

    # scheme_ids = fields.Many2many('odoocms.study.scheme', 'scheme_program_rel', 'program_id', 'scheme_id',
    #     string='Study Schemes')
    specialization_ids = fields.One2many('odoocms.specialization', 'program_id', string='Specializations')
    user_ids = fields.Many2many('res.users', 'program_user_access_rel', 'program_id', 'user_id', 'Users', domain="[('share','=', False)]")

    #     import_identifier = fields.Many2one('ir.model.data', 'Import Identifier', compute='_get_import_identifier',
#         store=True)
#
    _sql_constraints = [
        ('code', 'unique(code)', "Code already exists "),
    ]

    # def name_get(self):
    #     res = []
    #     for record in self:
    #         name = record.name
    #         if record.department_id:
    #             name = name + ' - ' + record.department_id.campus_id.code
    #         res.append((record.id, name))
    #     return res
#
#     @api.model
#     def name_search(self, name, args=None, operator='ilike', limit=100):
#         if name:
#             recs = self.search([('name', operator, name)] + (args or []), limit=limit)
#             if not recs:
#                 recs = self.search([('code', operator, name)] + (args or []), limit=limit)
#             return recs.name_get()
#         return super(OdooCMSProgram, self).name_search(name, args=args, operator=operator, limit=limit)
#
#
#     @api.depends('code')
#     def _get_import_identifier(self):
#         for rec in self:
#             name = rec.code or rec.id
#             identifier = self.env['ir.model.data'].search(
#                 [('model', '=', 'odoocms.program'), ('res_id', '=', rec.id)])
#
#             if identifier:
#                 identifier.module = 'PR'
#                 identifier.name = name
#             else:
#                 data = {
#                     'name': name,
#                     'module': 'PR',
#                     'model': 'odoocms.program',
#                     'res_id': rec.id,
#                 }
#                 identifier = self.env['ir.model.data'].create(data)
#
#             rec.import_identifier = identifier.id


class OdooCMSSpecialization(models.Model):
    _name = "odoocms.specialization"
    _description = "CMS Specialization"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description  = fields.Text(string='Formal Description')
    program_id = fields.Many2one('odoocms.program', string='Program')


class OdooCMSBatch(models.Model):
    _name = "odoocms.batch"
    _description = "Program Batches"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    sequence = fields.Integer('Sequence')


class ResUsers(models.Model):
    _inherit = "res.users"

    program_ids = fields.Many2many('odoocms.program', 'program_user_access_rel', 'user_id', 'program_id', 'Programs')

    def create_user(self, records, user_group=None):
        for rec in records:
            if not rec.user_id:
                user_vals = {
                    'name': rec.name,
                    'login': rec.email or rec.name,
                    'partner_id': rec.partner_id.id,
                    'password': rec.mobile or '123456',
                    'groups_id': user_group,
                }
                user_id = self.create(user_vals)
                rec.user_id = user_id
                # if user_group:
                #    user_group.users = user_group.users + user_id

