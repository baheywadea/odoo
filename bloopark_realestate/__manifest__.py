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
            Tenants should be able to submit complaints using RealEstateX’s website.
                a. In the form, tenants will provide data to identify themselves (name, email) and
                the flat they are renting (address)
                b. The form should also include fields to describe the problem (type, description)
                c. There are many types of complaints (question, electrical issue, heating issue,
                etc)
                d. The form should be available without authentication.
                e. After submission, tenants should see a success page indicating that their
                complaint has been recorded, and they should also receive an email with their
                complaint number
            
            2. Back-office Pipeline: In the backend, RealEstateX’s employees should be able to
            see the complaints submitted by the tenants and take action appropriately.
                a. Complaints should be assigned automatically to a customer service
                representative, who will be responsible to classify the complaint and decide
                and write down (text field) the action plan.
                b. If the complaint is a question, the customer service representative can just
                message the tenant with the answer and close the complaint.
                c. If the complaint is not valid (duplication, wrong information, or other reasons)
                the customer service representative can drop it.
                d. If the action plan requires an intervention from a RealEstateX’s employee, a
                work order needs to be printed by a customer service supervisor.
                e. Once a complaint is closed (solved or dropped) an email must be sent to the
                tenant notifying the outcome of their complaint
                f. The Pipeline have 5 stages
                    i. New: for newly created complaints
                    ii. In Review: for complaints that are being classified by a customer
                    service representative
                    iii. In Progress: for complaints that are being addressed with an action
                    plan
                    iv. Solved: for complaints that have been solved
                    v. Dropped: for complaints that have been dropped

    """,
    'author': 'Bahey Wadea',
    "price": 120,
    "currency": 'EUR',
    'website': 'https://www.linkedin.com/in/baheywadeahakim/',
    'depends': ['base','hr', 'website','account'],
    'data': [
        'report/property_complaint_report.xml',
        'report/property_complaint_report_action.xml',
        'security/res_groups_data.xml',
        'security/ir.model.access.csv',
        'views/property_views.xml',
        'data/property_data.xml',
        'data/mail_template_data.xml',
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
    'application': True,
    # 'live_test_url':'https://youtu.be/JMFQ7DUNOkg',
    'images':[
        "static/description/icon.png"
    ],
}

