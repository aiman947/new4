# -*- coding: utf-8 -*-
import pdb
import time
import datetime
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta

class OdooCMSCreateStudentUserWiz(models.TransientModel):
	_name ='odoocms.student.user.wiz'
	_description = 'Create Student User'

	@api.model
	def _get_students(self):
		if self.env.context.get('active_model', False) == 'odoocms.student' and self.env.context.get('active_ids', False):
			return self.env.context['active_ids']

	student_ids = fields.Many2many('odoocms.student', string='Students',
		help="""Only selected students will be Processed.""",default=_get_students)


	def create_user(self):
		group_portal = self.env.ref('base.group_portal')
		for record in self.student_ids:
			if not record.user_id:
				data = {
					#'name': record.name + ' ' + (record.last_name or ''),
					'partner_id': record.partner_id.id,
					'login': record.id_number or record.entryID or record.email,
					'password': record.mobile or '123456',
					'groups_id': group_portal,
				}
				user = self.env['res.users'].create(data)
				record.user_id = user.id

		return {'type': 'ir.actions.act_window_close'}


class OdooCMSCreateFacultyUser(models.TransientModel):
	_name ='odoocms.faculty.user.wiz'
	_description = 'Create Faculty User'

	@api.model
	def _get_faculty(self):
		if self.env.context.get('active_model', False) == 'odoocms.faculty.staff' and self.env.context.get('active_ids', False):
			return self.env.context['active_ids']

	faculty_ids = fields.Many2many('odoocms.faculty.staff', string='Faculty Staff',
		help="""Only selected staff will be Processed.""",default=_get_faculty)


	def create_user(self):
		group_portal = self.env.ref('base.group_portal')
		for record in self.faculty_ids:
			if not record.user_id:
				data = {
					#'name': record.name + ' ' + (record.last_name or ''),
					'partner_id': record.partner_id.id,
					'login': record.email,
					'password': record.mobile or '654321',
					'groups_id': group_portal,
				}
				user = self.env['res.users'].create(data)
				record.user_id = user.id

		return {'type': 'ir.actions.act_window_close'}


