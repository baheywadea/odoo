# -*- coding: utf-8 -*-
# Part of BAHEY WADEA. See LICENSE file for full copyright and licensing details.
{
    'name': 'Real Estate',
    'version': '17.0.0.0',
    'category': 'Accounting',
    'summary': 'RealEstateX Tenant Complaint Management System',
    'description': """
            RealEstateX Tenant Complaint Management System
1. Introduction
RealEstateX aims to streamline the process of handling tenant complaints through an efficient online system. This project involves the development of a web-based platform where tenants can submit complaints related to their rented flats, and RealEstateX employees can manage and address these complaints effectively.

2. Project Scope
The scope of this project includes:

Designing and implementing a user-friendly complaint submission form for tenants.
Developing a robust back-end pipeline for RealEstateX employees to handle and classify complaints.
Automating complaint assignment and notification processes.
Implementing a comprehensive system to track complaint status through different stages.
3. Key Features
For Tenants:
Complaint Submission Form:

Allows tenants to provide identification details (name, email) and flat information (address).
Includes fields to describe the complaint type and provide a detailed description.
Accessible without Authentication:

Tenants can submit complaints without the need for user authentication.
Feedback and Confirmation:

Upon submission, tenants receive a success confirmation on the website.
Tenants automatically receive an email with a unique complaint number for reference.
For RealEstateX Employees:
Complaint Management Pipeline:

Automated assignment of complaints to customer service representatives.
Classification of complaints based on type and severity.
Workflow Stages:

New: Newly submitted complaints awaiting classification.
In Review: Complaints being reviewed and categorized.
In Progress: Complaints with action plans being addressed.
Solved: Complaints that have been resolved.
Dropped: Invalid or duplicate complaints that are closed.
Action Plans:

Customer service representatives develop action plans for valid complaints.
Supervisors intervene for escalated complaints requiring further attention.
Communication and Notifications:

Automatic email notifications to tenants for complaint status updates (e.g., resolution, closure).
4. System Architecture
The system architecture consists of:

Front-end:

Developed using HTML/CSS/JavaScript.
User interface for complaint submission and confirmation.
Back-end:

Built with Node.js and Express.js.
MongoDB database for storing complaint data.
RESTful APIs for handling complaint submissions and management.
5. Deployment and Integration
The system will be deployed on a web server environment, ensuring scalability and reliability. Integration with email services (e.g., SMTP) will enable automated email notifications to tenants.

6. Future Enhancements
Potential future enhancements may include:

Integration with a dashboard for real-time monitoring of complaint status.
Machine learning models for automated complaint classification.
Mobile application for on-the-go complaint submissions.

7. Conclusion
The RealEstateX Tenant Complaint Management System aims to enhance tenant satisfaction and streamline internal processes for complaint resolution. By leveraging modern web technologies and automation, this system will ensure efficient handling of tenant complaints and prompt resolution of issues.

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

