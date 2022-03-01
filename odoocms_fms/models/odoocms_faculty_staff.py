# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
import pdb
import re


class OdooCMSLanguage(models.Model):
    _name = 'odoocms.language'
    _description = "OdooCMS Languages"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char('Name')
    code = fields.Char('Code')
    sequence = fields.Integer(string='Sequence')


class OdooCMSDesignation(models.Model):
    _name = 'odoocms.designation'
    _description = 'HR Designation Setup'
    _rec_name = 'hr_desig_short_desc'

    code = fields.Char(string='Code')
    faculty_type = fields.Selection([('FM', 'Faculty Member'),
                                     ('HOD', 'Head of Department')],
                                    string='Faculty Type', default='FM', track_visibility='onchange')
    hr_desig_short_desc = fields.Char(string="Short Description")
    hr_desig_long_desc = fields.Char(string="Long Description")
    hr_desg_type = fields.Selection(
        [('faculty', 'FACULTY'), ('support staff', 'SUPPORT STAFF'), ('other', 'OTHER')],
        string='Post Type', required=True, default='faculty', track_visibility='onchange')
    hr_desg_status = fields.Selection(
        [('active', 'ACTIVE'), ('inactive', 'INACTIVE')],
        string='Post Status', required=True, default='active', track_visibility='onchange')


# Passport DB Table
class OdooCMSPassport(models.Model):
    _name = 'odoocms.passport'
    _description = 'Faculty Passport'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', string='Faculty ID')
    passport_no = fields.Char(string="PASSPORT.NO")
    date_issue = fields.Date(string="DATE OF ISSUE")
    date_expiry = fields.Date(string="VALID UPTO")
    booklet_no = fields.Char(string="BOOKLET NO")
    country_id = fields.Many2one('res.country', string='PASSPORT(COUNTRY)', )
    issue_body = fields.Many2one('res.country', string='ISSUING(COUNTRY)', )


# Scholarship/Membership DB Table
class OdooCMSScholarship(models.Model):
    _name = 'odoocms.scholarships'
    _description = 'Faculty Scholarships'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', string='Faculty ID')
    type = fields.Selection([
        ('fellowship', 'FELLOWSHIP'),
        ('membership', 'MEMBERSHIP'),
        ('scholarship', 'SCHOLARSHIP')], string='SCHOLARSHIP', required=True, default='fellowship',
        track_visibility='onchange')
    award_body = fields.Selection([
        ('nust', 'NUST'), ('other', 'OTHER')], string='AWARDING BODY', required=True, default='nust',
        track_visibility='onchange')
    date_from = fields.Date(string="DATE FROM")
    date_to = fields.Date(string="DATE TO")
    description = fields.Text(string="DESCRIPTION")
    obligation = fields.Boolean(string="OBLIGATION")

    @api.constrains('date_from', 'date_to')
    def validate_date(self):
        for rec in self:
            start_date = fields.Date.to_string(rec.date_from)
            end_date = fields.Date.to_string(rec.date_to)
            if start_date > end_date:
                raise ValidationError(_('"DATE TO" MUST BE GREATER > "DATE FROM'))


class odooCMSAwards(models.Model):
    _name = 'odoocms.awards'
    _description = 'Faculty Honor/Awards'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    type = fields.Selection([('award', 'AWARD'), ('honor', 'HONOR')],
                            string='HONOR/AWARD TYPE', required=True, default='award', track_visibility='onchange')

    nomination = fields.Selection([('nust', 'NUST'), ('other', 'OTHER')],
                                  string='NOMINATED BY', required=True, default='nust', track_visibility='onchange')

    status = fields.Selection([('awarded', 'AWARDED'), ('not awarded', 'NOT AWARDED')],
                              string='STATUS', required=True, default='awarded', track_visibility='onchange')

    awarding_body = fields.Selection([('nust', 'NUST'), ('other', 'OTHER')],
                                     string='AWARDING BODY', required=True, default='nust', track_visibility='onchange')

    name = fields.Char(string="NAME")
    country_id = fields.Many2one('res.country', string='COUNTRY')
    date = fields.Date(string="DATE OF AWARD")
    description = fields.Text(string="DESCRIPTION")


# Next of Kin DB Table
class OdooCMSNextofkin(models.Model):
    _name = 'odoocms.nextofkin'
    _description = 'Faculty Next of Kin'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    name = fields.Char(string="NAME")
    relationship = fields.Selection(
        [('FA', 'Father'), ('M', 'Mother'), ('B', 'Brother'), ('S', 'Son'), ('D', 'Daughter'), ('SI', 'Sister'),
         ('SP', 'Spouse'),
         ('GF', 'Grandfather'), ('GM', 'Grandmother'), ('GD', 'Granddaughter'), ('GS', 'Grandson'),
         ('GM', 'Grandmother'), ('ES', 'Ex-Spouse'),
         ('SF', 'Step-Father'), ('SM', 'Step-Mother'), ('SD', 'Step-Daughter'), ('SS', 'Step-Son'),
         ('R', 'Other Relative'), ('SL', 'Self'),
         ('E', 'Employee'), ('ER', 'Employer'), ('FR', 'Friend'), ('LM', 'Loan Co-Maker'), ('LR', 'Loan Reference'),
         ('LS', 'Loan Co-Signer'),
         ('N', 'Neighbor'), ('PA', 'Partner'), ('RO', 'Roommate'), ('WF', 'Works For'), ('NI', 'None Indicated'),
         ('O', 'Other')], string="RELATIONSHIP")
    description = fields.Char(string="DESCRIPTION")
    cnic = fields.Char(string="CNIC NO", size=15)
    contact_no = fields.Char(string="CONTACT NO")
    address_id = fields.Char(string="ADDRESS")
    percentage = fields.Integer(string="%AGE OF SHARE")
    islamic_law = fields.Boolean(string="As Per Islamic Law")

    @api.constrains('cnic')
    def check_nok_cnic(self):
        for rec in self:
            if self.cnic and not re.match("\d{5}-\d{7}-\d{1}", str(rec.cnic)):
                raise ValidationError(_('Invalid CNIC Pattern..!! "99999-9999999-9"'
                                        ' Next Of Kin CNIC Must Contain Numeric Value [0-9]'))


# Training/Courses DB Table
class OdooCMSTraining(models.Model):
    _name = 'odoocms.training'
    _description = 'Faculty Training'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    type = fields.Char(string="TYPE")
    name = fields.Char(string="TRAINING/WORKSHOP")
    date_from = fields.Date(string="DURATION(FROM)")
    date_to = fields.Date(string="DURATION(TO)")
    center = fields.Char(string="CENTER")
    org_body = fields.Char(string="ORG BODY")
    sponsor_body = fields.Char(string="SPONSOR BODY")
    organized_by = fields.Selection([('nust', 'NUST'), ('other', 'OTHER')],
                                    string='ORGANIZED BY', required=True, default='nust', track_visibility='onchange')
    sponsor_by = fields.Selection([('nust', 'NUST'), ('other', 'OTHER')],
                                  string='SPONSORED BY', required=True, default='nust', track_visibility='onchange')

    @api.constrains('date_from', 'date_to')
    def validate_date(self):
        for rec in self:
            start_date = fields.Date.to_string(rec.date_from)
            end_date = fields.Date.to_string(rec.date_to)
            if start_date > end_date:
                raise ValidationError(_('"DURATION(TO)"   MUST BE GREATER >  "DURATION(FROM)'))


# Collaboration Table
class OdooCMSCollaborations(models.Model):
    _name = 'odoocms.collaborations'
    _description = 'Faculty Collaborations'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID4')
    coll_type = fields.Text(string="COLLABORATION TYPE/DETAIL")
    date_from = fields.Date(string="DURATION(FROM)")
    date_to = fields.Date(string="DURATION(TO)")
    organization = fields.Char(string="ORGANIZATION")
    country_id = fields.Many2one('res.country', 'COUNTRY')
    status = fields.Selection([('completed', 'COMPLETED'), ('in-progress', 'IN-PROGRESS')],
                              string='STATUS', required=True, default='completed', track_visibility='onchange')

    @api.constrains('date_from', 'date_to')
    def validate_date(self):
        for rec in self:
            start_date = fields.Date.to_string(rec.date_from)
            end_date = fields.Date.to_string(rec.date_to)
            if start_date > end_date:
                raise ValidationError(_('"DURATION(TO)"  MUST BE GREATER >  "DURATION(FROM)'))


# Experience DB Table
class OdooCMSExperience(models.Model):
    _name = 'odoocms.experience'
    _description = 'Faculty Experience'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID5')
    experience_type = fields.Selection(
        [('Professional', 'PROFESSIONAL'), ('research', 'RESEARCH'), ('Teaching', 'TEACHING'),
         ('Industry', 'INDUSTRY')],
        string='TYPE', required=True, default='Professional', track_visibility='onchange')
    designation = fields.Char(string="DESIGNATION")
    org_name = fields.Char(string="ORG NAME")
    org_address = fields.Char(string="ORG ADDRESS")
    date_from = fields.Date(string="DURATION(FROM)")
    date_to = fields.Date(string="DURATION(TO)")
    job_description = fields.Char(string="JOB DESCRIPTION")
    reason = fields.Char(string="REASON FOR LEAVING")
    miltray = fields.Selection(
        [('no', 'NO'), ('yes', 'YES')],
        string='MILTARY JOB EXPERIENCE', required=True, default='no', track_visibility='onchange')
    ref_name = fields.Char(string="NAME")
    ref_designation = fields.Char(string="DESIGNATION REFERENCE")
    fmn_unit_dept = fields.Char(string="FMN/Unit/Dept #")
    co_hod_name = fields.Char(string="Name of CO/HOD")
    experience_duration = fields.Char(string='Experience Duration',
                                      compute='_compute_experience_duration',
                                      readonly=True, store=True,
                                      help="Employee Age")
    ref_mobile = fields.Char(string="MOBILE")
    ref_landline = fields.Char(string="LAND LINE NO (With Ext")
    ref_email = fields.Char(string="EMAIL")
    confirmation = fields.Boolean(width=100,
                                  string="I solemnly affirm that the forgoing information given is true, complete and correct to the best of my knowledge and belief")

    @api.depends('date_from', 'date_to')
    def _compute_experience_duration(self):
        for record in self:
            experience = ''
            if record.date_from and record.date_to:
                experience = record.faculty_staff_id.calculate_year_month_mask(record.date_from, record.date_to)
            record.experience_duration = experience

    @api.constrains('date_from', 'date_to')
    def validate_date(self):
        for rec in self:
            start_date = fields.Date.to_string(rec.date_from)
            end_date = fields.Date.to_string(rec.date_to)
            if start_date > end_date:
                raise ValidationError(_('"DURATION(TO)"   MUST BE GREATER >  "DURATION(FROM)'))


# Professional/Qualification DB Table
class OdooCMSProfQualification(models.Model):
    _name = 'odoocms.profqualification'
    _description = 'Faculty Professional Qualificaation'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID6')
    fms_profqualification_cert = fields.Char(string="QUALIFICATION/CERTIFICATION")
    fms_profqualification_status = fields.Selection(
        [('completed', 'COMPLETED'), ('in-progress', 'IN-PROGRESS')],
        string='STATUS', required=True, default='completed', track_visibility='onchange')
    fms_profqualification_inst = fields.Char(string="INSTITUTION")
    fms_profqualification_country = fields.Many2one('res.country', string="COUNTRY")
    fms_profqualification_dt_from = fields.Date(string="DURATION(FROM)")
    fms_profqualification_dt_to = fields.Date(string="DURATION(TO)")
    fms_profqualification_div = fields.Char(string="DIVISION/%AGE/CGPA")
    fms_profqualification_miltary = fields.Boolean(string="IS MILITARY COURSE")
    confirmation = fields.Boolean(
        string="I solemnly affirm that the forgoing information given is true, complete and correct to the best of my knowledge and belief")

    @api.constrains('fms_profqualification_dt_from', 'fms_profqualification_dt_to')
    def validate_date(self):
        for rec in self:
            start_date = fields.Date.to_string(rec.fms_profqualification_dt_from)
            end_date = fields.Date.to_string(rec.fms_profqualification_dt_to)
            if start_date > end_date:
                raise ValidationError(_('"DURATION(TO)"   MUST BE GREATER >  "DURATION(FROM)'))


# Courses Taught DB Table
class OdooCMSCoursesTaught(models.Model):
    _name = 'odoocms.coursetaught'
    _description = 'Faculty Courses Taught'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    term_id = fields.Many2one('odoocms.academic.term', string="TERM")
    course_id = fields.Many2one('odoocms.course', string="COURSE ID")


# Project DB Table
class OdooCMSFacultyProjects(models.Model):
    _name = 'odoocms.faculty.projects'
    _description = 'Faculty Projects'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    project_type = fields.Selection(
        [('consultancy', 'CONSULTANCY'), ('proposed', 'PROPOSED'), ('under-taken', 'UNDER-TAKEN'), ('other', 'OTHER')],
        string='TYPE', required=True, default='consultancy', track_visibility='onchange')
    status = fields.Selection(
        [('completed', 'COMPLETED'), ('granted', 'GRANTED'), ('on-going', 'ON-GOING'), ('submitted', 'SUBMITTED')],
        string='STATUS', required=True, default='completed', track_visibility='onchange')
    remun = fields.Char(string="REMUNERATION AS PI")
    remun_amount = fields.Float(string="AMOUNT OF PROJECT")
    agency = fields.Selection(
        [('nust', 'NUST'), ('other', 'OTHER')],
        string='FUNDING AGENCY', required=True, default='nust', track_visibility='onchange')
    date_from = fields.Date(string="DURATION(FROM)")
    date_to = fields.Date(string="DURATION(TO)")
    url = fields.Char(string="URL(PROJECT WEBSITE)")
    position = fields.Selection(
        [('co-pi', 'CO-PI'), ('pi', 'PI')],
        string='POSITION', required=True, default='co-pi', track_visibility='onchange')
    remun_co = fields.Char(string="REMUNERATION AS CO-PI")
    grant = fields.Selection(
        [('yes', 'YES'), ('no', 'NO')],
        string='FUNDED/GRANTED', required=True, default='yes', track_visibility='onchange')
    grant_amount = fields.Float(string="FUNDED AMOUNT")
    transfer_amount = fields.Boolean(string="AMOUNT TRANSFERRED IN NUST ACCOUNT")

    @api.constrains('date_from', 'date_to')
    def validate_date(self):
        for rec in self:
            start_date = fields.Date.to_string(rec.date_from)
            end_date = fields.Date.to_string(rec.date_to)
            if start_date > end_date:
                raise ValidationError(_('"DURATION(TO)"   MUST BE GREATER >  "DURATION(FROM)'))


# Family DB Table
class OdooCMSFamily(models.Model):
    _name = 'odoocms.family'
    _description = 'Faculty Family'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    name = fields.Char(string="NAME")
    dob = fields.Date(string="DATE OF BIRTH")
    dom = fields.Date(string="DATE OF MARRIAGE")
    nationality_p = fields.Many2one('res.country', 'NATIONALITY(P)')
    nationality_s = fields.Many2one('res.country', 'NATIONALITY(S)')
    marriage_place = fields.Char(string="PLACE OF MARRIAGE")
    cnic = fields.Char(string="CNIC", size=15)
    designation = fields.Char(string="DESIGNATION")
    employer_name = fields.Char(string="EMPLOYER NAME")
    profession = fields.Selection([('agriculture', 'AGRICULTURE'),
                                   ('air force', 'AIR FORCE'),
                                   ('banker', 'BANKER'),
                                   ('businessman', 'BUSINESSMAN'),
                                   ('govt servant', 'GOVT SERVANT'),
                                   ('house wife', 'HOUSE WIFE'),
                                   ('navy', 'NAVY'),
                                   ('private service', 'PRIVATE SERVICE'),
                                   ('army', 'ARMY'),
                                   ('other', 'OTHER')],
                                  string='PROFESSION', required=True, default='agriculture',
                                  track_visibility='onchange')
    status = fields.Selection([('deceased', 'DECEASED'),
                               ('retired', 'RETIRED'),
                               ('serving', 'SERVING'),
                               ('other', 'OTHER')],
                              string='STATUS', required=True, default='serving', track_visibility='onchange')
    family_employer = fields.Selection(
        [('nust', 'NUST'), ('other', 'OTHER')],
        string='EMPLOYER', required=True, default='nust', track_visibility='onchange')

    @api.constrains('cnic')
    def check_fcnic(self):
        for rec in self:
            if self.cnic and not re.match("\d{5}-\d{7}-\d{1}", rec.cnic):
                raise ValidationError(_('Invalid CNIC Pattern..!! "99999-9999999-9"'
                                        ' EMPLOYEE FAMILY CNIC Must Contain Numeric Value [0-9]'))


# Defence Employee DB Table
class OdooCMSDefence(models.Model):
    _name = 'odoocms.defence'
    _description = 'Faculty Defence Employee'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    service_id = fields.Many2one('odoocms.hr.forces', 'SERVICE')
    rank = fields.Many2one('odoocms.hr.ranks', 'RANKS')
    arm = fields.Many2one('odoocms.hr.arm', 'ARM/CORP/BRANCH')
    service_no = fields.Char(string="SERVICE NUMBER")
    doc = fields.Date(string="DoC")
    served_to = fields.Date(string="SERVED TO")
    emp_status = fields.Selection(
        [('R', 'RETIRED'), ('S', 'SERVING')],
        string='EMPLOYEE STATUS', required=True, default='S', track_visibility='onchange')
    course = fields.Char(string="COURSE (e:g 113PMALC)")
    remarks = fields.Text(string="REMARKS")


# Defence Skills DB Table
class OdooCMSSkill(models.Model):
    _name = 'odoocms.skill'
    _description = 'Faculty Skills'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    skill_type = fields.Selection([('A', 'ABILITIES'),
                                   ('E', 'EXPERTIES'),
                                   ('S', 'SKILLS'),
                                   ('SP', 'SPECIALIZATION')],
                                  string='SKILL TYPE', required=True, default='A', track_visibility='onchange')
    description = fields.Char(string="DESCRIPTION")


# Prof Registration DB Table
class OdooCMSProgReg(models.Model):
    _name = 'odoocms.prof.reg'
    _description = 'Faculty Professional Registration'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    reg_body = fields.Char(string="REGISTRATION BODY")
    reg_no = fields.Char(string="REGISTRATION NO")
    reg_date = fields.Date(string="REGISTRATION DATE")
    reg_validity = fields.Date(string="VALID UPTO")

    @api.constrains('reg_date', 'reg_validity')
    def validate_date(self):
        for rec in self:
            start_date = fields.Date.to_string(rec.reg_date)
            end_date = fields.Date.to_string(rec.reg_validity)
            if start_date > end_date:
                raise ValidationError(_('"VALID UPTO DATE"   MUST BE GREATER >THEN  "REGISTRATION DATE'))


# HEC Supervised Students DB Table
class OdooCMSHEC(models.Model):
    _name = 'odoocms.hec'
    _description = 'Faculty HEC Supervised Student'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    status = fields.Selection([('A', 'APPLIED'),
                               ('AP', 'APPROVED'),
                               ('NA', 'NOT APPROVED'),
                               ('NAA', 'NOT APPLIED')],
                              string='CURRENT STATUS', required=True, default='A', track_visibility='onchange')
    curr_status_date = fields.Date(string="DATE OF CURRENT STATUS")
    valid_till_date = fields.Date(string="VALID TILL")
    remarks = fields.Text(string="REMARKS")


class OdooCMSAcademic(models.Model):
    _name = 'odoocms.academic'
    _description = 'Faculty Academic'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    fms_acad_qualification = fields.Many2one('odoocms.hr.qualification', 'QUALIFICATION')
    fms_acad_uni = fields.Many2one('odoocms.hr.university', 'UNIVERSITY/BOARD')
    fms_acad_country = fields.Many2one('res.country', 'COUNTRY')
    fms_acad_degree = fields.Char(string="DEGREE NAME")
    fms_acad_degree_duration = fields.Char(string="DEGREE DURATION")
    fms_acad_special = fields.Char(string="SPECIALIZATION")
    fms_acad_total_perc = fields.Char(string="TOTAL MARKS/CGPA%AGE")
    fms_acad_obt_perc = fields.Char(string="OBTAINED MARKS/CGPA%AGE")
    fms_acad_dur_from = fields.Date(string="DURATION FROM")
    fms_acad_dur_to = fields.Date(string="DURATION TO")
    fms_acad_deg_status = fields.Selection([('C', 'COMPLETED'),
                                            ('I', 'IN PROGRESS')],
                                           string='DEGREE STATUS', required=True, default='C',
                                           track_visibility='onchange')
    fms_acad_deg_ver = fields.Selection([('Y', 'YES'),
                                         ('N', 'NO')],
                                        string='VERIFIED', required=True, default='Y',
                                        track_visibility='onchange')
    fms_acad_deg_cat = fields.Many2one('odoocms.acad.category', 'CATEGORY')
    fms_attachment = fields.Binary(string="ATTACHMENT")
    fms_attachment_filename = fields.Char(string="FILE NAME")
    confirmation = fields.Boolean(
        string="I solemnly affirm that the forgoing information given is true, complete and correct to the best of my knowledge and belief")

    @api.constrains('fms_acad_dur_from', 'fms_acad_dur_to')
    def validate_date(self):
        for rec in self:
            start_date = fields.Date.to_string(rec.fms_acad_dur_from)
            end_date = fields.Date.to_string(rec.fms_acad_dur_to)
            if start_date > end_date:
                raise ValidationError(_('"DURATION TO"   MUST BE GREATER >THEN  "DURATION FROM'))


class OdooCMSChild(models.Model):
    _name = 'odoocms.children'
    _description = 'Faculty/Spouse Children'

    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    name = fields.Char(string="NAME")
    birth_place = fields.Char(string="PLACE OF BIRTH")
    disability_type = fields.Char(string="CHILD DISABILITY TYPE")
    disablity_desc = fields.Text(SIZE=1000, string="DISABILITY DESCRIPTION")
    birth_date = fields.Date(string="DATE OF BIRTH")
    age = fields.Integer(string="AGE(Yrs)")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string='GENDER', required=True, default='male', track_visibility='onchange')
    status = fields.Selection([('married', 'MARRIED'),
                               ('divorced', 'DIVORCED'),
                               ('widow', 'WIDOW'),
                               ('seperated', 'SEPERATED'),
                               ('single', 'SINGLE')],
                              string='STATUS', required=True, default='married', track_visibility='onchange')

    @api.constrains('birth_date')
    def validate_date(self):
        for rec in self:
            pob_date_issue = fields.Date.from_string(rec.birth_date)
            if pob_date_issue > fields.Date.today():
                raise ValidationError(_('Entered Date Cannot be Greater> than Today Date:'))


class OdooCMSFacultyStaff(models.Model):
    _name = 'odoocms.faculty.staffnew'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char('name', readonly=True, store=True)
    first_name = fields.Char(string="first name")
    # first_name = fields.Char(string="first name")
    contact_address = fields.Char(string="first name")

    last_name = fields.Char(string="last name")
    code = fields.Char( readonly=True, store=True)
    father_name = fields.Char('name', readonly=True, store=True)
    # tag_ids = fields.Many2one('odoocms.faculty.staff', 'tag ID')
    tag_ids = fields.Selection([('urdu', 'Urdu'),
                               ('english', 'English'),
                               ('math', 'Math'),
                               ('science', 'Science')],
                              string='tag', required=True, default='urdu', track_visibility='onchange')
    nationality = fields.Many2one('res.country', 'nationality')
    date_of_birth = fields.Date(string="DATE OF BIRTH")
    language_ids = fields.Many2one('odoocms.language', ' language ')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string='GENDER', required=True, default='male', track_visibility='onchange')

    linkedin_fms = fields.Char(string="LINKEDIN")
    father_address = fields.Char(string="ADDRESS(RES)")
    skype_fms = fields.Char(string="SKYPE ID")
    image_1920 = fields.Binary('image 1920', readonly=True, store=True)

    nust_campus_fms = fields.Selection([('yes', 'YES'),
                                        ('no', 'NO')],
                                       string='CAMPUS RESIDENT', default='yes', track_visibility='onchange')
    domocile_fms = fields.Selection([('punjab', 'Punjab'),
                                     ('sindh', 'Sindh'),
                                     ('kpk', 'Khyber Pakhtunkhwa'),
                                     ('cap', 'Capital'),
                                     ('gilgit', 'Gilgit Baltistan'),
                                     ('ajk', 'Azad Jamu Kashmir'),
                                     ('jk', 'Jamu Kashmir'),
                                     ('bal', 'Balochistan')],
                                    string='DOMICILE', default='punjab', track_visibility='onchange')
    cnic_no_fms = fields.Char(string="CNIC", size=15)
    # blood_group = fields.Char(string="CNIC", size=15)
    emergency_contact = fields.Char(string="CNIC", size=15)
    mobile_phone = fields.Char(string="mobile", size=15)
    phone = fields.Char(string="phone", size=15)

    employee_id = fields.Many2one('hr.employee', ' employee ')
    user_id = fields.Many2one('res.users', ' User ')
    work_email = fields.Char(string="CNIC", size=15)
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group', track_visibility='onchange')

    religion = fields.Selection([('muslim', 'MUSLIM'),
                                 ('ahmadi', 'AHMADI'),
                                 ('budhist', 'BUDHIST'),
                                 ('christian', 'CHRISTIAN'),
                                 ('catholic', 'CATHOLIC'),
                                 ('hindu', 'HINDU'),
                                 ('jewish', 'JEWISH'),
                                 ('other', 'OTHER')],
                                string='RELIGION', default='muslim', track_visibility='onchange')
    sect_fms = fields.Selection([('sunni', 'SUNNI'),
                                 ('shias', 'SHIAS'),
                                 ('ismailis', 'ISMAILIS')],
                                string='SECT', default='sunni', track_visibility='onchange')
    nust_campus_fms = fields.Selection([('yes', 'YES'),
                                        ('no', 'NO')],
                                       string='CAMPUS RESIDENT', default='yes', track_visibility='onchange')
    twitter_fms = fields.Char(string="TWITTER")
    profile_fms = fields.Char(string="PROFILE(BREIF)")
    facebook_fms = fields.Char(string="FACEBOOK")
    google_fms = fields.Char(string="GOOGLE SCHOLAR")
    father_name = fields.Char(string="NAME")
    father_cnic = fields.Char(string="FATHER's CNIC", size=15)
    father_status = fields.Selection([('deceased', 'DECEASED'),
                                      ('retired', 'RETIRED'),
                                      ('serving', 'SERVING')],
                                     string='STATUS', default='serving', track_visibility='onchange')
    agree_status_fms = fields.Boolean(string="STATUS OF COMPLETION OF DATA")
    father_profession = fields.Selection([('agriculture', 'AGRICULTURE'),
                                          ('air force', 'AIR FORCE'),
                                          ('banker', 'BANKER'),
                                          ('businessman', 'BUSINESSMAN'),
                                          ('govt servant', 'GOVT SERVANT'),
                                          ('navy', 'NAVY'),
                                          ('private service', 'PRIVATE SERVICE'),
                                          ('army', 'ARMY'),
                                          ('other', 'OTHER')],
                                         string='PROFESSION', default='agriculture', track_visibility='onchange')
    # classify_id = fields.One2many('odoocms.class.faculty', 'slas_id')
    test_id = fields.One2many('odoocms.test', 'testing_id')
    extra_activity_ids = fields.One2many('extra.activities', 'categ_id')


class OdooCMSAcadCategory(models.Model):

    _name = 'odoocms.class.faculty'
    _description = 'HR Academic Category'

    name = fields.Char(string='Category')
    slas_id = fields.Many2one('odoocms.faculty.staffnew', 'Faculty ID')
    term_id = fields.Many2one('odoocms.academic.term', 'Faculty ID')
    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    # count = fields.Float(string='count')
    student_count = fields.Char(string='student')


class OdooCMStest(models.Model):

    _name = 'odoocms.test'
    _description = 'HR Academic Category'

    name = fields.Char(string='Category')
    testing_id = fields.Many2one('odoocms.faculty.staffnew', 'Faculty ID')
    paper_attachment = fields.Binary(string='Paper')
    date = fields.Date(string="DATE")
    topic = fields.Char(string='Topic')


class OdooCMSactivities(models.Model):

    _name = 'extra.activities'
    _description = 'HR Academic Category'

    name = fields.Char(string='Name')
    categ_id = fields.Many2one('odoocms.faculty.staffnew', 'Faculty ID')
    remarks = fields.Html(string='Remarks')
    date = fields.Date(string="DATE")




# class OdooCMSFacultyStaff(models.Model):
#
#     # _name  = 'odoocms.faculty.staff'
#     _inherit = 'odoocms.faculty.staff'
#
#
#     # Replacing to Update String
#     employee_id = fields.Many2one('hr.employee', 'Linked Employee', required=True, ondelete="cascade")
#     # Fetching Information From Hr Employee to FMS
#     # marital_status = fields.Selection('Marriage Status', related='employee_id.marital', readonly=True, store=True)
#     birthday = fields.Date('Date of Birth',  readonly=True, store=True)
#     # related = 'employee_id.birthday',
#     mobile_phone = fields.Char('Mobile (Primary)', readonly=True, store=True)
#     name = fields.Char('name', readonly=True, store=True)
#
#     # related = 'employee_id.mobile_phone',
#     phone = fields.Char('Mobile (Secondary)',  readonly=True, store=True)
#     # related = 'employee_id.phone',
#     work_phone = fields.Char('Land Line (Res)',readonly=True, store=True)
#     # related = 'employee_id.work_phone',
#     work_email = fields.Char('Email (Official)',  readonly=True, store=True)
#     # related = 'employee_id.work_email',
#     private_email = fields.Char('Email', readonly=True, store=True)
#     # related = 'employee_id.private_email',
#     work_location = fields.Char('University Mailing Address', readonly=True, store=True)
#     # related = 'employee_id.work_location',
#     emergency_contact = fields.Char('Emergency Contact',  readonly=True, store=True)
#     # related = 'employee_id.emergency_contact',
#     emergency_phone = fields.Char('Emergency Phone',  readonly=True, store=True)
#     # related = 'employee_id.emergency_phone',
#     # ----------------------------------------------------
#     partner_id = fields.Many2one('res.partner', 'Partner',
#                                  required=False, ondelete="cascade")
#     institute = fields.Many2one('odoocms.institute', 'INSTITUTE',
#                                 readonly=True, store=True, track_visibility='onchange')
#     # compute = '_compute_institute',
#     designation = fields.Many2one('odoocms.designation', 'DESIG',
#                                    readonly=True,
#                                   store=True, track_visibility='onchange')
#     # compute = '_compute_designation',
#     ebps = fields.Many2one('odoocms.hr.scale', 'EBPS',
#                         compute='_compute_ebps', readonly=True,
#                         store=True, track_visibility='onchange')
#     hr_emp_pay_pkg_type = fields.Selection([('L', 'LUMPSUM'), ('B', 'BPS')],
#                                 string='Pay Package Type',
#                                 readonly=True, store=True, track_visibility='onchange',
#                                 help="Employee Pay Package type")
#     # compute = '_compute_hr_emp_pay_pkg_type',
#
#
#     hr_emp_project = fields.Selection([('H','HHFP'),('I','IPSP'),('U','USPCASE')],
#                                 string='Projects', compute='_compute_project',
#                                 readonly=True, store=True, track_visibility='onchange',
#                                 help="Employee Project")
#
#     department = fields.Many2one('odoocms.department', 'DEPARTMENT',
#                                  compute='_compute_department',
#                                  readonly=True, store=True, track_visibility='onchange')
#     #ik
#     fms_acad_qualification = fields.Many2one('odoocms.hr.qualification', 'QUALIFICATION',
#                                  readonly=True, store=True, track_visibility='onchange')
#
#     employed_from = fields.Date('EMPLOYED FROM', compute='_compute_employment_date',
#                                 readonly=True, store=True, track_visibility='onchange')
#     employee_status = fields.Selection([('A', 'ACTIVE'),
#                                         ('I', 'IN ACTIVE')], string='Employee State', compute='_compute_activity_status',
#                                 readonly=True, store=True, track_visibility='onchange')
#     employee_category = fields.Selection([('F', 'FACULTY'), ('S', 'SUPPORT STAFF')],
#                                 string='Employee Category', compute='_compute_category',
#                                 readonly=True, store=True, track_visibility='onchange')
#     hr_emp_action_type = fields.Selection([('ABS','ABSENT'), ('ADJ','ADJUSTMENT'),
#                      ('ATT','ATTACHMENT'), ('OPC','BONDED TO OPEN CONTRACT'),
#                      ('D','DEATH'), ('DEM','DEMOTION'), ('DEC','DISC. ON EXPIRY OF CONTRACT'),
#                      ('DTC','DISC. ON TENURE OF COMPLETION'), ('BFL','RESUMPTION / REJOIN AFTER LEAVE'),
#                      ('DA','DISCONTINUATION ON AGE'), ('DIS','DISCONTINUED'),
#                      ('DML','DISMISSAL'), ('EXP','EXPIRED'),
#                      ('NEJ','NEW JOINING'), ('LPR','LEAVE PRIOR TO RETIREMENT'),
#                      ('OTB','OPEN CONTRACT TO BONDED'), ('PPR','PAY PACKAGE REVISION'),
#                      ('PIN','POSTED IN'), ('OUT','POSTED OUT'),
#                      ('PRD','POSTING / ADJUSTMENT'), ('PRO','PROMOTION'),
#                      ('PHS','PROMOTION TO HIGHER STATUS'), ('RED','REDESIGNATION / ADJUSTMENT'),
#                      ('REM','RE-EMPLOYMENT'), ('RES','RESIGNED'),
#                      ('RFA','RETURN FROM ATTACHMENT'), ('RFS','REMOVAL FROM SERVICE'),
#                      ('RIN','REINSTATMENT'), ('RTD','RETIREMENT'),
#                      ('SPC','STATUS & PAY PACKAGE CONVERSION'), ('SPS','SPS'),
#                      ('TER','TERMINATION'), ('TNR','TENURED'),
#                      ('TNT','TTS 2nd TERM'), ('TRA','TRANSFER'),
#                      ('TTT','TRANSFER TO TTS'), ('UPS','UPGRADATION OF PAY SCALE'), ('WOL','WENT ON LEAVE')],
#                     string='Employee Action Type', compute='_compute_hr_emp_action_type',
#                     readonly=True, store=True, track_visibility='onchange',
#                     help="Employee Action Type")
#     hr_emp_type = fields.Selection([('C', 'CONTRACT'), ('R', 'REGULAR')],
#                                 string='Employee Type', compute='_compute_hr_emp_type',
#                                 readonly=True, store=True, track_visibility='onchange',
#                                 help="Employee Type")
#     emp_age = fields.Char(string='Age',
#                                 readonly=True, store=True, track_visibility='onchange',
#                                 help="Employee Age")
#     # compute = '_compute_employee_age',
#     confirmation = fields.Boolean(width=100,
#                    string="I solemnly affirm that the forgoing information given is true, complete and correct to the best of my knowledge and belief")
#       # Master Table PK Fields Detail
#
#     # scholarship_ids = fields.One2many('odoocms.scholarships', 'faculty_staff_id')
#     # award_ids = fields.One2many('odoocms.awards', 'faculty_staff_id')
#     # nok_ids = fields.One2many('odoocms.nextofkin', 'faculty_staff_id')
#     # training_ids = fields.One2many('odoocms.training', 'faculty_staff_id')
#     # collaboration_ids = fields.One2many('odoocms.collaborations', 'faculty_staff_id')
#     # experience_ids = fields.One2many('odoocms.experience', 'faculty_staff_id')
#     # profqualification_ids = fields.One2many('odoocms.profqualification', 'faculty_staff_id')
#     # project_ids = fields.One2many('odoocms.faculty.projects', 'faculty_staff_id')
#     # family_ids = fields.One2many('odoocms.family', 'faculty_staff_id')
#     # family_children_ids = fields.One2many('odoocms.children', 'faculty_staff_id')
#     # course_ids = fields.One2many('odoocms.coursetaught', 'faculty_staff_id')
#     # defence_ids = fields.One2many('odoocms.defence', 'faculty_staff_id')
#     # skill_ids = fields.One2many('odoocms.skill', 'faculty_staff_id')
#     # fms_prof_reg_ids = fields.One2many('odoocms.prof.reg', 'faculty_staff_id')
#     # fms_hec_ids = fields.One2many('odoocms.hec', 'faculty_staff_id')
#     # fms_academic_ids = fields.One2many('odoocms.academic', 'faculty_staff_id')
#     # passport_ids = fields.One2many('odoocms.passport', 'faculty_staff_id')
#     # probations_ids = fields.One2many('odoocms.hr.emp.probation', 'faculty_staff_id')
#     # #######################################################################
#     # master_ids = fields.One2many('odoocms.hr.emp.rec.master', 'faculty_staff_id')
#     # ##############################################################################
#     # additional_duties = fields.One2many('odoocms.hr.emp.add.duty', 'faculty_staff_id')
#     # additional_duty = fields.Many2one('odoocms.designation', 'ADDITIONAL DUTY',
#     #                               compute='_compute_additional_duty', readonly=True,
#     #                               store=True, track_visibility='onchange')
#     # contract_renewal_ids = fields.One2many('odoocms.hr.emp.contract.renew', 'faculty_staff_id')
#     # visit_abroad_ids = fields.One2many('odoocms.hr.emp.visit.abroad', 'faculty_staff_id')
#     # fin_incentive_ids = fields.One2many('odoocms.hr.emp.fin.inc', 'faculty_staff_id')
#     # discipline_ids = fields.One2many('odoocms.hr.emp.discipline', 'faculty_staff_id')
#     #---------------------------------------------------------------------
#     # Add By AARSOL
#     master_cnt = fields.Integer('Master Count', compute='_count_master')
#     renew_cnt = fields.Integer('Renew Count', compute='_count_master_contract_renew')
#     va_cnt = fields.Integer('VA Count', compute='_count_master_va')
#     probation_cnt = fields.Integer('Probation Count', compute='_count_master_probation')
#     incentive_cnt = fields.Integer('Incentive Count', compute='_count_master_fin_incentive')
#     add_duty_cnt = fields.Integer('Add. Duty Count', compute='_count_master_add_duty')
#     discipline_cnt = fields.Integer('Discipline Count', compute='_count_master_discipline')
#     cnic_no_fms = fields.Char(string="CNIC", size=15)
#     domocile_fms = fields.Selection([('punjab', 'Punjab'),
#                                      ('sindh', 'Sindh'),
#                                      ('kpk', 'Khyber Pakhtunkhwa'),
#                                      ('cap', 'Capital'),
#                                      ('gilgit', 'Gilgit Baltistan'),
#                                      ('ajk', 'Azad Jamu Kashmir'),
#                                      ('jk', 'Jamu Kashmir'),
#                                      ('bal', 'Balochistan')],
#     string='DOMICILE', default='punjab', track_visibility='onchange')
#     nust_campus_fms = fields.Selection([('yes', 'YES'),
#                                         ('no', 'NO')],
#                                        string='CAMPUS RESIDENT', default='yes', track_visibility='onchange')
#     skype_fms = fields.Char(string="SKYPE ID")
#     email_fms = fields.Char(string="EMAIL")
#     landline_office = fields.Char(string='LANDLINE (OFFICE)',
#                                   help="Land line number Office with extension")
#     email_off_fms = fields.Char(string="EMAIL(OFFICE)")
#     uni_mail_addr_fms = fields.Char(string="UNI MAIL ADDRESS")
#     profile_fms = fields.Char(string="PROFILE(BREIF)")
#     linkedin_fms = fields.Char(string="LINKEDIN")
#     twitter_fms = fields.Char(string="TWITTER")
#     facebook_fms = fields.Char(string="FACEBOOK")
#     google_fms = fields.Char(string="GOOGLE SCHOLAR")
#     # -----Father Information
#     father_name = fields.Char(string="NAME")
#     father_cnic = fields.Char(string="FATHER's CNIC", size=15)
#     father_address = fields.Char(string="ADDRESS(RES)")
#     father_profession = fields.Selection([('agriculture', 'AGRICULTURE'),
#                                        ('air force', 'AIR FORCE'),
#                                        ('banker', 'BANKER'),
#                                        ('businessman', 'BUSINESSMAN'),
#                                        ('govt servant', 'GOVT SERVANT'),
#                                        ('navy', 'NAVY'),
#                                        ('private service', 'PRIVATE SERVICE'),
#                                        ('army', 'ARMY'),
#                                        ('other', 'OTHER')],
#                                       string='PROFESSION',  default='agriculture', track_visibility='onchange')
#     father_status = fields.Selection([('deceased', 'DECEASED'),
#                                           ('retired', 'RETIRED'),
#                                           ('serving', 'SERVING')],
#     string='STATUS', default='serving', track_visibility='onchange')
#     agree_status_fms = fields.Boolean(string="STATUS OF COMPLETION OF DATA")
#     religion = fields.Selection([('muslim', 'MUSLIM'),
#                                      ('ahmadi', 'AHMADI'),
#                                      ('budhist', 'BUDHIST'),
#                                      ('christian', 'CHRISTIAN'),
#                                      ('catholic', 'CATHOLIC'),
#                                      ('hindu', 'HINDU'),
#                                      ('jewish', 'JEWISH'),
#                                      ('other', 'OTHER')],
#                                     string='RELIGION', default='muslim', track_visibility='onchange')
#     sect_fms = fields.Selection([('sunni', 'SUNNI'),
#                                  ('shias', 'SHIAS'),
#                                  ('ismailis', 'ISMAILIS')],
#                                 string='SECT', default='sunni', track_visibility='onchange')
#     login = fields.Char('Login', related='partner_id.user_id.login', readonly=1, store=True)
#     last_login = fields.Datetime('Latest Connection', readonly=1, related='partner_id.user_id.login_date')
#
#     def name_get(self):
#         res = []
#         for record in self:
#             name = record.name
#             if record.code:
#                 name += ' - ' + record.code
#             if record.institute:
#                 name += ' - ' + record.institute.code or ''
#             res.append((record.id, name))
#         return res
#
#     @api.model
#     def name_search(self, name, args=None, operator='ilike', limit=100):
#         if name:
#             recs = self.search([('name', operator, name)] + (args or []), limit=limit)
#             if not recs:
#                 recs = self.search(['|', ('institute', operator, name), ('code', operator, name)] + (args or []), limit=limit)
#             return recs.name_get()
#         return super(OdooCMSFacultyStaff, self).name_search(name, args=args, operator=operator, limit=limit)
#
#     def calculate_year_month_mask(self, date_one, date_two):
#         '''
#         Function returns Date string:
#         Format:
#             XY - XM - XD i.e. X are numbers computed from date_one and date_two
#         Pass Your Dates to get the masked date
#         '''
#         if not type(date_one) or type(date_two) == type(date):
#             return False
#         rdelta = relativedelta(date_two, date_one)
#         date_masked = str(rdelta.years) + 'Y - ' + str(rdelta.months) + 'M - ' + str(rdelta.days) + 'D'
#         return date_masked
#
#     @api.depends('employee_id.birthday')
#     def _compute_employee_age(self):
#         for record in self:
#             age = ''
#             if record.employee_id.birthday:
#                 age = record.calculate_year_month_mask(record.employee_id.birthday, date.today())
#             record.emp_age = age
#     #
#     # @api.depends('master_ids', 'master_ids.hr_emp_eff_from_dt', 'master_ids.hr_emp_status')
#     # def _compute_employment_date(self):
#     #     for record in self:
#     #         employed_from = None
#     #         for child in record.master_ids:
#     #             if child.hr_emp_status == 'A' and child.hr_emp_eff_from_dt:
#     #                 employed_from = child.hr_emp_eff_from_dt
#     #         record.employed_from = employed_from
#     #
#     # @api.depends('master_ids', 'master_ids.hr_emp_placed_dept', 'master_ids.hr_emp_status')
#     # def _compute_department(self):
#     #     for record in self:
#     #         department = None
#     #         for child in record.master_ids:
#     #             if child.hr_emp_status == 'A' and child.hr_emp_placed_dept:
#     #                 department = child.hr_emp_placed_dept
#     #         record.department = department
#     #
#     # @api.depends('master_ids', 'master_ids.hr_emp_placed_inst', 'master_ids.hr_emp_status')
#     # def _compute_institute(self):
#     #     for record in self:
#     #         institute = None
#     #         for child in record.master_ids:
#     #             if child.hr_emp_status == 'A' and child.hr_emp_placed_inst:
#     #                 institute = child.hr_emp_placed_inst
#     #         record.institute = institute
#     #
#     # @api.depends('master_ids', 'master_ids.hr_emp_ebps', 'master_ids.hr_emp_status')
#     # def _compute_ebps(self):
#     #     for record in self:
#     #         ebps = None
#     #         for child in record.master_ids:
#     #             if child.hr_emp_status == 'A' and child.hr_emp_ebps:
#     #                 ebps = child.hr_emp_ebps
#     #         record.ebps = ebps
#     #
#     # @api.depends('master_ids', 'master_ids.hr_emp_desig', 'master_ids.hr_emp_status')
#     # def _compute_designation(self):
#     #     for record in self:
#     #         designation = None
#     #         for child in record.master_ids:
#     #             if child.hr_emp_status == 'A' and child.hr_emp_desig:
#     #                 designation = child.hr_emp_desig
#     #         record.designation = designation
#     #
#     # @api.depends('master_ids', 'master_ids.hr_emp_status')
#     # def _compute_activity_status(self):
#     #     for record in self:
#     #         hr_emp_status = None
#     #         for child in record.master_ids:
#     #             if child:
#     #                 hr_emp_status = child.hr_emp_status
#     #         record.employee_status = hr_emp_status
#     #
#     # @api.depends('master_ids', 'master_ids.hr_emp_category')
#     # def _compute_category(self):
#     #     for record in self:
#     #         hr_emp_category = None
#     #         for child in record.master_ids:
#     #             if child:
#     #                 hr_emp_category = child.hr_emp_category
#     #         record.employee_category = hr_emp_category
#     #
#     # @api.depends('master_ids', 'master_ids.hr_emp_pay_pkg_type')
#     # def _compute_hr_emp_pay_pkg_type(self):
#     #     for record in self:
#     #         hr_emp_pay_pkg_type = None
#     #         for child in record.master_ids:
#     #             if child:
#     #                 hr_emp_pay_pkg_type = child.hr_emp_pay_pkg_type
#     #         record.hr_emp_pay_pkg_type = hr_emp_pay_pkg_type
#     #
#     # @api.depends('master_ids', 'master_ids.hr_emp_project')
#     # def _compute_project(self):
#     #     for record in self:
#     #         hr_emp_project = None
#     #         for child in record.master_ids:
#     #             if child:
#     #                 hr_emp_project = child.hr_emp_project
#     #         record.hr_emp_project = hr_emp_project
#     #
#     # @api.depends('master_ids', 'master_ids.hr_emp_action_type')
#     # def _compute_hr_emp_action_type(self):
#     #     for record in self:
#     #         hr_emp_action_type = None
#     #         for child in record.master_ids:
#     #             if child:
#     #                 hr_emp_action_type = child.hr_emp_action_type
#     #         record.hr_emp_action_type = hr_emp_action_type
#     #
#     # @api.depends('master_ids', 'master_ids.hr_emp_type')
#     # def _compute_hr_emp_type(self):
#     #     for record in self:
#     #         hr_emp_type = None
#     #         for child in record.master_ids:
#     #             if child:
#     #                 hr_emp_type = child.hr_emp_type
#     #         record.hr_emp_type = hr_emp_type
#
#     @api.depends('additional_duties', 'additional_duties.hr_emp_ad_duty', 'additional_duties.hr_emp_ad_status')
#     def _compute_additional_duty(self):
#         for record in self:
#             additional_duty = None
#             for child in record.additional_duties:
#                 if child.hr_emp_ad_status == 'A' and child.hr_emp_ad_duty:
#                     additional_duty = child.hr_emp_ad_duty
#             record.additional_duty = additional_duty
#
#     # Employee History Count
#     def _count_master(self):
#         for rec in self:
#             recs = self.env['odoocms.hr.emp.rec.master'].search([('faculty_staff_id','=',rec.id)])
#             rec.master_cnt = len(recs)
#
#     # Contract Renewal Count
#     def _count_master_contract_renew(self):
#         for rec in self:
#             recs = self.env['odoocms.hr.emp.contract.renew'].search([('faculty_staff_id', '=', rec.id)])
#             rec.renew_cnt = len(recs)
#
#     # Visit Abroad Count
#     def _count_master_va(self):
#         for rec in self:
#             recs = self.env['odoocms.hr.emp.visit.abroad'].search([('faculty_staff_id', '=', rec.id)])
#             rec.va_cnt = len(recs)
#
#     # Visit Probation Count
#     def _count_master_probation(self):
#         for rec in self:
#             recs = self.env['odoocms.hr.emp.probation'].search([('faculty_staff_id', '=', rec.id)])
#             rec.probation_cnt = len(recs)
#
#     # Visit Financial Count
#     def _count_master_fin_incentive(self):
#         for rec in self:
#             recs = self.env['odoocms.hr.emp.fin.inc'].search([('faculty_staff_id', '=', rec.id)])
#             rec.incentive_cnt = len(recs)
#
#     # Additional Duty Count
#     def _count_master_add_duty(self):
#         for rec in self:
#             recs = self.env['odoocms.hr.emp.add.duty'].search([('faculty_staff_id', '=', rec.id)])
#             rec.add_duty_cnt = len(recs)
#
#     #Discipline Count
#     def _count_master_discipline(self):
#         for rec in self:
#             recs = self.env['odoocms.hr.emp.discipline'].search([('faculty_staff_id', '=', rec.id)])
#             rec.discipline_cnt = len(recs)
#
#     @api.onchange('employee_id')
#     def set_emp_name(self):
#         for rec in self:
#             if rec.employee_id:
#                 rec.first_name = rec.employee_id.name
#
#     @api.constrains('cnic_no_fms')
#     def check_ncnic(self):
#         for rec in self:
#             if not re.match("\d{5}-\d{7}-\d{1}", rec.cnic_no_fms):
#                 raise ValidationError(_('Invalid CNIC Pattern..!! "99999-9999999-9"'
#                                         'EMPLOYEE/FACULTY CNIC Must Contain Numeric Value [0-9]'))
#
#     @api.constrains('father_cnic')
#     def check_ncnicf(self):
#         for rec in self:
#             if self.father_cnic and not re.match("\d{5}-\d{7}-\d{1}", str(rec.father_cnic)):
#                 raise ValidationError(_('Invalid CNIC Pattern..!! "99999-9999999-9"'
#                                        ' EMPLOYEE/FACULTY Father CNIC Must Contain Numeric Value [0-9]'))
#
#     # Functioned Referred on XML to Show Employee Leave View
#     def show_hr_con_leave(self):
#         return {
#                'name': ('Employee Leaves'),
#                'view_type': 'form',
#                'view_mode': 'form,tree',
#                'res_model': 'hr.leave',
#                'view_id': False,
#                'type': 'ir.actions.act_window',
#            }
#
#     # Functioned Referred on XML to Show Employee Record History View
#     # def show_hr_emp(self):
#     #     return {
#     #         'name': ('Employee Record'),
#     #         'view_type': 'form',
#     #         'view_mode': 'tree,form',
#     #         'res_model': 'odoocms.hr.emp.rec.master',
#     #         'view_id': False,
#     #         'type': 'ir.actions.act_window',
#     #         'domain' : [('id', 'in', self.master_ids.ids)]
#     #     }
#
#     # Functioned Referred on XML to Show Employee Contract Renew View
#     def show_hr_con_renew(self):
#         employee_record = self.env['odoocms.hr.emp.contract.renew'].search(
#             [('faculty_staff_id', '=', self._context['default_faculty_staff_id'])])
#         return {
#             'name': ('Employee Contract Renew'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'odoocms.hr.emp.contract.renew',
#             'view_id': False,
#             'type': 'ir.actions.act_window',
#             'domain': [('id', 'in', employee_record.ids)]
#         }
#
#     # Functioned Referred on XML to Show Employee Abroad Visit
#     def show_hr_visit_abroad(self):
#         employee_record = self.env['odoocms.hr.emp.visit.abroad'].search(
#             [('faculty_staff_id', '=', self._context['default_faculty_staff_id'])])
#         return {
#             'name': ('Employee Visit Abroad'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'odoocms.hr.emp.visit.abroad',
#             'view_id': False,
#             'type': 'ir.actions.act_window',
#             'domain': [('id', 'in', employee_record.ids)]
#         }
#
#     # Functioned Referred on XML to Show Employee Probation
#     def show_hr_probation(self):
#         employee_record = self.env['odoocms.hr.emp.probation'].search(
#             [('faculty_staff_id', '=', self._context['default_faculty_staff_id'])])
#         return {
#             'name': ('Employee Probation'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'odoocms.hr.emp.probation',
#             'view_id': False,
#             'type': 'ir.actions.act_window',
#             'domain': [('id', 'in', employee_record.ids)]
#         }
#
#     # Functioned Referred on XML to Show Financial Incentive
#     def show_hr_fin_inc(self):
#         employee_record = self.env['odoocms.hr.emp.fin.inc'].search(
#             [('faculty_staff_id', '=', self._context['default_faculty_staff_id'])])
#         return {
#             'name': ('Employee Financial Incentive'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'odoocms.hr.emp.fin.inc',
#             'view_id': False,
#             'type': 'ir.actions.act_window',
#             'domain': [('id', 'in', employee_record.ids)]
#         }
#
#     # Functioned Referred on XML to Show Additional Duty
#     def show_hr_ad_duty(self):
#         employee_record = self.env['odoocms.hr.emp.add.duty'].search(
#             [('faculty_staff_id', '=', self._context['default_faculty_staff_id'])])
#         return {
#             'name': ('Employee Additional Duty'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'odoocms.hr.emp.add.duty',
#             'view_id': False,
#             'type': 'ir.actions.act_window',
#             'domain': [('id', 'in', employee_record.ids)]
#         }
#
#     # Functioned Referred on XML to Show Discipline
#     def show_hr_discipline(self):
#             employee_record = self.env['odoocms.hr.emp.discipline'].search(
#                 [('faculty_staff_id', '=', self._context['default_faculty_staff_id'])])
#             return {
#                 'name': ('Employee Discipline'),
#                 'view_type': 'form',
#                 'view_mode': 'tree,form',
#                 'res_model': 'odoocms.hr.emp.discipline',
#                 'view_id': False,
#                 'type': 'ir.actions.act_window',
#                 'domain': [('id', 'in', employee_record.ids)]
#             }
#
#     def create_employee(self):
#         for record in self:
#             vals = {
#                 'name': record.name,
#                 'country_id': record.nationality.id,
#                 'gender': record.gender,
#                 'address_home_id': record.partner_id.id,
#                 'birthday': record.date_of_birth,
#                 'image': record.image,
#                 'work_phone': record.phone,
#                 'work_mobile': record.mobile,
#                 'work_email': record.email,
#             }
#             if not record.employee_id or len(record.employee_id) == 0:
#                 emp_id = self.env['hr.employee'].create(vals)
#                 record.write({'employee_id': emp_id.id})
#                 record.partner_id.write({'employee': True})
#
#             if not record.user_id or len(record.user_id) == 0:
#                 record.create_user()
#             record.employee_id.user_id = record.user_id
#             record.user_id = record.user_id


# class WizardFacultyEmployee(models.TransientModel):
#
#     _name = 'wizard.faculty.employee'
#     _description = "Create Employee and User of Faculty"
#
#     user_boolean = fields.Boolean("Want to create User too ?", default=True)
#
#     def create_employee(self):
#         for record in self:
#             active_id = self.env.context.get('active_ids', []) or []
#             faculty = self.env['odoocms.faculty.staff'].browse(active_id)
#             faculty.create_employee()
#             if record.user_boolean and not faculty.user_id:
#                 group_portal = self.env.ref('base.group_portal')
#                 self.env['res.users'].create_user(faculty, group_portal)
#                 faculty.employee_id.user_id = faculty.user_id
#


class OdooCMSAcadCategory(models.Model):

    _name = 'odoocms.acad.category'
    _description = 'HR Academic Category'

    name = fields.Char(string='Category')


class OdooCMSQualification(models.Model):
    _name = 'odoocms.hr.qualification'
    _description = 'HR Qualification Setup'
    _rec_name = 'hr_qual_short_desc'

    code = fields.Char(string='Code')
    hr_qual_short_desc = fields.Char(string="Short Description")
    hr_qual_long_desc = fields.Char(string="Long Description")
    hr_qual_desc = fields.Char(string="Description")
    hr_qual_status = fields.Selection(
        [('A', 'ACTIVE'), ('I', 'INACTIVE')],
        string='Status', required=True, default='A', track_visibility='onchange')


# HR Competent Authority SETUP DB Table
class OdooCMSCompetentAuthority(models.Model):
    _name = 'odoocms.hr.ca'
    _description = 'HR Competent Authority'
    _rec_name = 'hr_ca_name'

    code = fields.Char(string='Code')
    hr_ca_body_type = fields.Selection(
        [('B', 'BODY'), ('I', 'INDIVIDUAL')],
        string='Body Type', required=True, default='I', track_visibility='onchange')
    hr_ca_name = fields.Char(string="Competent Authority Name")
    hr_ca_code = fields.Char(string="Code")
    hr_ca_level = fields.Char(string="Approval Chain Level")
    hr_ca_status = fields.Selection(
        [('A', 'ACTIVE'), ('I', 'INACTIVE')],
        string='Status', required=True, default='A', track_visibility='onchange')


# HR Competent Authority Meeting SETUP DB Table
class OdooCMSCompetentAuthMeeting(models.Model):
    _name = 'odoocms.hr.ca.meeting'
    _description = 'HR Competent Authority Meeting'

    code = fields.Char(string='Code')
    hr_ca_emp_id = fields.Many2one('hr.employee', 'Employee')
    hr_ca_id = fields.Many2one('odoocms.hr.ca', 'Competent Authority Name')
    hr_ca_meeting_dt = fields.Date(string="Meeting Date")
    hr_ca_meeting_chairby = fields.Char(string="Meeting Chaired By")
    hr_ca_meeting_remarks = fields.Text(string="Meeting Remarks")


# HR Scale SETUP DB Table
class OdooCMSScale(models.Model):
    _name = 'odoocms.hr.scale'
    _description = 'HR Scales'
    # Change for Data Import
    _rec_name = 'hr_scale_no'

    code = fields.Char(string='Code')
    hr_scale_no = fields.Char(string="BPS")
    hr_scale_desc = fields.Char(string="BPS/EBPS Description")


# HR Universities SETUP DB Table
class OdooCMSUniversity(models.Model):
    _name = 'odoocms.hr.university'
    _description = 'HR Universities'
    _rec_name = 'hr_uni_desc_long'

    code = fields.Char(string='Code')
    hr_uni_desc_long = fields.Char(string="*University/Board Description")
    hr_uni_desc_short = fields.Char(string="University/Board Description")
    hr_uni_country_code = fields.Char(string="Country Code")
    hr_uni_type = fields.Selection(
        [('U', 'UNIVERSITY'), ('B', 'BOARD')],
        string='University Type', required=True, default='U', track_visibility='onchange')
    hr_uni_status = fields.Selection(
        [('A', 'ACTIVE'), ('I', 'INACTIVE')],
        string='Status', required=True, default='A', track_visibility='onchange')


# HR Post SETUP DB Table
class OdooCMSPost(models.Model):
    _name = 'odoocms.hr.post'
    _description = 'HR Post'
    _rec_name = 'hr_post_name'

    code = fields.Char(string='Code')
    hr_post_child_ids = fields.One2many('odoocms.hr.post.detail', 'hr_post_dtl_child_id')
    hr_post_name = fields.Char(string="Post Name")
    hr_post_code = fields.Char(string="Post Code")


# HR Forces SETUP DB Table
class OdooCMSForce(models.Model):
    _name = 'odoocms.hr.forces'
    _description = 'HR Forces'
    _rec_name = 'hr_force_desc'

    code = fields.Char(string='Code')
    hr_force_desc = fields.Char(string="Force Description")
    hr_force_status = fields.Selection(
        [('A', 'ACTIVE'), ('I', 'INACTIVE')],
        string='Status', required=True, default='A', track_visibility='onchange')


# HR ARM SETUP DB Table
class OdooCMSArm(models.Model):
    _name = 'odoocms.hr.arm'
    _description = 'HR ARMS'
    _rec_name = 'hr_arm_desc'

    code = fields.Char(string='Code')
    hr_arm_desc = fields.Char(string="ARMS Description")
    hr_arm_status = fields.Selection(
        [('A', 'ACTIVE'), ('I', 'INACTIVE')],
        string='Status', required=True, default='A', track_visibility='onchange')


# HR Ranks SETUP DB Table
class OdooCMSRank(models.Model):
    _name = 'odoocms.hr.ranks'
    _description = 'HR Ranks'
    _rec_name = 'hr_rank_desc'

    code = fields.Char(string='Code')
    hr_rank_desc = fields.Char(string="Ranks Description")
    hr_rank_status = fields.Selection(
        [('A', 'ACTIVE'), ('I', 'INACTIVE')],
        string='Status', required=True, default='A', track_visibility='onchange')


# HR Post Detail SETUP DB Table
class OdooCMSPostDetail(models.Model):
    _name = 'odoocms.hr.post.detail'
    _description = 'HR Post Detail'

    hr_post_dtl_child_id = fields.Many2one('odoocms.hr.post', 'Post id')
    hr_post_dtl_ed = fields.Date(string="Effective Date")
    hr_post_dtl_post_list = fields.Char(string="Post List")
    hr_post_dtl_type = fields.Selection(
        [('F', 'FACULTY'), ('S', 'SUPPORT STAFF'), ('other', 'OTHER')],
        string='Post Type', required=True, default='F', track_visibility='onchange')
    hr_post_level = fields.Selection(
        [('F', 'Officer(EBPS>=17)'), ('S', 'Staff(EBPS<=16)'), ('other', 'OTHER')],
        string='Post Level', required=True, default='F', track_visibility='onchange')
    hr_post_category = fields.Selection(
        [('A', 'ACADEMIC'), ('AD', 'ADMIN'), ('other', 'OTHER')],
        string='Post Category', required=True, default='A', track_visibility='onchange')
    hr_post_sub_category = fields.Selection(
        [('C', 'CLERICAL'), ('F', 'FINANCE'), ('I', 'IT'), ('L', 'LIBRARY'), ('O', 'OTHER')],
        string='Post Sub Category', required=True, default='C', track_visibility='onchange')
    hr_post_ebps = fields.Many2one('odoocms.hr.scale', 'EBPS')
    hr_post_sliding_scale = fields.Char(string="Sliding Scale")
    hr_post_min_ebps = fields.Many2one('odoocms.hr.scale', 'Minmium EBPS')
    hr_post_max_ebps = fields.Many2one('odoocms.hr.scale', 'Maximum EBPS')


# HR Faculty Post Authorization Master DB Table

class OdooCMSFacultyPostAuth(models.Model):
    _name = 'odoocms.hr.faculty.post.auth.master'
    _description = 'HR Faculty Post Authorization Master'

    hr_fac_post_child_ids = fields.One2many('odoocms.hr.faculty.post.auth.detail', 'hr_fac_dtl_child_id')
    hr_fac_post_institute = fields.Many2one('odoocms.institute', 'Institute/College')
    hr_fac_post_nod = fields.Char(string="No of Discipline")
    hr_fac_post_ss = fields.Char(string="Student Strength")
    hr_fac_post_tap = fields.Char(string="Total Authorized Posts")
    hr_fac_post_auth_prof = fields.Char(string="No of Authorized Professers")
    hr_fac_post_auth_associate_prof = fields.Char(string="No of Authorized Associate Professers")
    hr_fac_post_auth_assistant_prof = fields.Char(string="No of Authorized Assistant Professers")
    hr_fac_post_auth_lec = fields.Char(string="No of Authorized Lecturer/RVF")
    hr_fac_post_date = fields.Date(string="Student Strength as on")
    hr_fac_post_dept_code = fields.Char(string="Dept/Dte Code")
    hr_fac_post_lab_eng_civil = fields.Char(string="Lab Engineer Civilian")
    hr_fac_post_lab_eng_mil = fields.Char(string="Lab Engineer Military")


# HR Faculty Post Authorization Detail DB Table
class OdooCMSFacultyPostAuthDtl(models.Model):
    _name = 'odoocms.hr.faculty.post.auth.detail'
    _description = 'HR Faculty Post Authorization Detail'

    hr_fac_dtl_child_id = fields.Many2one('odoocms.hr.faculty.post.auth.master', 'Institute id')
    hr_fac_dtl_acad_car = fields.Selection(
        [('UGRD', 'BACHELORS'), ('MSTR', 'MASTERS'), ('PHD', 'DOCTORAL'), ('MPHIL', 'MPHIL'), ('MUGRD', 'MED-UGRD')],
        string='ACADEMIC CAREER', required=True, default='UGRD', track_visibility='onchange')
    hr_fac_dtl_fac_ratio = fields.Char(string="Faculty Ratio")
    hr_fac_dtl_std_ratio = fields.Integer(string="Student Ratio")
    hr_fac_dtl_ss = fields.Integer(string="Student Strength")
    hr_fac_dtl_miltary_std = fields.Char(string="Miltary Students")
    hr_fac_dtl_civil_std = fields.Char(string="Civilian Students")
    hr_fac_dtl_nod = fields.Char(string="No of Discipline")
    hr_fac_dtl_auth_post = fields.Integer(string="Authorized Post")
    hr_fac_dtl_fac_std_ratio = fields.Selection(
        [('U20', 'UG-> 1 FACULTY : 20 STUDENT'), ('M12', 'MS-> 1 FACULTY : 12 STUDENT'),
         ('P05', 'PHD-> 1 FACULTY : 05 STUDENTS')],
        string='FACULTY STUDENT RATIO', required=True, default='U20', track_visibility='onchange')

    @api.onchange('hr_fac_dtl_ss', 'hr_fac_dtl_std_ratio')
    def onchange_hr_fac_dtl_ss(self):

        if self.hr_fac_dtl_ss < 0:
            return {
                'warning': {
                    'title': "Incorrect Student Strength Value",
                    'message': "Student Strength Student Value can not be less then 0",
                },
            }
        if self.hr_fac_dtl_std_ratio < 0:
            return {
                'warning': {
                    'title': "Incorrect Student Ratio Value",
                    'message': "Student Ratio Value can not be less then 0",
                },
            }

        if self.hr_fac_dtl_std_ratio == 0 and self.hr_fac_dtl_ss > 0:
            return {
                'warning': {
                    'title': "Incorrect Student Ratio Value",
                    'message': "Enter Student Ratio Value..! must be greater> 0 to calculate Authorized Post",
                },
            }

        if self.hr_fac_dtl_ss:
            self.hr_fac_dtl_auth_post = self.hr_fac_dtl_ss / self.hr_fac_dtl_std_ratio


# HR Employment Record DB Table
class OdooCMSHREmploymentRecordMaster(models.Model):
    _name = 'odoocms.hr.emp.rec.master'
    _description = 'HR Emp Record Master'
    _rec_name = 'hr_emp_status'

    fms_hr_erm_ids = fields.One2many('odoocms.hr.emp.rec.detail', 'fms_emp_record_master_ids01')
    fms_hr_ermm_ids = fields.One2many('odoocms.hr.emp.rec.detail1', 'fms_emp_record_master_ids01')
    faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
    hr_emp_status = fields.Selection(
        [('A', 'ACTIVE'), ('I', 'IN ACTIVE')],
        string='STATUS', track_visibility='onchange')
    hr_emp_eff_dt = fields.Date(string="EFFECTIVE DATE")
    hr_emp_eff_from_dt = fields.Date(string="EFFECTIVE FROM")
    hr_emp_payroll_id = fields.Char(string="PAYROLL ID")
    hr_emp_placed_branch = fields.Char(string="PLACED AT (BRANCH)")
    hr_emp_post_auth_dtl = fields.Char(string="POST AUTH DETAIL ID")
    hr_emp_post_ex_auth_dtl = fields.Char(string="POST EX-DETAIL ID")
    hr_emp_conflict_post = fields.Char(string="CONFLICTING POST ID")
    hr_emp_erp_post_id = fields.Char(string="ERP POST ID")
    hr_emp_salary = fields.Char(string="SALARY ON THIS ACTION")
    hr_emp_remarks = fields.Text(size=1000, string="REMARKS")
    hr_emp_oo_no = fields.Char(string="OO NO")
    hr_emp_oo_dt = fields.Date(string="OO DATE")
    hr_emp_placed_dept = fields.Many2one('odoocms.department', 'DEPT/DTE CODE')
    hr_emp_ebps = fields.Many2one('odoocms.hr.scale', 'EBPS')
    hr_emp_desig = fields.Many2one('odoocms.designation', 'DESIGNATION')
    hr_emp_placed_inst = fields.Many2one('odoocms.institute', 'PLACED AT (INST/MAIN OFFICE)')
    hr_emp_category = fields.Selection(
        [('F', 'FACULTY'), ('S', 'SUPPORT STAFF')],
        string='CATEGORY', default='F', track_visibility='onchange')
    hr_emp_action_type = fields.Selection(
        [('ABS', 'ABSENT'), ('ADJ', 'ADJUSTMENT'),
         ('ATT', 'ATTACHMENT'), ('OPC', 'BONDED TO OPEN CONTRACT'),
         ('D', 'DEATH'), ('DEM', 'DEMOTION'), ('DEC', 'DISC. ON EXPIRY OF CONTRACT'),
         ('DTC', 'DISC. ON TENURE OF COMPLETION'), ('BFL', 'RESUMPTION / REJOIN AFTER LEAVE'),
         ('DA', 'DISCONTINUATION ON AGE'), ('DIS', 'DISCONTINUED'),
         ('DML', 'DISMISSAL'), ('EXP', 'EXPIRED'),
         ('NEJ', 'NEW JOINING'), ('LPR', 'LEAVE PRIOR TO RETIREMENT'),
         ('OTB', 'OPEN CONTRACT TO BONDED'), ('PPR', 'PAY PACKAGE REVISION'),
         ('PIN', 'POSTED IN'), ('OUT', 'POSTED OUT'),
         ('PRD', 'POSTING / ADJUSTMENT'), ('PRO', 'PROMOTION'),
         ('PHS', 'PROMOTION TO HIGHER STATUS'), ('RED', 'REDESIGNATION / ADJUSTMENT'),
         ('REM', 'RE-EMPLOYMENT'), ('RES', 'RESIGNED'),
         ('RFA', 'RETURN FROM ATTACHMENT'), ('RFS', 'REMOVAL FROM SERVICE'),
         ('RIN', 'REINSTATMENT'), ('RTD', 'RETIREMENT'),
         ('SPC', 'STATUS & PAY PACKAGE CONVERSION'), ('SPS', 'SPS'),
         ('TER', 'TERMINATION'), ('TNR', 'TENURED'),
         ('TNT', 'TTS 2nd TERM'), ('TRA', 'TRANSFER'),
         ('TTT', 'TRANSFER TO TTS'), ('UPS', 'UPGRADATION OF PAY SCALE'), ('WOL', 'WENT ON LEAVE')],
        string='ACTION TYPE', default='NEJ', size=64,
        track_visibility='onchange')
    hr_emp_project = fields.Selection(
        [('H', 'HHFP'), ('I', 'IPSP'), ('U', 'USPCASE')],
        string='PROJECT', track_visibility='onchange')
    hr_emp_type = fields.Selection(
        [('C', 'CONTRACT'), ('R', 'REGULAR')],
        string='EMPLOYEE TYPE', default='C', track_visibility='onchange')
    hr_emp_sub_cat = fields.Selection(
        [('DE', 'DEFENSE'), ('TT', 'TENURE TRACK'),
         ('DP', 'DEPUTATION'), ('NU', 'NUST'),
         ('HE', 'HEC')],
        string='SUB CATEGORY', default='NU', track_visibility='onchange')
    hr_emp_pay_pkg_type = fields.Selection(
        [('L', 'LUMPSUM'), ('B', 'BPS')],
        string='PAY PACKAGE TYPE', default='L', track_visibility='onchange')
    hr_emp_hiring = fields.Selection(
        [('CON', 'CONSULTANT'), ('RVF', 'RVF'), ('TVF', 'TVF')],
        string='HIRED AS', track_visibility='onchange')
    hr_emp_def_status = fields.Selection(
        [('R', 'RETIRED'), ('S', 'SERVING')],
        string='DEFENCE EMPLOYEE STATUS', default='S', track_visibility='onchange')

    hr_emp_hec_supvr = fields.Boolean("HEC APPROVED SUPVR")

    def status_change(self):
        self.ensure_one()
        employee_records = self.search([('faculty_staff_id', '=', self.faculty_staff_id.id),
                                        ('id', '!=', self.id)])
        if employee_records:
            for record in employee_records:
                if record.hr_emp_status == 'A':
                    record.write({'hr_emp_status': 'I'})
        self.write({'hr_emp_status': 'A'})
        return True

    @api.model
    def create(self, values):
        if values:
            employee_records = self.search([('faculty_staff_id', '=', values.get('faculty_staff_id')),
                                            ('create_date', '<', datetime.now())], order='create_date ASC')
            if employee_records:
                for record in employee_records:
                    if record.hr_emp_status == 'A':
                        record.write({'hr_emp_status': 'I'})
        result = super(OdooCMSHREmploymentRecordMaster, self).create(values)
        return result

    def write(self, values):
        result = super(OdooCMSHREmploymentRecordMaster, self).write(values)
        return result


class OdooCMSHREmploymentRecorddetail(models.Model):
    _name = 'odoocms.hr.emp.rec.detail'
    _description = 'HR Emp Record Detail'

    fms_emp_record_master_ids01 = fields.Many2one('odoocms.hr.emp.rec.master', 'Faculty ID 01')
    hr_emp_dtl_auth_id = fields.Many2one('odoocms.designation', 'AUTHORIZED ID')
    hr_emp_dtl_emp_id = fields.Many2one('hr.employee', 'EMPLOYEE ID')
    hr_emp_dtl_held_dt = fields.Date(string="HELD ON")
    hr_emp_dtl_emp_ref = fields.Char(string="MEETING REFERENCE")


class OdooCMSHREmploymentRecorddetail1(models.Model):
    _name = 'odoocms.hr.emp.rec.detail1'
    _description = 'HR Emp Record Comp Auth Detail'

    fms_emp_record_master_ids01 = fields.Many2one('odoocms.hr.emp.rec.master', string='Faculty ID')
    hr_emp_dtl1_auth_id = fields.Many2one('odoocms.designation', 'AUTHORIZED ID')
    hr_emp_dtl1_gov_body_id = fields.Many2one('odoocms.designation', 'GOVERNING BODY MEETING ID')
    hr_emp_dtl1_chaired_by = fields.Many2one('odoocms.designation', 'CHAIRED BY')
    hr_emp_dtl1_held_dt = fields.Date(string="HELD ON")

# # HR Employee Contract Renewal DB Table
# class OdooCMSHRContractRenewal(models.Model):
#     _name = 'odoocms.hr.emp.contract.renew'
#     _description = 'HR Employee Contract Renewal'
#     _rec_name = 'hr_emp_con_year'
#
#     faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
#     hr_emp_con_year = fields.Selection(
#         [('1Y','1 YEAR'),('2Y','2 YEAR'),('3Y','3 YEAR'),('5Y','5 YEAR'),('6M','6 MONTHS'),
#          ('FP','FIXED PERIOD'),('OC','OPEN CONTRACT')],
#         string='TYPE', required=True, default='1Y', track_visibility='onchange')
#     hr_emp_con_bond = fields.Selection(
#         [('Y','YES'), ('N','NO')],
#         string='BONDED', required=True, default='N', track_visibility='onchange')
#     hr_emp_con_start_dt = fields.Date(string="START DATE")
#     hr_emp_con_end_dt = fields.Date(string="END DATE")
#     status = fields.Selection(
#         [('A', 'ACTIVE'), ('I', 'IN ACTIVE')],
#         string='STATUS', required=True, default='A', track_visibility='onchange')
#     hr_emp_con_oo_no = fields.Char(string="OO NO")
#     hr_emp_con_oo_dt = fields.Date(string="OO DATE")
#     hr_emp_con_remarks = fields.Text(size=1000,string="REMARKS")
#     individual_auth = fields.One2many('odoocms.hr.emp.contract.renew.ia','contract_renew_id')
#     approval_auth = fields.One2many('odoocms.hr.emp.contract.renew.ca','contract_renew_id')
#
#     @api.constrains('hr_emp_con_start_dt', 'hr_emp_con_end_dt')
#     def validate_date(self):
#         for rec in self:
#             start_date = fields.Date.to_string(rec.hr_emp_con_start_dt)
#             end_date = fields.Date.to_string(rec.hr_emp_con_end_dt)
#             if start_date > end_date:
#                 raise ValidationError(_('"END DATE" MUST BE GREATER THEN "START DATE'))
#
#     @api.model
#     def create(self, values):
#         if values:
#             contracts = self.search([('faculty_staff_id', '=', values.get('faculty_staff_id')),
#                                 ('create_date', '<', datetime.now())], order='create_date ASC')
#             if contracts:
#                 for contract in contracts:
#                     if contract.status == 'A':
#                         contract.write({'status':'I'})
#         result = super(OdooCMSHRContractRenewal, self).create(values)
#         return result
#
#     def write(self, values):
#         result = super(OdooCMSHRContractRenewal, self).write(values)
#         return result
#
#
# class OdooCMSHRContractRenewIndividualAuthority(models.Model):
#     _name = 'odoocms.hr.emp.contract.renew.ia'
#     _description = 'HR Employee Contract Renew Individual Authority'
#
#     contract_renew_id = fields.Many2one('odoocms.hr.emp.contract.renew', 'Contract ID')
#     hr_emp_dtl_auth_id = fields.Many2one('odoocms.designation','AUTHORIZED ID')
#     authority = fields.Char('AUTHORITY')
#     hr_emp_dtl_emp_id = fields.Many2one('hr.employee', 'EMPLOYEE ID')
#     hr_emp_dtl_held_dt = fields.Date(string="HELD ON")
#     name = fields.Char('NAME')
#     hr_emp_dtl_emp_ref = fields.Char(string="MEETING REFERENCE")
#
#
# class OdooCMSHREmploymentCompetentAuthority(models.Model):
#     _name = 'odoocms.hr.emp.contract.renew.ca'
#     _description = 'HR Employee Contract Renew Competent Authority'
#
#     name = fields.Char('NAME')
#     contract_renew_id = fields.Many2one('odoocms.hr.emp.contract.renew', 'Contract ID')
#     hr_emp_dtl1_auth_id = fields.Many2one('odoocms.designation','AUTHORIZED ID')
#     authority = fields.Char('AUTHORITY')
#     hr_emp_dtl1_gov_body_id = fields.Many2one('odoocms.designation','GOVERNING BODY MEETING ID')
#     hr_emp_dtl1_chaired_by = fields.Many2one('odoocms.designation','CHAIRED BY')
#     hr_emp_dtl1_held_dt = fields.Date(string="HELD ON")
#
#
# # HR Employee Abroad Visit DB Table
# class OdooCMSHRVisitAbroad(models.Model):
#     _name = 'odoocms.hr.emp.visit.abroad'
#     _description = 'HR Employee Abroad Visit'
#     _rec_name = 'hr_emp_visit_type'
#     faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
#
#     hr_emp_visit_type = fields.Selection(
#         [('O','OFFICIAL'),('P','PERSONAL'),('S','STUDENT')],
#         string='TYPE', required=True, default='O', track_visibility='onchange')
#     hr_emp_visit_purpose = fields.Text(string="PURPOSE OF VISIT")
#     hr_emp_visit_country = fields.Many2one('res.country','COUNTRY')
#     hr_emp_visit_from_dt = fields.Date(string="FROM DATE")
#     hr_emp_visit_to_dt = fields.Date(string="TO DATE")
#     hr_emp_visit_approved_by = fields.Date(string="APPROVED BY")
#     hr_emp_visit_remarks = fields.Text(size=1000,string="REMARKS")
#
#     @api.constrains('hr_emp_visit_from_dt', 'hr_emp_visit_to_dt')
#     def validate_date(self):
#         for rec in self:
#             start_date = fields.Date.to_string(rec.hr_emp_visit_from_dt)
#             end_date = fields.Date.to_string(rec.hr_emp_visit_to_dt)
#             if start_date > end_date:
#                 raise ValidationError(_('"TO DATE"   MUST BE GREATER >THEN  "FROM DATE'))
#
#
# # HR Employee Probation DB Table
# class OdooCMSHRProbation(models.Model):
#
#     _name = 'odoocms.hr.emp.probation'
#     _description = 'HR Employee Probation'
#     _rec_name = 'hr_emp_prob_type'
#
#     faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
#     hr_emp_prob_type = fields.Selection(
#         [('ECP', 'EXTENDED CASUAL PERIOD'), ('EPP', 'EXTENDED PROBATION PERIOD'),
#          ('ICP', 'INITIAL CASUAL PERIOD'),('IPP', 'INITIAL PROBATION PERIOD')],
#         string='PROBATION TYPE', required=True, default='ECP', track_visibility='onchange')
#     hr_emp_prob_duration = fields.Selection(
#         [('12M', '12 MONTHS'), ('3M', '3 MONTHS'),('6M', '06 MONTHS')],
#         string='DURATION', required=True, default='12M', track_visibility='onchange')
#     hr_emp_prob_start_dt = fields.Date(string="START DATE")
#     hr_emp_prob_end_dt = fields.Date(string="END DATE")
#     hr_emp_prob_oo_no = fields.Char(string="OO NO:")
#     hr_emp_prob_oo_dt = fields.Date(string="OO DATE")
#     hr_emp_prob_rev_oo_no = fields.Char(string="REMOVAL FROM PROBATION OO NO")
#     hr_emp_prob_rev_dt = fields.Date(string="OO DATE REMOVAL")
#     hr_emp_prob_remarks = fields.Text(size=1000,string="REMARKS")
#
#     @api.constrains('hr_emp_prob_start_dt', 'hr_emp_prob_end_dt')
#     def validate_date(self):
#         for rec in self:
#             start_date = fields.Date.to_string(rec.hr_emp_prob_start_dt)
#             end_date = fields.Date.to_string(rec.hr_emp_prob_end_dt)
#             if start_date > end_date:
#                 raise ValidationError(_('"END DATE"  MUST BE GREATER >THEN  "START DATE'))
#
#
# # HR Employee Financial Incentive DB Table
# class OdooCMSHRFinancialIncentive(models.Model):
#
#     _name = 'odoocms.hr.emp.fin.inc'
#     _description = 'HR Employee Financial Incentive'
#     _rec_name = 'hr_emp_fin_cat'
#
#     faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
#     hr_emp_fin_cat = fields.Selection(
#         [('ADR', 'ADHOC RELIEF'),
#          ('AI', 'ADVANCE INCREMENT'),
#          ('ANI', 'ANNUAL INCREMENT'),
#          ('AR', 'ADDITIONAL RENUMERATION'),
#          ('DA', 'DEAN ALLOWANCE'),
#          ('D', 'DEATH'),
#          ('HODA', 'HOD ALLOWANCE'),
#          ('HONOR', 'HONORARIUM'),
#          ('ITA', 'IT ALLOWANCE'),
#          ('OT', 'OVER TIME'),
#          ('PBA', 'PERFORMANCE BASED INCREMENT (TTS)'),
#          ('PA', 'PAY ENHANCEMENTS'),
#          ('PMA', 'PRE MATURE INCEREMENT'),
#          ('QI', 'QUALIFICATION INCREMENT'),
#          ('RPA', 'RISAL PUR ALLOWANCE'),
#          ('HODRA', 'HOD RESEARCH ALLOWANCE')],
#         string='CATEGORY', required=True, default='AR', size=64,
#         track_visibility='onchange')
#     hr_emp_fin_type = fields.Selection(
#         [('A', 'ANNUALLY'), ('M', 'MONTHLY'),('O','ONCE'),('SP','SPECIFIC PERIOD')],
#         string='TYPE', required=True, default='A', track_visibility='onchange')
#     hr_emp_fin_start_dt = fields.Date(string="START DATE")
#     hr_emp_fin_end_dt = fields.Date(string="END DATE")
#     hr_emp_fin_increment_no = fields.Char(string="NO OF INCREMENTS (IF ANY)")
#     hr_emp_fin_increment_amt = fields.Char(string="AMOUNT")
#     hr_emp_fin_oo_no = fields.Char(string="OO NO:")
#     hr_emp_fin_oo_dt = fields.Date(string="OO DATE")
#     hr_emp_fin_add_duty = fields.Char(string="LINK IT TO ADDITIONAL DUTY")
#     hr_emp_fin_remarks = fields.Text(size=1000,string="REMARKS")
#
#     @api.constrains('hr_emp_fin_start_dt','hr_emp_fin_end_dt')
#     def validate_date(self):
#         for rec in self:
#             start_date = fields.Date.to_string(rec.hr_emp_fin_start_dt)
#             end_date = fields.Date.to_string(rec.hr_emp_fin_end_dt)
#             if start_date > end_date:
#                 raise ValidationError(_('"END DATE"  MUST BE GREATER >THEN  "START DATE'))
#
#
# # HR Employee Additional Duty DB Table
# class OdooCMSHRAdditionalDuty(models.Model):
#
#     _name = 'odoocms.hr.emp.add.duty'
#     _description = 'HR Employee Additional Duty'
#     _rec_name = 'hr_emp_ad_desig'
#
#     faculty_staff_id = fields.Many2one('odoocms.faculty.staff', 'Faculty ID')
#     hr_emp_ad_desig = fields.Many2one('odoocms.designation','DESIGNATION OF EMPLOYEE')
#     hr_emp_ad_duty = fields.Many2one('odoocms.designation','DESIGNATION OF ADDITIONAL DUTY')
#     hr_emp_ad_start_dt = fields.Date(string="FROM")
#     hr_emp_ad_end_dt = fields.Date(string="TO")
#     hr_emp_ad_status = fields.Selection(
#         [('A', 'ACTIVE'), ('I', 'IN ACTIVE')],
#         string='STATUS', required=True, default='A', track_visibility='onchange')
#     hr_emp_ad_remarks = fields.Text(string="REMARKS", size=1000)
#
#     @api.constrains('hr_emp_ad_start_dt', 'hr_emp_ad_end_dt')
#     def validate_date(self):
#         for rec in self:
#             start_date = fields.Date.to_string(rec.hr_emp_ad_start_dt)
#             end_date = fields.Date.to_string(rec.hr_emp_ad_end_dt)
#             if start_date > end_date:
#                 raise ValidationError(_('"TO DATE"  MUST BE GREATER >THEN  "FROM DATE'))
#
#     @api.model
#     def create(self, values):
#         if values:
#             additionalduites = self.search([('faculty_staff_id', '=', values.get('faculty_staff_id')),
#                                             ('create_date', '<', datetime.now())], order='create_date ASC')
#             if additionalduites:
#                 for duty in additionalduites:
#                     if duty.hr_emp_ad_status == 'A':
#                         duty.write({'hr_emp_ad_status':'I'})
#         result = super(OdooCMSHRAdditionalDuty, self).create(values)
#         return result
#
#     def write(self, values):
#         result = super(OdooCMSHRAdditionalDuty, self).write(values)
#         return result
#
#
# class OdooCMSHRDiscipline(models.Model):
#
#     _name = 'odoocms.hr.emp.discipline'
#     _description = 'HR Employee Discipline Record'
#     _rec_name = 'hr_emp_disp_offence_dtl'
#
#     faculty_staff_id = fields.Many2one('odoocms.faculty.staff','Faculty ID40')
#     hr_emp_disp_offence_dtl = fields.Char(string="DETAIL OF OFFENCE")
#     hr_emp_disp_offence_dt = fields.Date(string="OFFENCE DATE")
#     hr_emp_disp_offence_place = fields.Char(string="PLACE OF OFFENCE")
#     hr_emp_disp_punish_award = fields.Char(string="PUNISHMENT AWARDED")
#     punishment_awarded_on = fields.Date(string="PUNISHMENT AWARDED ON")
#     punishment_awarded_by = fields.Many2one('hr.employee', 'PUNISHMENT AWARDED BY')
#     hr_emp_disp_head_by = fields.Many2one('hr.employee', 'INQUIRY HEADED BY')
#     hr_emp_disp_reinstate_by = fields.Many2one('hr.employee', 'REINSTATED BY')
#     hr_emp_disp_inq = fields.Selection(
#         [('Y', 'YES'), ('N', 'NO')],
#         string='INQUIRY HELD', required=True, default='N', track_visibility='onchange')
#     hr_emp_disp_punish = fields.Selection(
#         [('MAJOR', 'MAJOR'), ('MINOR', 'MINOR')],
#         string='TYPE OF PUNISHMENT', required=True, default='MINOR', track_visibility='onchange')
#     hr_emp_disp_reinstate= fields.Selection(
#         [('Y', 'YES'), ('N', 'NO')],
#         string='RE-INSTATED', required=True, default='Y', track_visibility='onchange')
#     hr_emp_disp_remarks = fields.Text(size=1000,string="REMARKS")
#     hr_emp_disp_reinstate_on = fields.Date(string="RE-INSTATED ON")
#
# # ---------------------------------------------------------------------------------------
# # This Table kept in Parser to Prevent Server Breakage, this table is no more in Use.
# # ---------------------------------------------------------------------------------------
# class OdooCMSHRAAR(models.Model):
#     _name = 'odoocms.hr.emp.aar'
#     _description = 'HR Employee AAR'
#     _rec_name = 'hr_emp_aar_type'
#
#     faculty_staff_id = fields.Many2one('odoocms.faculty.staff','Faculty ID')
#     hr_emp_aar_type = fields.Selection(
#         [('A', 'ANNUAL'), ('P', 'PROBATION'), ('S', 'SPECIAL/RE')],
#         string='AAR TYPE', required=True, default='A', track_visibility='onchange')
#     hr_emp_io_grade = fields.Selection(
#         [('VG', 'VERY GOOD'),('O', 'OUTSTANDING'),('P', 'POOR'), ('G', 'GOOD'), ('E', 'EXCELLENT'), ('A', 'AVERAGE')
#         ,('AB', 'ABOVE AVERAGE'), ('ND', 'NOT DUE'), ('NA', 'NOT AVAILABLE'),('OL', 'ON LEAVE')
#         ,('S','SATISFACTORY'),('US', 'UN SATISFACTORY')],
#         string='GRADE OF IO', required=True, default='VG', track_visibility='onchange')
#     hr_emp_sro_grade = fields.Selection(
#         [('VG','VERY GOOD'), ('O','OUTSTANDING'), ('P','POOR'), ('G','GOOD'), ('E','EXCELLENT'),('A', 'AVERAGE')
#             , ('AB', 'ABOVE AVERAGE'), ('ND', 'NOT DUE'), ('NA', 'NOT AVAILABLE'), ('OL', 'ON LEAVE')],
#         string='GRADE OF SRO', required=True, default='VG', track_visibility='onchange')
#     hr_emp_aar_year = fields.Char(string="YEAR")
#     hr_emp_aar_score = fields.Char(string="AAR SCORE")
#     hr_emp_aar_io = fields.Many2one('hr.employee','INITIATING OFFICER (IO)')
#     hr_emp_aar_sro = fields.Many2one('hr.employee','SENIOR REPORTING OFFICER (SRO)')
#     hr_emp_aar_tech = fields.Many2one('hr.employee','TECHNICAL REPORTING OFFICER (TRO)')
#     hr_emp_aar_nsro = fields.Many2one('hr.employee','NEXT SENIOR REPORTING OFFICER (NSRO)')
#     hr_emp_aar_nsro_grade = fields.Char(string="GRADE OF NSRO")
#     hr_emp_aar_adverse_remarks = fields.Text(size=1000,string="ADVERSE REMARKS")
#     hr_emp_aar_tech_remarks = fields.Text(size=1000,string="REMARKS OF TRO")
