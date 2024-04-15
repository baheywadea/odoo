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


class res_partner(models.Model):
    _inherit = "res.partner"

    tenant = fields.Boolean('Tenant', help="Check this box if this contact is a tenant.")


class rent_type(models.Model):
    _name = "rent.type"
    _order = 'name'

    name = fields.Char(string="Name", required=True)
    duration = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                                 ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')])
    renttype = fields.Selection([('Month', 'Month(S)'), ('Year', 'Year(S)')])


class property_type(models.Model):
    _name = "property.type"

    name = fields.Char('Name', size=50, required=True)


class complaint_type(models.Model):
    _name = 'complaint.type'

    name = fields.Char('Maintenance Type', size=50, required=True)


class room_type(models.Model):
    _name = "room.type"

    name = fields.Char('Name', size=50, required=True)


class room_assets(models.Model):
    _name = "room.assets"

    date = fields.Date('Date')
    name = fields.Char('Description', size=60, required=True)
    type = fields.Selection([('fixed', 'Fixed Assets'), ('movable', 'Movable Assets'), ('other', 'Other Assets')],
                            'Type')
    qty = fields.Float('Quantity')
    room_id = fields.Many2one('property.room', 'Property')


class property_room(models.Model):
    _name = "property.room"

    note = fields.Text('Notes')
    width = fields.Float('Width')
    height = fields.Float('Height')
    length = fields.Float('Length')
    image = fields.Binary('Picture')
    name = fields.Char('Name', size=60, required=True)
    attach = fields.Boolean('Attach Bathroom')
    type_id = fields.Many2one('room.type', 'Room Type')
    assets_ids = fields.One2many('room.assets', 'room_id', 'Assets')
    property_id = fields.Many2one('property', 'Property')


class property_photo(models.Model):
    _name = "property.photo"

    photos = fields.Binary('Photos')
    doc_name = fields.Char('Filename')
    photos_description = fields.Char('Description')
    photo_id = fields.Many2one('property', 'Property')


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


class property(models.Model):
    _name = 'property'
    _description = 'Property'

    active = fields.Boolean(string="Active", default=True)

    name = fields.Char('Name / Reference',
                       default=lambda self: self.env['ir.sequence'].next_by_code('realestate.property'), required=True,
                       help="Unique Property Number")
    image = fields.Binary('Image')
    note = fields.Text('Notes', help='Additional Notes.')

    city = fields.Char('City')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', size=24, change_default=True)
    country_id = fields.Many2one('res.country', 'Country')
    state_id = fields.Many2one("res.country.state", 'State')

    type_id = fields.Many2one('property.type', 'Property Type', help='Property Type.')
    room_ids = fields.One2many('property.room', 'property_id', 'Rooms')

    property_manager = fields.Many2one('hr.employee', 'Property Manager', help="Manager of Property (Employee).")
    property_photo_ids = fields.One2many('property.photo', 'photo_id', 'Photos')

    bedroom = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5+')], 'Bedrooms', default='1')
    bathroom = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5+')], 'Bathrooms', default='1')

    ground_rent = fields.Float('Ground Rent', help='Ground rent of Property.')
    gfa_meter = fields.Float('GFA(m)', help='Gross floor area in Meter.')

    current_tenant_id = fields.Many2one('res.partner', 'Current Tenant')
    rent_type_id = fields.Many2one('rent.type', 'Rent Type')

    # complaint_ids = fields.One2many('property.complaint', 'property_id', 'Maintenance')

    facing = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], 'Facing',
                              default='east')
    furnished = fields.Selection([('none', 'None'), ('semi_furnished', 'Semi Furnished'),
                                  ('full_furnished', 'Full Furnished')], 'Furnishing', default='none',
                                 help='Furnishing.')
    state = fields.Selection(
        [('new_draft', 'Booking Open'), ('draft', 'Available'), ('book', 'Booked'), ('normal', 'On Lease'),
         ('close', 'Sale'), ('sold', 'Sold'), ('cancel', 'Cancel')], 'State',
        required=True, default='draft')

    _sql_constraints = [('uniq_name', 'unique(name)', "The name of this Property must be unique!")]
