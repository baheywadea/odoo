# -*- coding: utf-8 -*-
# Part of BAHEY WADEA 2024. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError



# complaint type models help to add ny type in futue and not static type
class complaint_type(models.Model):
    _name = 'complaint.type'

    name = fields.Char('Maintenance Type', size=50, required=True)




# complaint models contains the customer details and complaint details
# and what intervention needed and happend
class property_complaint(models.Model):
    _name = "property.complaint"
    _inherit = ['mail.thread']

    # complaint name / No created automaically depend on sequence for complaint
    name = fields.Char(string="Complaint No",
                       default=lambda self: self.env['ir.sequence'].next_by_code('realestate.property.complaints'),
                       required=True, help="Unique Property Complaint Number", tracking=True )
    # relate the customer record data to complaint
    partner_id = fields.Many2one('res.partner',string="Contact", tracking=True)
    # the date of customer complaint
    date = fields.Datetime('Date', default=fields.Datetime.now, tracking=True)

    # relate the complaint with type
    type = fields.Many2one('complaint.type', 'Type',required=True, tracking=True)
    # relate the complaint with assigned employee
    assign_to = fields.Many2one('hr.employee', 'Assign To', tracking=True)

    # mail_check = fields.Boolean('Mail Send', default=False)
    # property_id = fields.Many2one('property','Property')
    # here the customer issue described from website form or if is this question
    customer_description = fields.Text('Customer Description', tracking=True)
    # relate email from customer email to complaint to make easy read for customer service
    customer_email = fields.Char('Customer Email',related="partner_id.email",readonly=False, required=True, tracking=True)
    # customer_name = fields.Text('Customer Name', required=True, tracking=True)

    # relate email from customer address to complaint to make easy read for customer service
    customer_street = fields.Char('Customer Street',related="partner_id.street",readonly=False,  required=True, tracking=True)
    customer_street2 = fields.Char('Customer Street2',related="partner_id.street2",readonly=False, )
    customer_city = fields.Char('Customer City',related="partner_id.city",readonly=False,  required=True, tracking=True)
    # customer_country = fields.Many2one('res.country', string='Customer Country', required=True)
    customer_house_no = fields.Text('Customer House No', required=True, tracking=True)
    customer_Flat_no = fields.Text('Customer Flat No', required=True, tracking=True)

    # here customer service add the action plan to solve the customer complaint
    action_plan = fields.Text('Action Plan', tracking=True)

    # here customer service add answer of customer question if type is question
    question_answer = fields.Text('Question Answer', tracking=True)

    # here the complaint states for each step
    state = fields.Selection(
        [('New', 'New'), ('In Review', 'In Review'), ('In Progress', 'In Progress'), ('Solved', 'Solved'),
         ('Dropped', 'Dropped')],
        'State', default='New')


    def confirm_complaint(self):
        """" Confirm the complaint if the state it's new and tell the customer service
        to enter action plan if there's no action plan then change the state to be In Review
        but in case the type of complaint is Question Customer service has to enter the answer
        of customer questiont and then change the state to be solved.
        """
        for rec in self:
            if rec.type.name == "Question":
                if not rec.question_answer:
                    raise UserError(
                        _('Please Answer the customer question before confirm'))
                else:
                    rec.write({'state': 'Solved'})
            else:
                if not rec.action_plan:
                    raise UserError(
                        _('Please Write The Action Plan ' ))
                else:
                    rec.write({'state':'In Review'})

    def confirm2_complaint(self):
        """" After the complaint be In Review state May be the work operation
        will work on it so can be change the state to be In Progress
                """
        for rec in self:
            rec.write({'state':'In Progress'})

    def mark_as_done(self):
        """" After the complaint be In Progress state May be the work operation
                has been solved so can be change the state to be solved
                        """
        for rec in self:
            rec.write({'state':'Solved'})

    def drop_it(self):
        """" Here the customer service can change the state of complaint to be dropped
        for dublicate issue or other things also can be dropped if the state in New Only
                                """
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
        """ Get the appropriate mail template for the current complaint based on its state.
        """
        self.ensure_one()
        return self.env.ref('bloopark_realestate.email_template_property_complaint', raise_if_not_found=False)

    def _send_order_confirmation_mail(self):
        """ Send a mail to the complaint customer to inform them that their order has been received.

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