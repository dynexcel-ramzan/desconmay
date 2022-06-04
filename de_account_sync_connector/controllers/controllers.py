# -*- coding: utf-8 -*-
# from odoo import http


# class DeAccountSyncConnector(http.Controller):
#     @http.route('/de_account_sync_connector/de_account_sync_connector/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_sync_connector/de_account_sync_connector/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_sync_connector.listing', {
#             'root': '/de_account_sync_connector/de_account_sync_connector',
#             'objects': http.request.env['de_account_sync_connector.de_account_sync_connector'].search([]),
#         })

#     @http.route('/de_account_sync_connector/de_account_sync_connector/objects/<model("de_account_sync_connector.de_account_sync_connector"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_sync_connector.object', {
#             'object': obj
#         })
