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
from odoo import models, fields, api, SUPERUSER_ID, _
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
    question_answer = fields.Text('Question Answer', tracking=True)

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

    def action_complaint_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()
        lang = self.env.context.get('lang')
        mail_template = self._find_mail_template()
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'property.complaint',
            'default_res_ids': self.ids,
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'force_email': True,
            'model_description': self.with_context(lang=lang).type.name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


    def _find_mail_template(self):
        """ Get the appropriate mail template for the current sales order based on its state.

        If the SO is confirmed, we return the mail template for the sale confirmation.
        Otherwise, we return the quotation email template.

        :return: The correct mail template based on the current status
        :rtype: record of `mail.template` or `None` if not found
        """
        self.ensure_one()
        return self.env.ref('bloopark_realestate.email_template_property_complaint', raise_if_not_found=False)

    def _send_order_confirmation_mail(self):
        """ Send a mail to the SO customer to inform them that their order has been confirmed.

        :return: None
        """
        for order in self:
            mail_template = order._find_mail_template()
            order._send_order_notification_mail(mail_template)

    def _send_order_notification_mail(self, mail_template):
        """ Send a mail to the customer

        Note: self.ensure_one()

        :param mail.template mail_template: the template used to generate the mail
        :return: None
        """
        self.ensure_one()

        if not mail_template:
            return

        if self.env.su:
            # sending mail in sudo was meant for it being sent from superuser
            self = self.with_user(SUPERUSER_ID)

        self.with_context(force_send=True).message_post_with_source(
            mail_template,
            email_layout_xmlid='mail.mail_notification_layout_with_responsible_signature',
            subtype_xmlid='mail.mt_comment',
        )


    _sql_constraints = [('uniq_name', 'unique(name)', "The name of this Property must be unique!")]