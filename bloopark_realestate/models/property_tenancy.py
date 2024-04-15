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


class tenancy_rent_schedule(models.Model):
	_name = "tenancy.rent.schedule"
	_rec_name = "tenancy_id"
	_order = 'start_date'


	note = fields.Text('Notes', help='Additional Notes.')

	amount = fields.Float(default=0.0, string='Amount', help="Rent Amount.")
	start_date = fields.Date('Date', help='Start Date.')
	end_date = fields.Date('End Date', help='End Date.')

	rel_tenant_id = fields.Many2one('res.partner', string="Tenant", ondelete='restrict',related='tenancy_id.tenant_id', store=True)

	property_id = fields.Many2one('property', 'Property', help='Property Name.',related='tenancy_id.property_id')

	tenancy_id = fields.Many2one('property.tenancy', 'Tenancy', help='Tenancy Name.')





class property_tenancy(models.Model):
	_name = "property.tenancy"
	_order='ref'

	contract_attachment = fields.Binary('Tenancy Contract')


	deposit_received = fields.Boolean(compute='_get_deposit', method=True, default=False, multi='deposit',
									  string='Deposit Received?',
									  help="True if deposit amount received for current Tenancy.")
	deposit_return = fields.Boolean(compute='_get_deposit', method=True, default=False, multi='deposit', type='boolean',
									string='Deposit Returned?',
									help="True if deposit amount returned for current Tenancy.")
	ref = fields.Char('Reference')

	date = fields.Date('Expiration Date', select=True, help="Tenancy contract end date.")
	date_start = fields.Date('Start Date', default=lambda *a: time.strftime(DEFAULT_SERVER_DATE_FORMAT),
							 help="Tenancy contract start date .")

	amount_fee_paid = fields.Integer('Amount of Fee Paid')
	manager_id = fields.Many2one('hr.employee', 'Account Manager', help="Manager of Tenancy.")
	property_id = fields.Many2one('property', 'Property', help="Name of Property.")
	tenant_id = fields.Many2one('res.partner', 'Tenant', domain="[('tenant', '=', True)]",
								help="Tenant Name of Tenancy.")
	contact_id = fields.Many2one('res.partner', 'Contact', help="Contact person name.")

	rent_schedule_ids = fields.One2many('tenancy.rent.schedule', 'tenancy_id', 'Rent Schedule')


	rent = fields.Float(default=0.0, string='Tenancy Rent Amount', help="Tenancy rent for selected property per Month.")

	deposit = fields.Float(default=0.0, string='Deposit', help="Deposit amount for Tenancy.")

	total_rent = fields.Float(compute='_total_amount_rent', string='Total Rent', readonly=True, store=True,
								 help='Total rent of this Tenancy.')

	amount_return = fields.Float(default=0.0, string='Deposit Returned', help="Deposit Returned amount for Tenancy.")


	description = fields.Text('Description', help='Additional Terms and Conditions')

	duration_cover = fields.Text('Duration of Cover', help='Additional Notes')

	rent_type_id = fields.Many2one('rent.type', 'Rent Type')

	deposit_scheme_type = fields.Selection([('insurance', 'Insurance-based'), ], 'Type of Scheme')

	state = fields.Selection([('template', 'Template'), ('draft', 'New'), ('open', 'In Progress'),
							  ('pending', 'To Renew'), ('close', 'Closed'), ('cancelled', 'Cancelled')],
							 'Status', required=True, copy=False, default='draft')