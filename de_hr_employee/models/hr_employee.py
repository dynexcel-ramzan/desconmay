# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"
    dept_manager_id = fields.Many2one('hr.employee',  string='Dept Manager')
