# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import warnings
from datetime import datetime, timedelta
import logging
from odoo import http, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.osv.expression import AND
from odoo.http import request
from odoo.tools.misc import groupby

_logger = logging.getLogger(__name__)


class WebsitePropertyComplaint(http.Controller):

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

    @http.route('/property/complaint/submit', type='http', auth="public", website=True, methods=["POST"])
    def complaint_apply_record(self, **kwargs):
        _logger.warning("/property/complaint/submit"+str(kwargs))
        partner_vals = {'name':kwargs.get('partner_name'),
                        'email': kwargs.get('email_from'),
                        'street': kwargs.get('customer_street'),
                        'street2': kwargs.get('customer_street2'),
                        'city': kwargs.get('customer_city'),
                        }

        partner_id = request.env['res.partner'].sudo().create(partner_vals)
        complaint_type = request.env['complaint.type'].sudo().search([('name','=',kwargs.get('type'))])
        complaint_vals = {'partner_id':partner_id.id,
                          'customer_house_no': kwargs.get('customer_house_no'),
                          'customer_Flat_no': kwargs.get('customer_Flat_no'),
                          'customer_description': kwargs.get('description'),
                          'type':complaint_type[0].id
                          }
        complaint_id = request.env['property.complaint'].sudo().create(complaint_vals)
        return request.redirect("/complaint-thank-you?id="+str(complaint_id.id))
