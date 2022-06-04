# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import psycopg2


class AccountSyncConnector(models.Model):
    _name = 'account.sync.connector'
    _desciption = 'Account Sync Connector'
    
    query = fields.Char(string='Query')
    type = fields.Selection(selection=[
            ('send', 'Send'),
            ('view', 'View'),
        ], string='Type',
        default='send')
    host = fields.Char(string='Host/IP', required=True)
    username = fields.Char(string='Postgres Username', required=True)
    password = fields.Char(string='Postgres Password', required=True)
    database = fields.Char(string="Database", required=True)
    
    def action_post_data(self):
        for line in self:
            conn = psycopg2.connect(
              host=self.host,
              database=self.database,
              user=self.username,
              password=self.password)
            cur = conn.cursor()
            statement=self.query
            cur.execute(statement)
            cur.commit()
            cur.close()
            

    
