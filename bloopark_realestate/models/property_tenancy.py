# -*- coding: utf-8 -*-
# Part of BAHEY WADEA 2024. See LICENSE file for full copyright and licensing details.


import time
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


# this model handle the tenancy contract rent schedule depend on contract tenancy start date and end date
class tenancy_rent_schedule(models.Model):
	_name = "tenancy.rent.schedule"
	_rec_name = "tenancy_id"
	_order = 'start_date'

	note = fields.Text('Notes', help='Additional Notes.')

	amount = fields.Float(default=0.0, string='Amount', help="Rent Amount.")
	start_date = fields.Date('Date', help='Start Date.')
	end_date = fields.Date('End Date', help='End Date.')

	rel_tenant_id = fields.Many2one('res.partner', string="Tenant", ondelete='restrict', related='tenancy_id.tenant_id',
									store=True)

	property_id = fields.Many2one('property', 'Property', help='Property Name.', related='tenancy_id.property_id')

	tenancy_id = fields.Many2one('property.tenancy', 'Tenancy', help='Tenancy Name.')


# this model handle the tenancy contract details with tenant and specific property
class property_tenancy(models.Model):
	_name = "property.tenancy"
	_order = 'name'

	# can upload contract file of agreement to this tenancy contract
	contract_attachment = fields.Binary('Tenancy Contract')

	deposit_received = fields.Boolean(string='Deposit Received?',help="True if deposit amount received for current Tenancy.")
	deposit_return = fields.Boolean(string='Deposit Returned?',help="True if deposit amount returned for current Tenancy.")

	# the tenancy contract ref / name automaticaly generated depend on sequence
	name = fields.Char('Reference',
					   default=lambda self: self.env['ir.sequence'].next_by_code('realestate.property.tenancy'),
					   required=True, help="Unique Property Tenancy Number")


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
	_sql_constraints = [('uniq_name', 'unique(name)', "The name of this Property Tenancy must be unique!")]

	@api.depends('rent_schedule_ids', 'rent_schedule_ids.amount')
	def _total_amount_rent(self):
		"""
        This method is used to calculate Total Rent of current Tenancy.
        @param self: The object pointer
        @return: Calculated Total Rent.
        """
		tot = 0.00
		if self.rent_schedule_ids and self.rent_schedule_ids.ids:
			for propety_brw in self.rent_schedule_ids:
				tot += propety_brw.amount
		self.total_rent = tot

