{
    'name': "Programs",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['mail', 'base'],
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'security/user_rules.xml',
        'views/programme_form.xml',
        'views/hall.xml',
        'data/activity.xml',
        'data/cron.xml',


    ],
    'demo': [],
    'summary': "logic_programs",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': False
}
