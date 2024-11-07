# project_forge/core/project_manager.py
import os
import yaml
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from pathlib import Path

from .config import ConfigManager
from ..handlers.file_handler import FileHandler
from ..handlers.software_handler import SoftwareHandler
from ..handlers.snippet_handler import SnippetHandler
from ..cli.colors import Colors

class ProjectManager:
    def __init__(self, config_path: str = 'project_config.yaml', test_mode: bool = False):
        self.test_mode = test_mode
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.config

        # Initialize paths and folders
        self.base_path = self.configure_base_path()
        self.master_folders = self.configure_master_folders()
        
        # Get configurations
        self.project_structure = self.config.get('project_structure', {})
        self.file_categories = self.config.get('file_categories', {})
        self.naming_patterns = self.config.get('naming_patterns', {})
        self.defaults = self.config.get('defaults', {
            'status': 'ONGOING',
            'create_readme': True,
            'readme_template': "# {project_name}\nCreated: {date}\nStatus: {status}\n"
        })
        
        # Initialize handlers
        self.file_handler = FileHandler(self.config)
        self.software_handler = SoftwareHandler(self.config)
        self.snippet_handler = SnippetHandler(self.config)

    def configure_base_path(self) -> str:
        """Configure and validate base project path"""
        if self.test_mode:
            base_path = '/tmp/test_projects'
            os.makedirs(base_path, exist_ok=True)
            return base_path

        current_base_path = self.config.get('base_path')
        
        if not current_base_path:
            print(Colors.header("\n====== Welcome to Project Forge! ======"))
            print(Colors.info("""
Initialize your project workspace by setting up a master folder.
This will be the central location where all your projects will be organized.
Common locations include:
- Desktop/Projects
- Documents/Projects
- Home directory/Projects
            """))
            base_path = input(Colors.info("Please enter the path for your master project folder: "))
        else:
            change = input(Colors.info(f"Current master folder path: {current_base_path}\nWould you like to change it? (y/n): "))
            if change.lower() == 'y':
                base_path = input(Colors.info("Please enter the new path for the master folder: "))
            else:
                base_path = current_base_path

        try:
            # Handle Windows paths
            if ':' in base_path:
                drive = base_path[0].lower()
                path_without_drive = base_path[2:].replace('\\', '/').lstrip('/')
                base_path = f"/mnt/{drive}/{path_without_drive}"

            # Create base directory if it doesn't exist
            os.makedirs(base_path, exist_ok=True)
            
            # Update config
            self.config['base_path'] = base_path
            self.config_manager.save_config()
            
            if not current_base_path:
                print(Colors.success("\nMaster folder successfully initialized!"))
                print(Colors.info("Your project workspace is now ready for use."))
                
            return base_path
            
        except Exception as e:
            print(Colors.error(f"Error creating base directory: {e}"))
            raise

    def configure_master_folders(self) -> List[Dict[str, str]]:
        """Configure master folder structure"""
        if self.test_mode:
            test_folders = [
                {'name': 'ONGOING', 'desc': 'Active projects'},
                {'name': 'DONE', 'desc': 'Completed projects'}
            ]
            for folder in test_folders:
                os.makedirs(os.path.join(self.base_path, folder['name']), exist_ok=True)
            return test_folders

        print(Colors.header("\n====== Project Organization Structure ======"))
        
        # Get default folders from config
        default_folders = self.config.get('master_folders', [
            {'name': 'ONGOING', 'desc': 'Active projects in development'},
            {'name': 'IDEAS', 'desc': 'Project concepts and future plans'},
            {'name': 'HOLD', 'desc': 'Temporarily paused projects'},
            {'name': 'DONE', 'desc': 'Completed projects'},
            {'name': 'Test_Lab', 'desc': 'Code snippet experiments and test projects'},
            {'name': 'Code_Vault', 'desc': 'Code snippets, libraries, ready to go'}
        ])

        print(Colors.info("""
Project Forge uses a folder structure to help you keep your work organized.
The default structure is:"""))
        
        for folder in default_folders:
            print(Colors.success(f"\n• {folder['name']}")
                  + Colors.info(f"\n  {folder['desc']}"))
        
        print(Colors.info("""
Choose your folder structure setup:
1. Use default structure only (press '1')
2. Use default structure + custom folders (press '2')
3. Create completely custom structure (press '3')
"""))
        choice = input(Colors.info("Your choice (1/2/3): "))
        
        if choice == '1':
            # Create default folders
            print(Colors.success("\nCreating default folder structure:"))
            for folder in default_folders:
                folder_path = os.path.join(self.base_path, folder['name'])
                os.makedirs(folder_path, exist_ok=True)
                print(Colors.success(f"✓ Created {folder['name']}"))
                
        elif choice == '2':
            # Create default folders first
            print(Colors.success("\nCreating default folder structure:"))
            for folder in default_folders:
                folder_path = os.path.join(self.base_path, folder['name'])
                os.makedirs(folder_path, exist_ok=True)
                print(Colors.success(f"✓ Created {folder['name']}"))

            # Then add custom folders
            print(Colors.info("""
Let's add your custom folders!
Enter folder names and descriptions (press Enter without a name to finish).
These will be created alongside the default folders.
"""))
            
            while True:
                name = input(Colors.info("Custom folder name (or press Enter to finish): ")).strip().upper()
                if not name:
                    break
                desc = input(Colors.info(f"Description for {name}: ")).strip()
                
                # Create the custom folder
                folder_path = os.path.join(self.base_path, name)
                os.makedirs(folder_path, exist_ok=True)
                print(Colors.success(f"✓ Created custom folder {name}"))
                
        else:  # choice == '3'
            print(Colors.info("""
Let's create your custom folder structure!
Enter folder names and descriptions (press Enter without a name to finish).
This will be your project's organization structure.
"""))
            
            custom_folders = []
            while True:
                name = input(Colors.info("Folder name (or press Enter to finish): ")).strip().upper()
                if not name:
                    if not custom_folders:
                        print(Colors.warning("\nAt least one folder is required. Please create a folder:"))
                        continue
                    break
                desc = input(Colors.info(f"Description for {name}: ")).strip()
                custom_folders.append({'name': name, 'desc': desc})
                
                # Create the folder
                folder_path = os.path.join(self.base_path, name)
                os.makedirs(folder_path, exist_ok=True)
                print(Colors.success(f"✓ Created {name}"))

        print(Colors.success("\nFolder structure setup complete!"))
        print(Colors.info("Your project workspace is now organized and ready for use."))

        # Always return the default folders from config
        return default_folders

    def create_project(self, project_name: str, status: str = None) -> str:
        """Create new project with basic structure"""
        status = status or self.defaults['status']
        project_path = os.path.join(self.base_path, status, project_name)
        
        # Create project directory
        os.makedirs(project_path, exist_ok=True)
        
        # Create project structure from config
        print(Colors.header(f"\nCreating project structure for '{project_name}'..."))
        for folder_name, folder_info in self.project_structure.items():
            folder_path = os.path.join(project_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            print(Colors.success(f"✓ Created {folder_name}"))
            
            # Create subfolders if defined
            if 'subfolders' in folder_info:
                if isinstance(folder_info['subfolders'], list):
                    # Simple list of subfolder names
                    for subfolder in folder_info['subfolders']:
                        subfolder_path = os.path.join(folder_path, subfolder)
                        os.makedirs(subfolder_path, exist_ok=True)
                        print(Colors.success(f"  ✓ Created {folder_name}/{subfolder}"))
                else:
                    # Dictionary with nested structure
                    for subfolder, sub_items in folder_info['subfolders'].items():
                        subfolder_path = os.path.join(folder_path, subfolder)
                        os.makedirs(subfolder_path, exist_ok=True)
                        print(Colors.success(f"  ✓ Created {folder_name}/{subfolder}"))
                        
                        # Create any deeper nested folders
                        if isinstance(sub_items, list) and sub_items:
                            for item in sub_items:
                                item_path = os.path.join(subfolder_path, item)
                                os.makedirs(item_path, exist_ok=True)
                                print(Colors.success(f"    ✓ Created {folder_name}/{subfolder}/{item}"))
        
        # Create project metadata
        self._create_project_yaml(project_path, project_name, status)
        print(Colors.success("✓ Created project.yaml"))
        
        # Create README if enabled
        if self.defaults.get('create_readme', True):
            self._create_readme(project_path, project_name, status)
            print(Colors.success("✓ Created README.md"))
        
        print(Colors.success(f"\nProject '{project_name}' created successfully!"))
        return project_path

    def organize_existing_project(self, source_path: str, project_name: str, 
                                status: str, naming_pattern: str = None) -> str:
        """Organize existing project files"""
        # Create new project
        project_path = self.create_project(project_name, status)
        
        # Check if it's a software project
        if self.software_handler.detect_project_type(source_path):
            self.software_handler.copy_project(source_path, project_path)
            
        # Organize other files
        self.file_handler.organize_files(source_path, project_path, naming_pattern)
        
        return project_path

    def _create_project_yaml(self, project_path: str, project_name: str, status: str):
        """Create project metadata YAML file"""
        yaml_content = {
            'name': project_name,
            'status': status,
            'created_date': datetime.now().strftime("%Y-%m-%d"),
            'description': '',
            'version': '0.1.0',
            'metadata': {
                'type': 'project',
                'category': '',
                'tags': []
            }
        }
        
        yaml_path = os.path.join(project_path, "project.yaml")
        with open(yaml_path, 'w') as f:
            yaml.dump(yaml_content, f, default_flow_style=False)

    def _create_readme(self, project_path: str, project_name: str, status: str):
        """Create README.md from template"""
        template = self.defaults.get('readme_template', "# {project_name}\n")
        content = template.format(
            project_name=project_name,
            date=datetime.now().strftime("%Y-%m-%d"),
            status=status
        )
        
        readme_path = os.path.join(project_path, "README.md")
        with open(readme_path, 'w') as f:
            f.write(content)

    def _get_all_projects(self) -> Dict[str, List[str]]:
        """Get all projects organized by status"""
        projects = {}
        
        try:
            # Get all directories that aren't hidden
            status_dirs = [d for d in os.listdir(self.base_path) 
                         if os.path.isdir(os.path.join(self.base_path, d)) 
                         and not d.startswith('.')]
            
            # Get projects for each status directory
            for status in status_dirs:
                status_path = os.path.join(self.base_path, status)
                if os.path.exists(status_path):
                    projects[status] = sorted([
                        d for d in os.listdir(status_path)
                        if os.path.isdir(os.path.join(status_path, d)) 
                        and not d.startswith('.')
                    ])
                    
            return projects
            
        except Exception as e:
            print(Colors.error(f"Error reading projects: {e}"))
            return {}
