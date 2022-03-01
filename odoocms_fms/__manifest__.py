# -*- coding: utf-8 -*-

{
    'name': "Faculty Management",
    'sequence': 5,
    'summary': """
        Faculty Management System""",
    'description':"""
            Module Containing Faculty Management System Features.\n
            Version Log:\n
                13.0.0.4: Field Label Updates to Remove Conflicts in Labels.\n
                13.0.0.5: Applied controls for record creations (master record, contract renew,and Additional Duty tabs), for every new record the previous records will be archived.\n
                    \t Also added legacy codes fields on setup tables of FMS.\n
                13.0.0.6: Security Rights and Groups for FMS.\n
                13.0.0.7: Add Extra values to selection column of Faculty Table.\n
                13.0.0.8: Added Fields Missing on faculty staff.\n
                13.0.0.9: Removed Required Flag from master record to cater data import .\n
                """,
    'author': "GlobalXS",
    'company': "GlobalXS Technology Solutions",
    'website': "https://www.globalxs.co",
    'category': 'OdooCMS',
    'version': '0.9',
    'depends': ['odoocms','mail'],
# odoocms_faculty_portal
# odoocms_faculty_portal
# '
    'data': [
        # 'security/fms_groups.xml',
        'security/ir.model.access.csv',
        # 'data/data.xml',
        'views/faculty_staff_view.xml',
        'views/fms_menu.xml',
        # 'views/fms_view.xml',
        # 'views/staff_view.xml',
        'views/odoocms_faculty_menu.xml',

        # 'views/profile/user_profile_head.xml',
        # 'views/profile/user_profile.xml',
        # #'reports/faculty_one_pager.xml',
        # 'reports/ss_one_pager_m.xml',
        # 'reports/faculty_one_pager.xml',
        # 'reports/report.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
