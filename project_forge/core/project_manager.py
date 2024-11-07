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

        if 'base_path' not in self.config:
            print(Colors.header("\n=== Project Base Configuration ==="))
            base_path = input(Colors.info("Enter the base path for all projects: "))
        else:
            base_path = self.config['base_path']
            change = input(Colors.info(f"The current base path serves as the master folder, designated for all projects: {base_path}. Would you like to change it? (y/n): "))
            if change.lower() == 'y':
                base_path = input(Colors.info("Please enter the new path for the master folder: "))

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

        print(Colors.header("\n=== Master Folders Configuration ==="))
        
        if 'master_folders' in self.config:
            print(Colors.info("Current default master folders:"))
            for folder in self.config['master_folders']:
                print(f"  - {folder['name']}: {folder['desc']}")
            
            change = input(Colors.info("\nWould you like to modify the master folders? (y/n): initialize the Default or modify is 'y', to bypass press 'n': "))
            if change.lower() != 'y':
                return self.config['master_folders']

        master_folders = []
        print(Colors.info("\nEnter master folder names and descriptions (empty name to initialize default):"))
        
        while True:
            name = input(Colors.info("\nFolder name (or press Enter to finish): ")).strip().upper()
            if not name:
                break
            desc = input(Colors.info(f"Description for {name}: ")).strip()
            master_folders.append({'name': name, 'desc': desc})

        if not master_folders:
            # Provide default folders if none specified
            master_folders = [
                {'name': 'ONGOING', 'desc': 'Active projects in development'},
                {'name': 'IDEAS', 'desc': 'Project concepts and future plans'},
                {'name': 'HOLD', 'desc': 'Temporarily paused projects'},
                {'name': 'DONE', 'desc': 'Completed projects'},
                {'name': 'Test_And_Experiments', 'desc': 'Code snippet experiments and test projects'},
                {'name': 'Code_Archives', 'desc': 'Code snippets, libraries, ready to go'}
            ]
            print(Colors.warning("\nUsing default folder structure:"))
            for folder in master_folders:
                print(f"  - {folder['name']}: {folder['desc']}")

        # Create the folders
        for folder in master_folders:
            folder_path = os.path.join(self.base_path, folder['name'])
            os.makedirs(folder_path, exist_ok=True)
            print(Colors.success(f"Ensured {folder['name']} exists"))

        # Update config
        self.config['master_folders'] = master_folders
        self.config_manager.save_config()
        return master_folders

    def create_project(self, project_name: str, status: str = None) -> str:
        """Create new project with basic structure"""
        status = status or self.defaults['status']
        project_path = os.path.join(self.base_path, status, project_name)
        
        os.makedirs(project_path, exist_ok=True)
        self._create_project_yaml(project_path, project_name, status)
        
        if self.defaults.get('create_readme', True):
            self._create_readme(project_path, project_name, status)
            
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
