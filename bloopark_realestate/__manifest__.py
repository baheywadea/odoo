# -*- coding: utf-8 -*-
# Part of BAHEY WADEA. See LICENSE file for full copyright and licensing details.
{
    'name': 'Real Estate',
    'version': '17.0.0.0',
    'category': 'Accounting',
    'summary': 'Real Estate',
    'description': """
            provide a form on website for
            tenants to submit complaints about their rented flats. These complaints will then be classified
            and dealt with by RealEstateX’s employees.

    """,
    'author': 'Bahey Wadea',
    "price": 120,
    "currency": 'EUR',
    'website': 'https://www.linkedin.com/in/baheywadeahakim/',
    'depends': ['base','hr', 'website','account'],
    'data': [
        # 'report/pos_receipt_card.xml',
        # 'report/pos_receipt_report.xml',
        # 'report/pos_arabic_receipt.xml',
        # 'report/pos_arabic_receipt_report.xml',

        'security/res_groups_data.xml',

        'security/ir.model.access.csv',

        'views/property_views.xml',
        'views/property_data.xml',
        'views/property_menus.xml',
        'views/property_complaint_website_template.xml',
    ],
    'assets': {
        # 'point_of_sale._assets_pos': [
        #     'bi_pos_a4_size_receipt/static/src/app/receiptscreen.js',
        #     'bi_pos_a4_size_receipt/static/src/app/receiptscreen.xml',
        # ],
    },
    'license': 'OPL-1',
    'auto_install': False,
    'installable': True,
    # 'live_test_url':'https://youtu.be/JMFQ7DUNOkg',
    'images':[
        "static/description/icon.png"
    ],
}

