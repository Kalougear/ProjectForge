# project_forge/constants/defaults.py

DEFAULT_CONFIG = {
    'project_structure': {
        '_docs': {
            'description': 'Documentation and reference materials',
            'subfolders': ['datasheets', 'images', 'notes', 'references']
        },
        'hardware': {
            'description': 'Hardware-related files',
            'subfolders': {
                'schematics': [],
                'pcb': [],
                'bom': [],
                'production': ['gerber', 'assembly']
            }
        },
        'software': {
            'description': 'Software and firmware',
            'subfolders': []
        },
        'cad': {
            'description': 'CAD files and 3D printing',
            'subfolders': {
                'models': [],
                '3dprint': ['stl', 'gcode'],
                'drawings': []
            }
        },
        'builds': {
            'description': 'Build outputs and releases',
            'subfolders': []
        }
    },
    'file_categories': {
        'code': ['.py', '.js', '.html', '.css', '.cpp', '.h', '.ino'],
        'docs': ['.md', '.txt', '.pdf', '.doc', '.docx'],
        'data': ['.json', '.yaml', '.csv']
    },
    'naming_patterns': {
        'snake_case': {
            'pattern': '{name}_{type}_{counter}',
            'description': 'snake_case: component_name_001',
            'example': 'motor_mount_cad_001'
        },
        'PascalCase': {
            'pattern': '{name}{type}{counter}',
            'description': 'PascalCase: ComponentName001',
            'example': 'MotorMountCad001'
        }
    },
    'defaults': {
        'status': 'ONGOING',
        'create_readme': True,
        'readme_template': """# {project_name}
Created: {date}
Status: {status}

## Description
Add project description here.

## Structure
- src/ - Source code
- docs/ - Documentation
- tests/ - Test files
"""
    },
    'software_project_markers': {
        'files': [
            'platformio.ini',
            'CMakeLists.txt',
            'package.json',
            'requirements.txt',
            'setup.py'
        ],
        'directories': [
            'src',
            'include',
            'lib',
            'test'
        ]
    },
    'preserved_software_structure': [
        'src',
        'include',
        'lib',
        'test',
        '.pio',
        '.vscode',
        'boards',
        'scripts',
        'data'
    ],
    'ignore_patterns': [
        r'^\.',           # Hidden files
        r'^__pycache__$', # Python cache
        r'\.pyc$',        # Python compiled files
        r'\.o$',          # Object files
        r'\.exe$',        # Executables
        r'node_modules',  # Node.js modules
        r'\.git$',        # Git directory
        r'\.svn$',        # SVN directory
        r'\.DS_Store$',   # macOS files
        r'Thumbs\.db$'    # Windows thumbnail cache
    ]
}
