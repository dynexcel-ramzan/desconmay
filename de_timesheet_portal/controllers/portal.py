# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from operator import itemgetter

from markupsafe import Markup

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, UserError, ValidationError

from odoo.http import request
from odoo.tools.translate import _
from odoo.tools import groupby as groupbyelem
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager
from odoo.osv.expression import OR, AND


class CustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'timesheet_report_count' in counters:
            values['timesheet_report_count'] = request.env['hr.timesheet.sheet'].search_count([]) \
                if request.env['hr.timesheet.sheet'].check_access_rights('read', raise_exception=False) else 0
        if 'timesheet_count' in counters:
            values['timesheet_count'] = request.env['account.analytic.line'].search_count([]) \
                if request.env['account.analytic.line'].check_access_rights('read', raise_exception=False) else 0
        return values
    
    # timesheet report page
    @http.route(['/my/timelogs', '/my/timelogs/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_timelogs(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Sheet = request.env['hr.timesheet.sheet']
        domain = []

        searchbar_sortings = {
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        #if date_begin and date_end:
        #    domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # Timesheet Report count
        timesheet_report_count = Sheet.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/timelogs",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=timesheet_report_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        sheets = Sheet.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_report_timesheets_history'] = sheets.ids[:100]
        
        project_list = []
        project_obj = request.env['project.project'].sudo().search([])
        for project in project_obj:
            project_list.append({
                'name': project.name, 
                'id': project.id
            })
        values['project_list'] = project_list
        

        values.update({
            #'date': date_begin,
            #'date_end': date_end,
            'sheets': sheets,
            'page_name': 'timelogs_report',
            'default_url': '/my/timelogs',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("de_timesheet_portal.portal_my_timelogs", values)
    
    # ------------------------------------------------------------
    # My Timesheet
    # ------------------------------------------------------------
    def _timesheet_get_page_view_values(self, timesheet, access_token, **kwargs):
        sheet = kwargs.get('sheet')
        if sheet:
            sheet_accessible = True
            page_name = 'report_timelog'
            history = 'my_report_timelogs_history'
        else:
            page_name = 'sheet'
            history = 'my_timelogs_history'
            try:
                sheet_accessible = bool(timesheet.sheet_id.id and self._document_check_access('hr.timesheet.sheet', timesheet.sheet_id.id))
            except (AccessError, MissingError):
                sheet_accessible = False
        values = {
            'page_name': page_name,
            'timesheet': timesheet,
            'user': request.env.user,
            'sheet_accessible': sheet_accessible,
        }
        return self._get_page_view_values(timesheet, access_token, values, history, False, **kwargs)
    
    def _sheet_get_page_view_values(self, sheet, access_token, **kwargs):
        values = {
            'sheet': sheet,
            'timesheets': sheet.timesheet_line_ids,
            'token': access_token,
            'return_url': '/shop/payment/validate',
            'bootstrap_formatting': True,
        #    'partner_id': order.partner_id.id,
            'report_type': 'html',
            #'action': order._get_portal_return_action(),
        }
        #if order.company_id:
        #    values['res_company'] = order.company_id

        #if order.has_to_be_paid():
        #    domain = expression.AND([
        #        ['&', ('state', 'in', ['enabled', 'test']), ('company_id', '=', order.company_id.id)],
        #        ['|', ('country_ids', '=', False), ('country_ids', 'in', [order.partner_id.country_id.id])]
        #    ])
        #    acquirers = request.env['payment.acquirer'].sudo().search(domain)

        #    values['acquirers'] = acquirers.filtered(lambda acq: (acq.payment_flow == 'form' and acq.view_template_id) or
        #                                             (acq.payment_flow == 's2s' and acq.registration_view_template_id))
        #    values['pms'] = request.env['payment.token'].search([('partner_id', '=', order.partner_id.id)])
        #    values['acq_extra_fees'] = acquirers.get_acquirer_extra_fees(order.amount_total, order.currency_id, order.partner_id.country_id.id)

        #if order.state in ('draft', 'sent', 'cancel'):
        history = request.session.get('my_timelogs_history', [])
        #else:
        #    history = request.session.get('my_orders_history', [])
        values.update(get_records_pager(history, sheet))

        return values
    
    # ------------------------------------------------
    # ---------Project & task render values ----------
    # ------------------------------------------------
    def _get_project_task_render_values(self, kw, render_values):
        '''
        This method provides fields related to the project to render the website sale form
        '''
        
        #values = render_values['portal_timesheet_page']
        
        #project = request.env['project.project'].browse(int(values['project_id']))
        #project = project and project.exists()
        projects = request.env['project.project'].search([])
        type_ids = request.env['hr.timesheet.type'].sudo().search([])
        
        

        res = {
            #'project': project,
            'task_ids': projects.get_website_sale_tasks(),
            'projects': projects.get_website_sale_projects(),
            'type_ids': type_ids,
        }
        return res
    
    
    @http.route(['/my/timelog/<int:sheet_id>'], type='http', auth="public", website=True)
    def portal_timesheet_page(self, sheet_id=None, access_token=None, message=False, download=False, **kw):

        try:
            #sheet_sudo = self._document_check_access('hr.timesheet.sheet', sheet_id, access_token=access_token)
            sheet_sudo = request.env['hr.timesheet.sheet'].sudo().search([('id', '=', int(sheet_id))])
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        type_list = [];
        project_list = [];
       
        if sheet_sudo:
            # store the date as a string in the session to allow serialization
            now = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_request_%s' % sheet_sudo.id)
            if session_obj_date != now and request.env.user.share and access_token:
                request.session['view_request_%s' % sheet_sudo.id] = now
                body = _('Quotation viewed by customer %s', sheet_sudo.employee_id.name)
                _message_post_helper(
                    "hr.timesheet.sheet",
                    sheet_sudo.id,
                    body,
                    token=sheet_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    #partner_ids=sheet_sudo.user_id.sudo().partner_id.ids,
                )
        
        values = self._sheet_get_page_view_values(sheet_sudo, access_token, **kw)
        
        
        render_values = {
            #'project_id': project_id,
            #'error': errors,
            'callback': kw.get('callback'),
        }
        values.update(self._get_project_task_render_values(kw, render_values))
        
        type_obj = request.env['hr.timesheet.type'].sudo().search([])
        for type in type_obj:
            type_list.append({
                'name': type.name, 
                'id': type.id
            })
        values['type_list'] = type_list
        
        project_obj = request.env['project.project'].sudo().search([])
        for project in project_obj:
            project_list.append({
                'name': project.name, 
                'id': project.id
            })
        values['project_list'] = project_list
        
        values['message'] = message
        message = kw.get('decline_message')
        
       
        return request.render('de_timesheet_portal.portal_my_timelog', values)
    
    # --------------------------------------------
    # ------------- Submit Request ---------------
    # --------------------------------------------
    @http.route([
        '/my/timelog/submit/<int:sheet_id>',
        #'/my/timelog/delete/<int:timesheet_id>/<access_token>',
    ], type='http', auth="public", website=True)
    def sheet_submit(self, sheet_id=None, access_token=None, **kw):
        try:
            sheet_sudo = self._document_check_access('hr.timesheet.sheet', sheet_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        #sheet = request.env['hr.timesheet.sheet'].sudo().browse(int(sheet_id))
        if sheet_sudo:
            sheet_sudo.sudo().action_submit_sheet()
        return request.redirect('/my/timelog/%s' % (sheet_sudo.id))
    
    
    # --------------------------------------------
    # ------------- Accept Request ---------------
    # --------------------------------------------
    @http.route([
        '/my/timelog/approve/<int:sheet_id>',
        '/my/timelog/delete/<int:sheet_id>/<access_token>',
    ], type='http', auth="public", website=True)
    def sheet_approve(self, sheet_id=None, access_token=None, **kw):
        try:
            sheet_sudo = self._document_check_access('hr.timesheet.sheet', sheet_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        sheet_sudo = request.env['hr.timesheet.sheet'].sudo().browse(int(sheet_id))
        if sheet_sudo:
            sheet_sudo.sudo().action_approve()
        return request.redirect('/my/timelog/%s' % (sheet_sudo.id))
    
    # ------------------------
    # Reject request
    # ------------------------
    @http.route([
        '/my/timelog/reject/<int:sheet_id>',
        '/my/timelog/reject/<int:sheet_id>/<access_token>',
    ], type='http', auth="public", website=True)
    def request_reject(self, sheet_id=None, access_token=None, **kw):
        try:
            sheet_sudo = self._document_check_access('hr.timesheet.sheet', sheet_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        #if not sheet_sudo.team_id.allow_portal_ticket_closing:
        #    raise UserError(_("The team does not allow ticket closing through portal"))

        #if not ticket_sudo.closed_by_partner:
        #    closing_stage = ticket_sudo.team_id._get_closing_stage()
        #    if ticket_sudo.stage_id != closing_stage:s
        #        ticket_sudo.write({'stage_id': closing_stage[0].id, 'closed_by_partner': True})
        #    else:
        #sheet_sudo.write({'stage_id': 4})
        body = _('request rejected')
        sheet_sudo.with_context(mail_create_nosubscribe=True).message_post(body=body, message_type='comment', subtype_xmlid='mail.mt_note')
        
        message = kw.get('decline_message')

        query_string = False
        sheet_sudo.action_refuse()
        if message:
            sheet_sudo.action_refuse()
            _message_post_helper('hr.timesheet.sheet', sheet_id, message, **{'token': access_token} if access_token else {})
        else:
            query_string = "&message=cant_reject"

        return request.redirect('/my/timelog/%s' % (sheet_id))
    
    # ------------------------
    # Update  request
    # ------------------------
    @http.route([
        '/my/timelog/edit/<int:sheet_id>',
        '/my/timelog/edit/<int:sheet_id>/<access_token>',
    ], type='http', auth="public", website=True)
    def update_request(self, sheet_id=None, access_token=None, **kw):
        try:
            sheet_sudo = self._document_check_access('hr.timesheet.sheet', sheet_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        timesheet = request.env['account.analytic.line']
        values = {}
        timesheet_id = kw.get('timesheet_id')
        if timesheet_id:
            timesheet = request.env['account.analytic.line'].sudo().search([('id','=',int(timesheet_id))],limit=1)
        values = {
            'name': kw.get('name')
        }
        timesheet.write(values)

        return request.redirect('/my/timelog/%s' % (sheet_id))
    
    # ------------------------
    # Delete  request
    # ------------------------
    #@http.route(['/action/delete/line/<int:line_id>'], type='http', auth="public", website=True)
    #def action_stock_delete_line(self, line_id , access_token=None, **kw): 
    #    recrd = request.env['stock.transfer.order.line'].sudo().browse(line_id)
    #    material_id = recrd.stock_transfer_order_id.id
    #    task_sudo = request.env['stock.transfer.order'].sudo().search([('id', '=', material_id)])
    #    recrd.unlink()
    #    values = self._stock_material_get_page_view_values(task_sudo, access_token, **kw)
    #    return request.render("de_portal_stock_material_transfer.portal_stock_material", values)
    
    @http.route([
        '/my/timelog/delete/<int:timesheet_id>',
        #'/my/timelog/delete/<int:timesheet_id>/<access_token>',
    ], type='http', auth="public", website=True)
    def timesheet_delete(self, timesheet_id=None, access_token=None, **kw):
        #try:
        #    sheet_sudo = self._document_check_access('hr.timesheet.sheet', sheet_id, access_token)
        #except (AccessError, MissingError):
        #    return request.redirect('/my')
        
        timesheet = request.env['account.analytic.line'].sudo().browse(int(timesheet_id))
        if timesheet:
            sheet_sudo = request.env['hr.timesheet.sheet'].sudo().search([('id', '=', int(timesheet.sheet_id.id))],limit=1)
            timesheet.sudo().unlink()
        

        #raise ValidationError(_(timesheet.id))
        
        #timesheet.action_delete()
        
        #timesheet_id = kw.get('timesheet_id')
        #raise ValidationError(_(timesheet))
        #if timesheet_id:
        #    timesheet = request.env['account.analytic.line'].sudo().search([('id','=',int(timesheet_id))],limit=1)
        #    timesheet.action_delete()
            #timesheet.unlink()
        #values = self._sheet_get_page_view_values(sheet_sudo, access_token, **kw)
        #return request.render('de_timesheet_portal.portal_my_timelog', values)
        return request.redirect('/my/timelog/%s' % (sheet_sudo.id))
    
    @http.route([
        '/my/timelog/add',
    ], type='http', auth="public", website=True)
    def timesheet_add(self, **kw):
        employee_id = request.env['hr.employee'].sudo().search([('user_id','=',http.request.env.context.get('uid'))])
        vals = {
            'employee_id': employee_id.id,
            'name': kw.get('name'),
            'date': fields.date.today(),
        }
        sheet_id = request.env['hr.timesheet.sheet'].sudo().create(vals)
        return request.redirect('/my/timelog/%s' % (sheet_id.id))
    
    @http.route([
        '/my/timelog/add/line',
        #'/my/timelog/add/line/<int:sheet_id>',
        #'/my/timelog/add/line/<int:sheet_id>/<access_token>',
    ], type='http', auth="public", website=True)
    #@http.route('/my/timelog/add/line/<int:timesheet_id>', type='http', csrf=False, auth="public", website=True)
    def timesheet_add_line(self, **kw):
        #sheet = request.env['hr.timesheet.sheet'].sudo().search([('id', '=', int(sheet_id))],limit=1)
        #sheet = request.env['hr.timesheet.sheet'].sudo().browse(int(sheet_id))
        sheet = request.env['hr.timesheet.sheet'].sudo().browse(int(kw.get('sheet_id')),)
        vals = {}
        if kw.get('vals'):
            for line in kw.get('vals'):
                vals = {
                    'sheet_id': sheet.id,
                    'project_id': int(line['project_id']),
                    'task_id': int(line['task_id']),
                    'name': line['name'] or 'this is test',
                    #'product_uom_qty': int(line['sheet_id']),
                    'unit_amount_from': int(line['unit_amount_from']),
                    'unit_amount_to': int(line['unit_amount_to']),
                    'unit_amount': int(line['unit_amount_to'])-int(line['unit_amount_from']),
                    'date': fields.date.today(),
                    'employee_id': sheet.employee_id.id
                }
        vals = {
            'sheet_id': sheet.id,
            'project_id': int(kw.get('project_id')),
            #'task_id': int(kw.get('task_id')),
            'timesheet_type_id': int(kw.get('task_id')),
            'name': kw.get('name'),
            #'product_uom_qty': int(line['sheet_id']),
            'unit_amount_from': float(kw.get('unit_amount_from')),
            'unit_amount_to': float(kw.get('unit_amount_to')),
            'unit_amount': float(kw.get('unit_amount_to')) - float(kw.get('unit_amount_from')),
            'date': kw.get('date'),
            'employee_id': sheet.employee_id.id
        }
        timesheet_id = request.env['account.analytic.line'].sudo().create(vals)
        return request.redirect('/my/timelog/%s' % (sheet.id))

    
