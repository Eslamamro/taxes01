# -*- coding: utf-8 -*-
{
    'name': "Tax",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
        Long description of the module's purpose.
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in module listings
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # Any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # Assets for the module
    'assets': {
        'web.assets_backend': [
            'taxes01/static/src/css/views.css',
        ],
    },

    # Always loaded
    'data': [
        'security/security_perms.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/todo_list.xml',
        'views/templates.xml',
    ],

    # Only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}

