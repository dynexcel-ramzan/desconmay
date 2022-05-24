# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import OrderedDict
from operator import itemgetter

from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
import json
import base64
from odoo.tools import groupby as groupbyelem

from odoo.osv.expression import OR
from odoo.addons.web_editor.models.ir_qweb import Integer


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'timesheet_report_count' in counters:
            values['timesheet_report_count'] = request.env['hr.timesheet.sheet'].search_count([])
        return values

    def _project_get_page_view_values(self, project, access_token, **kwargs):
        values = {
            'page_name': 'admission',
            'admission': project,
        }
        return self._get_page_view_values(project, access_token, values, 'my_projects_history', False, **kwargs)

    @http.route(['/my/timelogs', '/my/timelogs/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_timelogs(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Project = request.env['hr.timesheet.sheet']
        domain = []

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # projects count
        admission_count = Project.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/timelogs",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=admission_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        projects = Project.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_projects_history'] = projects.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'sheets': projects,
            'page_name': 'admission',
            'default_url': '/my/timelogs',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("de_timesheet_portal.portal_my_timelogs", values)

    @http.route(['/my/timelog/<int:sheet_id>'], type='http', auth="public", website=True)
    def portal_my_timelog(self, sheet_id=None, access_token=None, **kw):
        sheet_obj = request.env['hr.timesheet.sheet'].sudo().search([('id', '=', int(sheet_id))])
        if 'next_date_deadline' in kw:
            print("this is the activity ")
            date_deadline = kw['next_date_deadline']
            summary = kw['summary']
            # kw.pop['summary']
            kw.pop("next_date_deadline")
            
            
        
        if 'stage_id' in kw:
            kw['stage_id'] = int(kw['stage_id'])
            write_record = addmission_obj.sudo().write(kw)
            
            
        sheet = request.env['hr.timesheet.sheet'].sudo().search([('id', '=', int(sheet_id))])
        
        return request.render("de_timesheet_portal.portal_my_timelog", {'id': sheet.id,
                                                                          'stage_id': sheet.stage_id,
                                                                          })


#############Sync code################
class Admission(http.Controller):

    @http.route('/admission_webform', type="http", auth="public", website=True)
    def admission_webform(self, **kw):
        company_id = request.env['res.company'].sudo().search([])
        country_id = request.env['res.country'].sudo().search([])
        relation = request.env['op.relation'].sudo().search([])
        crm_admission_register_id = request.env['op.school.crm.admission.register'].sudo().search([])
        course_id = request.env['oe.school.course'].sudo().search([])
        return http.request.render('de_school_admission.create_admission', {
            'company_id': company_id,
            'country_id': country_id,
            'relation':relation,
            'state_id': country_id,
            'crm_admission_register_id': crm_admission_register_id,
            'course_id': course_id,
        })

    @http.route('/create/webadmissionss', type="http", auth="public", website=True)
    def create_webadmission(self, **kw):
        try:
            print("thisithis isi kw",kw)
            print("Family list --------------",kw['crm_lead_edu_history_id'])
            print("Education list --------------", kw['applicant_relation_ids'])


            edcat_hsty_lst = []; famy_hsty_lst =[]
            edcat_hsty_ls = kw['crm_lead_edu_history_id'];famy_hsty_ls = kw['applicant_relation_ids']
            print("Family list----------",famy_hsty_ls)
            edcat_hsty_ls = json.loads(edcat_hsty_ls)
            famy_hsty_ls = json.loads(famy_hsty_ls)
            for dict in famy_hsty_ls:
                if dict:
                    famy_hsty_lst.append((0, 0, dict))
            for dict in edcat_hsty_ls:
                if dict:
                    edcat_hsty_lst.append((0, 0, dict))
            kw['crm_lead_edu_history_id'] = edcat_hsty_lst
            kw['applicant_relation_ids'] = famy_hsty_lst
            if kw.get('crm_admission_register_id'):
                crm_adm_id = kw['crm_admission_register_id']
                crm_adm_obj = request.env['op.school.crm.admission.register'].sudo().search([('id', '=', crm_adm_id)])
                kw['course_id'] = int(crm_adm_obj.course_id)
            print("This is the port addmision kw", kw)
            
            if kw.get('student_image'):
                image = kw.get('student_image').read()
                print("student image...", image)
                kw['student_image'] = base64.b64encode(image)
            create_record = request.env['crm.lead'].sudo().create(kw)
            if create_record:
                return request.render("de_school_admission.student_thanks",{'apl_no':create_record.reference})
        except:
            return request.render("de_school_admission.student_attempt_failed",{})

    @http.route('/create/webadmissions_editoooollldd', type="http", auth="public", website=True)
    def edit_webadmission(self, **kw):
        print("This is the web admission model", kw)
        if kw.get('id'):
            admission_id = kw['id']
            addmission_obj = request.env['crm.lead'].sudo().search([('id', '=', int(admission_id))])
        kw.pop("id")
        # kw.pop("course_id")
        kw['course_id'] = int(kw['course_id'])
        write_record = addmission_obj.sudo().write(kw)
        
        
        
        
        
        
        
        
        
        
        
        print("JJJJJJJJJJJJthe operation the web admission model", write_record)
        if write_record:
            admission = request.env['crm.lead'].sudo().search([('id', '=', int(admission_id))])
            course_ids = request.env['oe.school.course'].sudo().search([])
            return request.render("de_school_admission.portal_my_admission", {'id': admission.id,
                                                                              'expected_revenue': admission.expected_revenue,
                                                                              'company_id': admission.company_id,
                                                                              'phone': admission.phone,
                                                                              'user_id': admission.user_id,
                                                                              'reference': admission.reference,
                                                                              'name': admission.name,
                                                                              'stage_id': admission.stage_id,
                                                                              'partner_id': admission.partner_id,
                                                                              'course_id_name': admission.course_id.name,
                                                                              'email_from': admission.email_from,
                                                                              'team_id': admission.team_id,
                                                                              'priority': admission.priority,
                                                                              'street': admission.street,
                                                                              'activity_ids': admission.activity_ids,
                                                                              'email_from': admission.email_from,
                                                                              'team_id': admission.team_id,
                                                                              'priority': admission.priority,
                                                                              'course_ids': course_ids
                                                                              })
