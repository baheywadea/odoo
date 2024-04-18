# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import common



@common.tagged('post_install', '-at_install')
class TestPropertyComplaint(common.TransactionCase):

    def setUp(self):
        super(TestPropertyComplaint, self).setUp()
        self.ResPartner = self.env['res.partner']
        self.ComplaintType = self.env['complaint.type']
        self.PropertyComplaint = self.env['property.complaint']

        self.partner_test = self.env['res.partner'].create({
            'name': 'My Test Customer',
            'email': 'bahey.wadea@gmail.com',
            'street': 'str1',
            'street2': 'str2',
            'city': 'testCity',
            'tenant': True})

        self.employee_test = self.env['hr.employee'].sudo().search([])[0]
        self.property_complaint = self.env['property.complaint'].create({
            'partner_id': self.partner_test.id,
            'type': self.env.ref('bloopark_realestate.complaint_type_question').id,
            'assign_to': self.employee_test.id,
            'customer_house_no': 'Test House No',
            'customer_Flat_no': 'Test Flat No',
            'customer_description': 'Test Description',

        })

    def test_00_send_order_confirmation_mail(self):
        # In order to test complaint
        # Create complaint and create partner and then send email

        self.partner_test = self.env['res.partner'].create({
            'name': 'My Test Customer',
            'email': 'bahey.wadea@gmail.com',
            'street': 'str1',
            'street2': 'str2',
            'city': 'testCity',
            'tenant': True})

        self.employee_test = self.env['hr.employee'].sudo().search([])[0]
        self.property_complaint = self.env['property.complaint'].create({
            'partner_id': self.partner_test.id,
            'type': self.env.ref('bloopark_realestate.complaint_type_question').id,
            'assign_to': self.employee_test.id,
            'customer_house_no': 'Test House No',
            'customer_Flat_no': 'Test Flat No',
            'customer_description': 'Test Description',

        })
        self.property_complaint._send_order_confirmation_mail()


    def test_00_confirm_complaint(self):
        # In order to test complaint
        # Create complaint and create partner and then confirm complaint

        self.partner_test = self.env['res.partner'].create({
            'name': 'My Test Customer',
            'email': 'bahey.wadea@gmail.com',
            'street': 'str1',
            'street2': 'str2',
            'city': 'testCity',
            'tenant': True})

        self.employee_test = self.env['hr.employee'].sudo().search([])[0]
        self.property_complaint = self.env['property.complaint'].create({
            'partner_id': self.partner_test.id,
            'type': self.env.ref('bloopark_realestate.complaint_type_question').id,
            'assign_to': self.employee_test.id,
            'customer_house_no': 'Test House No',
            'customer_Flat_no': 'Test Flat No',
            'customer_description': 'Test Description',

        })
        self.property_complaint.confirm_complaint()
