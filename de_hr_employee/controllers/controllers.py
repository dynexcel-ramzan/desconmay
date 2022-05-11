# -*- coding: utf-8 -*-
# from odoo import http


# class DeHrEmployee(http.Controller):
#     @http.route('/de_hr_employee/de_hr_employee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_hr_employee/de_hr_employee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_hr_employee.listing', {
#             'root': '/de_hr_employee/de_hr_employee',
#             'objects': http.request.env['de_hr_employee.de_hr_employee'].search([]),
#         })

#     @http.route('/de_hr_employee/de_hr_employee/objects/<model("de_hr_employee.de_hr_employee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_hr_employee.object', {
#             'object': obj
#         })
