
{
    'name': 'OdooCMS Core',
    'version': '13.0.1.0.1',
    'summary': """Core Module for UMS""",
    'description': 'Core Module of Educational Institutes (University Level)',
    'category': 'OdooCMS',
    'sequence': 1,
    'author': 'AARSOL & NUST Team',
    'company': 'AARSOL & NUST (Joint Venture)',
    'website': "https://www.aarsol.com/",
    'depends': ['base', 'mail','hr','website'],
    'data': [
        'security/ir.model.access.csv',
        'security/odoocms_security.xml',
        
        'data/pre_data.xml',
        'data/odoocms.campus.csv',
        'data/odoocms.institute.csv',
        'data/odoocms.program.csv',
        'data/data.xml',
        
        
        # 'views/res_config_setting_view.xml',
        'views/odoocms_menu.xml',
        # # 'views/assets.xml',
        
        'views/base_view.xml',
        
        
        
        'views/campus_view.xml',
        'views/institute_view.xml',
        'views/department_view.xml', # discipline views in department file
        'views/career_view.xml',

        'views/program_view.xml', # Specialization views in Program file
        'views/term_view.xml', # Session views in Term File
        
        'views/course_view.xml',
        'views/study_scheme_view.xml',

        'views/student_view.xml',
        # 'views/transcript_history_view.xml',

        # 'wizard/change_student_state_view.xml',
        # 'wizard/student_comments_view.xml',
        # 'wizard/create_user.xml',
        # 'wizard/change_reg_to_reg.xml',
        # 'views/sequence.xml',


    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}