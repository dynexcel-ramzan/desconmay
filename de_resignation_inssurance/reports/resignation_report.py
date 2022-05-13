import json
from odoo import models
from odoo.exceptions import UserError

class ResignationReport(models.AbstractModel):
    _name = 'report.de_resignation_inssurance.resignation_report_xlx'
    _description = 'Resignation Inssurance Report'
    _inherit = 'report.report_xlsx.abstract'
    
    
    def generate_xlsx_report(self, workbook, data, lines):
        data = self.env['resignation.inssurance.wizard'].browse(self.env.context.get('active_ids'))
        format1 = workbook.add_format({'font_size': '12', 'align': 'center', 'bold': False})
        format2 = workbook.add_format({'font_size': '12', 'align': 'center', 'bold': False})
        sheet = workbook.add_worksheet('Employee Resignation Report')
        bold = workbook. add_format({'bold': True, 'align': 'center','border': True})
        sheet.set_column('A:A', 10,)
        sheet.set_column('B:B', 20,)
        sheet.set_column('C:D', 20,)
        sheet.set_column('E:F', 20,)
        sheet.set_column('G:G', 20,)
        sheet.set_column('H:H', 40,)
        sheet.set_column('I:I', 40,)
        sheet.set_column('I:J', 30,)
        sheet.set_column('K:L', 20,)
        sheet.set_column('M:N', 30,)
        sheet.write(0,3,str(data.start_date.strftime('%d-%b-%Y')),bold)
        sheet.write(0,5,str(data.end_date.strftime('%d-%b-%Y')),bold)
        employees=self.env['hr.employee'].search([('active','in',(False,True)),('resigned_date','>=',data.start_date),('resigned_date','<=',data.end_date),('company_id','=',data.company_id.id)], order='emp_type desc')
        sheet.write(1,0, 'SR#',bold)
        sheet.write(1,1, 'Name of Employee',bold)
        sheet.write(1,2, 'Date of Birth' ,bold)
        sheet.write(1,3, 'Designation' ,bold)
        sheet.write(1,4,'Category',bold)
        sheet.write(1,5,'CNIC Number' ,bold)
        sheet.write(1,6, 'Salary' ,bold)
        sheet.write(1,7, 'Addition Effective Date' ,bold)
       
        row = 2
        record_count=0
        for line in employees:
            sheet.write(row, 0, str(record_count), format1)
            sheet.write(row, 1, str(line.name), format1)
            sheet.write(row, 2, str(line.birthday), format1)
            sheet.write(row, 3, str(line.grade_designation.name if line.grade_designation else '-'), format1)
            sheet.write(row, 4, str(line.category_id.name if line.job_id else '-'), format1)
            sheet.write(row, 5, str(line.cnic), format1)
            sheet.write(row, 6,  format1)
            sheet.write(row, 7,  format1)
            
            row += 1 
            record_count += 1