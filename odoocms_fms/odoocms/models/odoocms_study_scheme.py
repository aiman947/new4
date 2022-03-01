import pdb
import calendar
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)


class OdooCMSStudyScheme(models.Model):
    _name = "odoocms.study.scheme"
    _description = "CMS Study Scheme"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence'
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', copy=False)
    sequence = fields.Integer('Sequence')
    scheme_date = fields.Date(string="Scheme Date")
    active = fields.Boolean('Active', default=True,
                            help="If Unchecked, it will allow you to hide the Study Scheme without removing it.")
    credit_hours = fields.Integer('Credit Hours')
    career_id = fields.Many2one("odoocms.career", string="Career", required=True)
    institute_id = fields.Many2one("odoocms.institute", string="Institute")

    program_ids = fields.Many2many('odoocms.program','scheme_program_rel','scheme_id','program_id',string='Program', copy=True)
   # here
    batch_id = fields.Many2many('odoocms.batch','scheme_batch_rel','scheme_id','batch_id',string='Batches', copy=True)
    line_ids = fields.One2many('odoocms.study.scheme.line','study_scheme_id',string='Study Scheme', copy=True)
    stream_ids = fields.Many2many('odoocms.program.stream','scheme_stream_rel','scheme_id','stream_id',string='Streams', copy=True)
    scheme_type = fields.Selection([('regular', 'Regular'), ('special', 'Special')], 'Scheme Type', default='regular')
    _sql_constraints = [
        ('code', 'unique(code)', "Code already exists for another Study Scheme"),
    ]

    
class OdooCMSStudySchemeLine(models.Model):
    _name = 'odoocms.study.scheme.line'
    _description = 'CMS Study Scheme Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'course_id'
    _order = 'semester_id'

    study_scheme_id = fields.Many2one('odoocms.study.scheme', string="Study Scheme", ondelete='restrict')
    semester_id = fields.Many2one('odoocms.semester', string="Semester", track_visibility='onchange')
    course_type = fields.Selection([
        ('compulsory','Compulsory'),
        ('elective','Elective'),
        ('gen_elective', 'General Elective'),
        ('placeholder','Elective Placeholder')
    ], 'Course Type',default='compulsory', track_visibility='onchange')
    course_type_id = fields.Many2one('odoocms.course.type', 'Course Type', track_visibility='onchange')
    term_id = fields.Many2one('odoocms.academic.term',string="Term", track_visibility='onchange')
    course_id = fields.Many2one('odoocms.course',string='Course', required=True, track_visibility='onchange')
    
    course_code = fields.Char('Course Code', track_visibility='onchange')
    course_name = fields.Char('Course Name', track_visibility='onchange')

    component_lines = fields.One2many('odoocms.study.scheme.line.component', 'scheme_line_id', string='Course Components', track_visibility='onchange')
    prereq_ids = fields.Many2many('odoocms.course','scheme_prereq_subject_rel','scheme_line_id','subject_id', string='Prerequisite Courses',copy=False)
    coreq_course = fields.Many2one('odoocms.study.scheme.line','CO-Req Course', track_visibility='onchange')
    # coreq_subject_id = fields.Many2one('odoocms.subject','Co-Req Subject', track_visibility='onchange')
    # # import_identifier = fields.Many2one('ir.model.data', 'Import Identifier', compute='_get_import_identifier', store=True) #

    _sql_constraints = [
        ('unique_course', 'unique(study_scheme_id,course_id)', "Course already exists in Study Scheme"), ]

    def name_get(self):
        res = []
        for record in self:
            name = record.course_id.name
            if record.course_id.code:
                name = record.course_id.code + ' - ' + name
            res.append((record.id, name))
        return res
    
    @api.onchange('course_id')
    def onchagene_course(self):
        course = self.course_id
        components = [[5]]
        for component in course.component_lines:
            components.append((0, 0, {
                'component': component.component,
                'weightage': component.weightage,
                'contact_hours': component.contact_hours,
            }))
        self.component_lines = components
        self.prereq_ids = [(6,0,course.prereq_ids.mapped('prereq_id').ids)]
        if course.coreq_course:
            coreq_course = self.study_scheme_id.line_ids.filtered(lambda l: l.course_id.id == course.coreq_course.id).id
            if "NewId" in str(coreq_course):
                coreq_course = coreq_course.origin
            self.coreq_course = coreq_course
            
        self.course_code = course.code
        self.course_name = course.name

    # @api.onchange('course_type','course_type_id')
    # def onchagene_course_type(self):
    #     if self.course_type == 'placeholder':
    #         sub_domain = [('course_type','=','placeholder'),('course_type_id','=',self.course_type_id.id)]
    #     else:
    #         sub_domain = [('course_type', '!=', 'placeholder'),('course_type_id','=',self.course_type_id.id)]
    #
    #     return {
    #         'domain': {
    #             'course_id': sub_domain
    #         },
    #         'value': {
    #             'course_id': False,
    #         }
    #     }

    # @api.multi
    # @api.depends('study_scheme_id','subject_id','academic_semester_id')
    # def _get_import_identifier(self):
    #     for rec in self:
    #         name = (rec.study_scheme_id.code or '') + '-' + (rec.academic_semester_id.code and rec.academic_semester_id.code or str(rec.semester_id.number)) + '-' + (rec.subject_id.code or '')
    #         identifier = self.env['ir.model.data'].search(
    #             [('model', '=', 'odoocms.study.scheme.line'), ('res_id', '=', rec.id)])
    #
    #         if identifier:
    #             identifier.module = 'PR'
    #             identifier.name = name
    #         else:
    #             data = {
    #                 'name': name,
    #                 'module': 'SS',
    #                 'model': 'odoocms.study.scheme.line',
    #                 'res_id': rec.id,
    #             }
    #             identifier = self.env['ir.model.data'].create(data)
    #
    #         rec.import_identifier = identifier.id
    
    @api.model
    def create(self, vals):
        if vals.get('elective', False):
            vals['semester_id'] = False
        return super(OdooCMSStudySchemeLine, self).create(vals)
        

    # def write(self, vals):
    #     if vals.get('elective',False):
    #         vals['semester_id'] = False
    #     ret = super(OdooCMSStudySchemeLine,self).write(vals)
    #     # prereq = vals.get('prereq_course',False)
    #     # if prereq:
    #     #     self.course_id.prereq_course = True
    #     # else:
    #     #     scheme_subs = self.env['odoocms.study.scheme.line'].search([('course_id','=',self.course_id.id)])
    #     #     if scheme_subs and len(scheme_subs) == 1:
    #     #         self.course_id.prereq_course = False
    #     return ret


class OdooCMSStudySchemeLineComponent(models.Model):
    _name = 'odoocms.study.scheme.line.component'
    _description = 'CMS Scheme Line Component'
    
    scheme_line_id = fields.Many2one('odoocms.study.scheme.line')
    component = fields.Selection([
        ('lab', 'Lab'),
        ('lecture', 'Lecture'),
        ('studio', 'Studio'),
    ], string='Component')
    weightage = fields.Float(string='Credit Hours', default=3.0, help="Weightage for this Course", track_visibility='onchange')
    contact_hours = fields.Float(string='Contact Hours', default=1.0, help="Contact Hours for this Course", track_visibility='onchange')


