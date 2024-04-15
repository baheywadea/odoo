# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import warnings
from datetime import datetime, timedelta

from odoo import http, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.osv.expression import AND
from odoo.http import request
from odoo.tools.misc import groupby


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
