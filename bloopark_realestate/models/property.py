# -*- coding: utf-8 -*-
# Part of BAHEY WADEA 2024. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _



# Add fields to partner (Contact) to distinguish this contac is tenant not normal contact
class res_partner(models.Model):
    _inherit = "res.partner"

    tenant = fields.Boolean('Tenant', help="Check this box if this contact is a tenant.")


# This model for rent type like monthly or quartly ... etc
class rent_type(models.Model):
    _name = "rent.type"
    _order = 'name'

    name = fields.Char(string="Name", required=True)
    duration = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                                 ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')])
    renttype = fields.Selection([('Month', 'Month(S)'), ('Year', 'Year(S)')])


# This model for property type like Residential Flat, Office, Villa ,etc
class property_type(models.Model):
    _name = "property.type"

    name = fields.Char('Name', size=50, required=True)

# This model for room type like Master Room , Children Room , Dining room , etc
class room_type(models.Model):
    _name = "room.type"

    name = fields.Char('Name', size=50, required=True)


# This model for room asset like T.V , Heating ,etc and handle the qty there and the type of assets
class room_assets(models.Model):
    _name = "room.assets"

    date = fields.Date('Date')
    name = fields.Char('Description', size=60, required=True)
    type = fields.Selection([('fixed', 'Fixed Assets'), ('movable', 'Movable Assets'), ('other', 'Other Assets')],
                            'Type')
    qty = fields.Float('Quantity')
    room_id = fields.Many2one('property.room', 'Property')



# This model for property room details like (Width , Height , Length) and relate the room type and with assets ,
# Also can add attachment file to this room (like , plan or photo)
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


# This model for property photos details l
class property_photo(models.Model):
    _name = "property.photo"

    photos = fields.Binary('Photos')
    doc_name = fields.Char('Filename')
    photos_description = fields.Char('Description')
    photo_id = fields.Many2one('property', 'Property')



# This model for property details like Reference No
class property(models.Model):
    _name = 'property'
    _description = 'Property'

    active = fields.Boolean(string="Active", default=True)

    # Name or Reference No created automaticallly by sequence for each property no need to manual enter
    name = fields.Char('Name / Reference',
                       default=lambda self: self.env['ir.sequence'].next_by_code('realestate.property'), required=True,
                       help="Unique Property Number")

    # The Property Main Image
    image = fields.Binary('Image')
    note = fields.Text('Notes', help='Additional Notes.')

    # The PropertyAddress details
    city = fields.Char('City')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', size=24, change_default=True)
    country_id = fields.Many2one('res.country', 'Country')
    state_id = fields.Many2one("res.country.state", 'State')

    # Relate The property with type  details
    type_id = fields.Many2one('property.type', 'Property Type', help='Property Type.')
    # Relate The property with Rooms Detals
    room_ids = fields.One2many('property.room', 'property_id', 'Rooms')

    # Relate The property with Manager (from Employees Records Can Select)
    property_manager = fields.Many2one('hr.employee', 'Property Manager', help="Manager of Property (Employee).")
    # Relate The property With Multi Photos
    property_photo_ids = fields.One2many('property.photo', 'photo_id', 'Photos')

    # Add the Number of bedroom of this property
    bedroom = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5+')], 'Bedrooms', default='1')
    # Add the Number of bathroom of this property
    bathroom = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5+')], 'Bathrooms', default='1')

    # Add the rent amount of property
    ground_rent = fields.Float('Ground Rent', help='Ground rent of Property.')
    # Add the Gross floor area in Meter.
    gfa_meter = fields.Float('GFA(m)', help='Gross floor area in Meter.')

    # if property rented we will calculated the current tenant
    current_tenant_id = fields.Many2one('res.partner', 'Current Tenant')
    # Relate the property with rent type to help in tenancy record in future to be auto and also can modified
    rent_type_id = fields.Many2one('rent.type', 'Rent Type')

    # complaint_ids = fields.One2many('property.complaint', 'property_id', 'Maintenance')

    facing = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], 'Facing',
                              default='east')
    furnished = fields.Selection([('none', 'None'), ('semi_furnished', 'Semi Furnished'),
                                  ('full_furnished', 'Full Furnished')], 'Furnishing', default='none',
                                 help='Furnishing.')

    # The state of property like free to be rent or when it be rented will be on lease or if sold or booked only
    state = fields.Selection(
        [('new_draft', 'Booking Open'), ('draft', 'Available'), ('book', 'Booked'), ('normal', 'On Lease'),
         ('close', 'Sale'), ('sold', 'Sold'), ('cancel', 'Cancel')], 'State',
        required=True, default='draft')

    # Here constraint to make property name / ref unique and not be dublicated
    _sql_constraints = [('uniq_name', 'unique(name)', "The name of this Property must be unique!")]
