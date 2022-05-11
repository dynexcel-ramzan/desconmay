import json
from odoo import models
from odoo.exceptions import UserError


class OnExpenseSheetReport(models.AbstractModel):
    _name = 'report.de_expense_reports.on_expense_sheet_report'
    _description = 'On Expense  Sheet Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        data = self.env['expense.sheet.wizard'].browse(self.env.context.get('active_ids'))
        sheet = workbook.add_worksheet('Expense Report ')
        bold = workbook. add_format({'bold': True, 'align': 'center','bg_color': '#8CBDD6','border': True})
        title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14, 'border': True})
        header_row_style = workbook.add_format({'bold': True, 'align': 'center', 'border':True})
        format2 = workbook.add_format({'align': 'center'})
        format3 = workbook.add_format({'align': 'center','bold': True,'border': True,})   
        
        
        format4 = workbook.add_format({'num_format': '* "-"??;(@_)', 'fg_color': '#dfe4e4'})
        
      
        
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 1, 20)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 20)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 20)
        row = 6
        col = 0
        
        sheet.write('A1:A1',  data.company_id.name ,header_row_style)
        sheet.write('A2:A2',  str(data.date_from.strftime('%d-%b-%Y')) ,header_row_style)
        
        
        

        sheet.write(5,0,'Employees Name', bold)
        sheet.write(5,1 , 'Voucher#',bold)
        sheet.write(5,2 , "Status",bold)
        sheet.write(5,3 , "Amount (PKR)",bold)
    
        
        total_submited_amount = 0
        
        exp = self.env['hr.expense.sheet'].search([('company_id','=', data.company_id.id),('accounting_date','>=',data.date_from), ('accounting_date','<=',data.date_to)])
        for line in exp:
            total_submited_amount += line.total_amount
            
            sheet.write(row, 0, line.employee_id.name, format2)
            sheet.write(row, 1, line.name, format2)
            sheet.write(row, 2, line.state, format2)
            sheet.write(row, 3, line.total_amount, format2)
            row += 1
            
            
        sheet.write(row,0,'Total', bold)
        sheet.write(row,1 , '',bold)
        sheet.write(row,2,'', bold)
        sheet.write(row,3, total_submited_amount, bold)
        
        
    
        
        
        