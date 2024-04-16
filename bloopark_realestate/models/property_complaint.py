# -*- coding: utf-8 -*-
##############################################################################
#
#	odoo, Open Source Management Solution
#	Copyright (C) 2011-Today Serpent Consulting Services PVT LTD
#	(<http://www.serpentcs.com>)
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
############################################################################

import time
from datetime import datetime
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError


class complaint_type(models.Model):
    _name = 'complaint.type'

    name = fields.Char('Maintenance Type', size=50, required=True)


class property_complaint(models.Model):
    _name = "property.complaint"
    _inherit = ['mail.thread']

    name = fields.Char(string="Complaint No",
                       default=lambda self: self.env['ir.sequence'].next_by_code('realestate.property.complaints'),
                       required=True, help="Unique Property Complaint Number", tracking=True )

    partner_id = fields.Many2one('res.partner',string="Contact", tracking=True)
    date = fields.Datetime('Date', default=fields.Datetime.now, tracking=True)
    type = fields.Many2one('complaint.type', 'Type',required=True, tracking=True)
    assign_to = fields.Many2one('hr.employee', 'Assign To', tracking=True)

    # mail_check = fields.Boolean('Mail Send', default=False)
    # property_id = fields.Many2one('property','Property')
    customer_description = fields.Text('Customer Description', tracking=True)
    customer_email = fields.Char('Customer Email',related="partner_id.email",readonly=False, required=True, tracking=True)
    # customer_name = fields.Text('Customer Name', required=True, tracking=True)
    customer_street = fields.Char('Customer Street',related="partner_id.street",readonly=False,  required=True, tracking=True)
    customer_street2 = fields.Char('Customer Street2',related="partner_id.street2",readonly=False, )
    customer_city = fields.Char('Customer City',related="partner_id.city",readonly=False,  required=True, tracking=True)
    # customer_country = fields.Many2one('res.country', string='Customer Country', required=True)
    customer_house_no = fields.Text('Customer House No', required=True, tracking=True)
    customer_Flat_no = fields.Text('Customer Flat No', required=True, tracking=True)
    action_plan = fields.Text('Action Plan', tracking=True)

    state = fields.Selection(
        [('New', 'New'), ('In Review', 'In Review'), ('In Progress', 'In Progress'), ('Solved', 'Solved'),
         ('Dropped', 'Dropped')],
        'State', default='New')

    def confirm_complaint(self):
        for rec in self:
            if not rec.action_plan or not rec.assign_to:
                raise UserError(
                    _('Please Write The Action Plan and assign the complaint to Employee' ))
            else:
                rec.write({'state':'In Review'})

    def confirm2_complaint(self):
        for rec in self:
            rec.write({'state':'In Progress'})

    def mark_as_done(self):
        for rec in self:
            rec.write({'state':'Solved'})

    def drop_it(self):
        for rec in self:
            rec.write({'state':'Dropped'})

    _sql_constraints = [('uniq_name', 'unique(name)', "The name of this Property must be unique!")]