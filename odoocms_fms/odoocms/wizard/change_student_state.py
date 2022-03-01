# -*- coding: utf-8 -*-
import pdb
import time
import datetime
from odoo import api, fields, models,_
from dateutil.relativedelta import relativedelta


class OdooCMSChangeStudentState(models.TransientModel):
	_name ='odoocms.student.state.change'
	_description = 'Change Student State'
				
	@api.model	
	def _get_students(self):
		if self.env.context.get('active_model', False) == 'odoocms.student' and self.env.context.get('active_ids', False):
			return self.env.context['active_ids']
			
	student_ids = fields.Many2many('odoocms.student', string='Students',
		help="""Only selected students will be Processed.""",default=_get_students)
	state = fields.Selection(
		[('draft', 'Draft'),('cancel', 'Cancel'), ('suspend', 'Suspend'),('elumni', 'Elumni'), ('enroll', 'Enroll'),], string='Status',
		default='suspend')
	rule_id = fields.Many2one('odoocms.student.change.state.rule', string = "Reason",)


	def change_student_state(self):
		for student in self.student_ids:
			# if not student.batch_id:
			# 	continue
			# if not student.section_id:
			# 	if student.batch_id and len(student.batch_id.section_ids) == 1:
			# 		student.section_id = student.batch_id.section_ids[0].id
			# 	else:
			# 		continue
			# if (student.state == 'enroll' and (self.state in ('draft','suspend', 'cancel'))):
			# 	student.update({'state': self.state})
			# elif (student.state in ('draft','suspend', 'cancel') and self.state == 'enroll'):
			# 	student.update({'state': 'enroll'})

			student.state = self.state
		return {'type': 'ir.actions.act_window_close'}



