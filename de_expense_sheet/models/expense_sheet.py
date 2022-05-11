# -*- coding: utf-8 -*-

from odoo import models, fields, api



class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"
    reason = fields.Char(string="Reason")
    
    
   
