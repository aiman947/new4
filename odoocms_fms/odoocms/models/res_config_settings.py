import pdb
import calendar
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # module_odoocms_activity = fields.Boolean(string="Activity")
    # module_odoocms_facility = fields.Boolean(string="Facility")
    # module_odoocms_parent = fields.Boolean(string="Parent")
    # module_odoocms_assignment = fields.Boolean(string="Assignment")
    # module_odoocms_classroom = fields.Boolean(string="Classroom")
    module_odoocms_fee = fields.Boolean(string="Fee")
    module_odoocms_admission = fields.Boolean(string="Admission")
    module_odoocms_timetable = fields.Boolean(string="Timetable")
    # module_odoocms_exam = fields.Boolean(string="Exam")
    # module_odoocms_library = fields.Boolean(string="Library")
    # module_odoocms_attendance = fields.Boolean(string="Attendance")

    pdf_converter = fields.Char(string="PDF Converter", config_parameter='odoocms.pdf_converter', default='/usr/bin/unoconv')
    
    repeat_grades_allowed = fields.Char(string="Re-register Grades Allowed",config_parameter='odoocms.repeat_grades_allowed', default='F')
    repeat_grades_allowed_time = fields.Char(string="Re-Register Time-gap Allowed", config_parameter='odoocms.repeat_grades_allowed_time', default='3')
    x_st_repeat_grades_allowed_time = fields.Char(string="Re-Register Time-gap Allowed for X-final", config_parameter='odoocms.x_st_repeat_grades_allowed_time', default='2')

    repeat_grades_allowed_no = fields.Char(string="Re-Register Times Allowed", config_parameter='odoocms.repeat_grades_allowed_no', default='1')
    
    failed_grades = fields.Char(string="Failed Grades", config_parameter='odoocms.failed_grades', default='F,W')

    current_academic_semester = fields.Many2one('odoocms.academic.term', config_parameter='odoocms.current_academic_semester',
                                                string="Current Academic Term", help="Add Current Academic Semester")


    #FTP Server details
    ftp_server_address = fields.Char(string="FTP Server Address", config_parameter='odoocms.ftp_server_address')
    ftp_server_user = fields.Char(string="FTP Server User", config_parameter='odoocms.ftp_server_user')
    ftp_server_password = fields.Char(string="FTP Server Password", config_parameter='odoocms.ftp_server_password')
    ftp_server_source = fields.Char(string="Files Path", config_parameter='odoocms.pdf_converter', default = 'ftp/files/')
