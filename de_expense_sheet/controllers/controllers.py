# -*- coding: utf-8 -*-
# from odoo import http


# class DeExpenseSheet(http.Controller):
#     @http.route('/de_expense_sheet/de_expense_sheet/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_expense_sheet/de_expense_sheet/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_expense_sheet.listing', {
#             'root': '/de_expense_sheet/de_expense_sheet',
#             'objects': http.request.env['de_expense_sheet.de_expense_sheet'].search([]),
#         })

#     @http.route('/de_expense_sheet/de_expense_sheet/objects/<model("de_expense_sheet.de_expense_sheet"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_expense_sheet.object', {
#             'object': obj
#         })
