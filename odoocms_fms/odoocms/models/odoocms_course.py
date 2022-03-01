import pdb
import calendar
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)


class OdooCMSProgramStream(models.Model):
    _name = 'odoocms.program.stream'
    _description = 'Program Stream'
    
    name = fields.Char(string='Name', required=True, help="Stream Name")
    code = fields.Char(string="Code", required=True, help="Stream Code")
    
    
class OdooCMSCourseType(models.Model):
    _name = 'odoocms.course.type'
    _description = 'Course Type'

    name = fields.Char(string='Name', required=True, help="Course Type Name")
    code = fields.Char(string="Code", required=True, help="Course Type Code")
    # type = fields.Selection([
    #     ('core', 'Core'),
    #     ('elective', 'Elective'),
    # ], 'Type', default='core')
    # # scheme_line_ids = fields.One2many('odoocms.study.scheme.line','course_type_id','Courses')
    # stream = fields.Boolean('Stream')
    # # scheme_line_ids = fields.One2many('odoocms.study.scheme', 'line_ids', string="Scheme Line Ids",
    # #                                   track_visibility='onchange')


class OdooCMSCourse(models.Model):
    _name = 'odoocms.course'
    _description = 'CMS Course'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, help="Course Name", track_visibility='onchange')
    code = fields.Char(string="Code", required=True, help="Course Code", track_visibility='onchange')
    effective_date = fields.Date(string='Effective Date', help='Effective Date of Course')
    active = fields.Boolean('Active', default=True,
                            help="Current Status of Course")
    description = fields.Text(string='Description', help="Description about the Course")
    formal_description = fields.Text(string='Formal Description', help="Formal Description about the Course")
    career_id = fields.Many2one('odoocms.career', 'Career')
    # type = fields.Selection([
    #     ('earned', 'Earned'),
    #     ('additional', 'Additional'),
    #     ('minor', 'Minor'),
    #     ('major', 'Major'),
    #     ('graded', 'Graded'),
    #     ('notgraded', 'NotGraded'),
    # ], string='Type', default="earned", help="Choose the type of the Course", track_visibility='onchange')

    prereq_course = fields.Boolean('Prerequisite Course', default=False, help="Prerequisite Course")
    prereq_ids = fields.One2many('odoocms.course.prereq', 'course_id', string='PreRequisits', track_visibility='onchange')
    equivalent_ids = fields.One2many('odoocms.course.equivalent', 'course_id', string='Course Equivalent', track_visibility='onchange')
    component_lines = fields.One2many('odoocms.course.component', 'course_id', string='Course Components', track_visibility='onchange')
    coreq_course = fields.Many2one('odoocms.course', 'Co-Requisite', track_visibility='onchange')
    subject_type_id = fields.Many2one('odoocms.course.type', 'Subject Type', track_visibility='onchange')
    
    outline = fields.Html('Outline')
    suggested_books = fields.Text('Suggested Books')
    stream_id = fields.Many2one('odoocms.program.stream', 'Stream', track_visibility='onchange')

    _sql_constraints = [
        ('code', 'unique(code, name)', "Another Course already exists with this Code & Name!"), ]

    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.code:
                name = record.code + ' - ' + name
            res.append((record.id, name))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search([('name', operator, name)] + (args or []), limit=limit)
            if not recs:
                recs = self.search([('code', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super(OdooCMSCourse, self).name_search(name, args=args, operator=operator, limit=limit)


    # @api.model
    # def get_import_templates(self):
    #     return [{
    #         'label': _('Import Template for Courses'),
    #         'template': '/odoocms/static/xls/odoocms_subject.xls'
    #     }]

class OdooCMSCourseComponent(models.Model):
    _name = 'odoocms.course.component'
    _description = 'CMS Course Component'

    course_id = fields.Many2one('odoocms.course')
    component = fields.Selection([
        ('lab', 'Lab'),
        ('lecture', 'Lecture'),
        ('studio', 'Studio'),
    ], string='Component')
    weightage = fields.Float(string='Credit Hours', default=3.0, help="Weightage for this Course", track_visibility='onchange')
    contact_hours = fields.Float(string='Contact Hours', default=1.0, help="Contact Hours for this Course", track_visibility='onchange')
    
    # @api.constrains('weightage', 'lab', 'lecture')
    # def check_weightage(self):
    #     for rec in self:
    #         if rec.weightage <= 0:
    #             raise ValidationError(_('Weightage must be Positive'))
    #         if rec.lecture < 0:
    #             raise ValidationError(_('Contact Hours must be Zero or Positive'))
    #         if rec.lab < 0:
    #             raise ValidationError(_('Lab Hours must be Zero or Positive'))
  
    
class OdooCMSCoursePreReq(models.Model):
    _name = 'odoocms.course.prereq'
    _description = 'CMS Course PreRequist'
    
    course_id = fields.Many2one('odoocms.course', string='Course')
    prereq_id = fields.Many2one('odoocms.course', string='PreRequist')
    effective_date = fields.Date(string='Effective Date', help='Effective Date of PreRequist')


class OdooCMSCourseEquivalent(models.Model):
    _name = 'odoocms.course.equivalent'
    _description = 'CMS Course Equivalent'
    
    course_id = fields.Many2one('odoocms.course', string='Course')
    equivalent_id = fields.Many2one('odoocms.course', string='Equivalent')
    effective_date = fields.Date(string='Effective Date', help='Effective Date of Equivalent')