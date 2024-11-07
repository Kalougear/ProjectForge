import yaml
import os
from project_forge.handlers.file_handler import FileHandler
from project_forge.constants.defaults import (
    DEFAULT_FILE_CATEGORIES,
    DEFAULT_IGNORE_PATTERNS,
    DEFAULT_NAMING_PATTERNS
)
from project_forge.core.project_manager import ProjectManager

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    # Set default base path
    default_base_path = os.path.join(os.path.expanduser("~"), "Desktop", "Projects")
    
    # Initialize project manager with test mode to avoid path issues
    project_manager = ProjectManager('project_config.yaml', test_mode=True)
    
    # Example: Create a new project
    project_name = "example_project"
    project_path = project_manager.create_project(project_name)
    print(f"Created project at: {project_path}")

if __name__ == "__main__":
    main()
