# -*- coding: utf-8 -*-
# Part of BAHEY WADEA 2024. See LICENSE file for full copyright and licensing details.

import logging
from odoo import http, _
from odoo.http import request

_logger = logging.getLogger(__name__)


#This Controller Class to render and handle complaint form

class WebsitePropertyComplaint(http.Controller):
    """ This function render specific form of complaint
    and passing the complaint types to this form to help user to choose specific complaint type
        """
    @http.route('/property/complaint/', type='http', auth="public", website=True, sitemap=True)
    def complaint_apply(self, **kwargs):
        complaint_type_ids = request.env['complaint.type'].sudo().search([])
        if not complaint_type_ids:
            return request.render('http_routing.http_error', {
                'status_code': _('Oops'),
                'status_message': _("""The requested page is invalid, or doesn't exist anymore.""")})
        values = {
            'complaint_type_ids': complaint_type_ids,
        }
        return request.render("bloopark_realestate.apply_complaint",values)

    """ This function submit customer complaint data to create 
        partner record with customer data like (name,street , street2, city)
       
            """
    @http.route('/property/complaint/submit', type='http', auth="public", website=True, methods=["POST"])
    def complaint_apply_record(self, **kwargs):
        _logger.warning("/property/complaint/submit"+str(kwargs))
        """ Here is the customer data to create 
                partner record with customer data like (name,street , street2, city) and passing value tenant true
                    """
        partner_vals = {'name':kwargs.get('partner_name'),
                        'email': kwargs.get('email_from'),
                        'street': kwargs.get('customer_street'),
                        'street2': kwargs.get('customer_street2'),
                        'city': kwargs.get('customer_city'),
                        'tenant':True,
                        }

        partner_id = request.env['res.partner'].sudo().create(partner_vals)
        """ Here to get complaint type id"""
        complaint_type = request.env['complaint.type'].sudo().search([('name','=',kwargs.get('type'))])

        """ Here to get employee and auto assigned to complaint"""
        employee = request.env['hr.employee'].sudo().search([])[0]

        """ Here to get complaint values like created partner id and house no , flat no and customer description
            and the select type of complaint to customer
        """
        complaint_vals = {'partner_id':partner_id.id,
                          'customer_house_no': kwargs.get('customer_house_no'),
                          'customer_Flat_no': kwargs.get('customer_Flat_no'),
                          'customer_description': kwargs.get('description'),
                          'type':complaint_type[0].id,
                          'assign_to':employee.id,
                          }
        complaint_id = request.env['property.complaint'].sudo().create(complaint_vals)
        """ Here send email to customer email with complaint no created and recorded data
                """
        complaint_id._send_order_confirmation_mail()

        """Last Step redirect to Thank you page"""
        return request.redirect("/complaint-thank-you?id="+str(complaint_id.id))
