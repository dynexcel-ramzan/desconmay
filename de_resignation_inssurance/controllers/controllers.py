# -*- coding: utf-8 -*-
# from odoo import http


# class DeResignationInssurance(http.Controller):
#     @http.route('/de_resignation_inssurance/de_resignation_inssurance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_resignation_inssurance/de_resignation_inssurance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_resignation_inssurance.listing', {
#             'root': '/de_resignation_inssurance/de_resignation_inssurance',
#             'objects': http.request.env['de_resignation_inssurance.de_resignation_inssurance'].search([]),
#         })

#     @http.route('/de_resignation_inssurance/de_resignation_inssurance/objects/<model("de_resignation_inssurance.de_resignation_inssurance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_resignation_inssurance.object', {
#             'object': obj
#         })
