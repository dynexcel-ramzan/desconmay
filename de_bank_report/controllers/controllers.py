# -*- coding: utf-8 -*-
# from odoo import http


# class DeBankReport(http.Controller):
#     @http.route('/de_bank_report/de_bank_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_bank_report/de_bank_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_bank_report.listing', {
#             'root': '/de_bank_report/de_bank_report',
#             'objects': http.request.env['de_bank_report.de_bank_report'].search([]),
#         })

#     @http.route('/de_bank_report/de_bank_report/objects/<model("de_bank_report.de_bank_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_bank_report.object', {
#             'object': obj
#         })
