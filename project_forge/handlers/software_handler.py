import os
import shutil
import yaml
from pathlib import Path
from typing import Optional
from ..cli.colors import Colors

class SoftwareHandler:
    """Handler for software project detection and organization"""
    
    def __init__(self, config):
        self.config = config
        self.project_type = None
        self.markers = config.get('software_project_markers', {
            'files': [],
            'directories': []
        })
        self.preserved_structure = config.get('preserved_software_structure', [])

    def detect_project_type(self, source_path: str) -> bool:
        """Detect if the source directory is a software project"""
        try:
            # Check for PlatformIO project
            if os.path.exists(os.path.join(source_path, 'platformio.ini')):
                self.project_type = 'platformio'
                return True
                
            # Check for Arduino project
            arduino_markers = ['.ino']
            for marker in arduino_markers:
                if any(Path(source_path).glob(f"**/*{marker}")):
                    self.project_type = 'arduino'
                    return True
                    
            # Check for other software project markers
            for file in self.markers.get('files', []):
                if list(Path(source_path).glob(f"**/*{file}")):
                    self.project_type = 'general'
                    return True
            
            for directory in self.markers.get('directories', []):
                if list(Path(source_path).glob(f"**/{directory}")):
                    self.project_type = 'general'
                    return True
            
            return False
        except Exception as e:
            print(Colors.error(f"Error detecting software project: {e}"))
            return False

    def copy_project(self, source_path: str, target_path: str) -> None:
        """Copy software project preserving its structure"""
        try:
            software_path = os.path.join(target_path, 'software')
            project_type = getattr(self, 'project_type', 'general')
            
            # Create software directory if it doesn't exist
            os.makedirs(software_path, exist_ok=True)

            if project_type == 'platformio':
                special_dirs = [
                    '.pio',          # PlatformIO build and library cache
                    '.vscode',       # VSCode configuration
                    'include',       # Header files
                    'lib',          # Project libraries
                    'src',          # Source code
                    'test',         # Test files
                    'boards',       # Custom board definitions
                    'scripts',      # Build scripts
                    'data'          # Data files
                ]
                special_files = [
                    'platformio.ini',    # PlatformIO configuration
                    '.gitignore',        # Git ignore file
                    'README.md',         # Project documentation
                    'library.json',      # Library manifest
                    'library.properties' # Arduino library properties
                ]
            elif project_type == 'arduino':
                # For Arduino projects, look for the main .ino file directory
                ino_files = list(Path(source_path).glob('**/*.ino'))
                if not ino_files:
                    raise Exception("No .ino file found in Arduino project")
                    
                # Use the directory containing the first .ino file as main sketch directory
                main_sketch_dir = ino_files[0].parent
                sketch_name = main_sketch_dir.name
                
                # Create sketch directory
                sketch_path = os.path.join(software_path, sketch_name)
                os.makedirs(sketch_path, exist_ok=True)
                
                # Copy entire sketch directory
                for item in os.listdir(main_sketch_dir):
                    source_item = os.path.join(main_sketch_dir, item)
                    target_item = os.path.join(sketch_path, item)
                    
                    if os.path.isfile(source_item):
                        shutil.copy2(source_item, target_item)
                        print(Colors.success(f"Copied sketch file: {item}"))
                    elif os.path.isdir(source_item):
                        shutil.copytree(source_item, target_item, dirs_exist_ok=True)
                        print(Colors.success(f"Copied sketch directory: {item}"))
                
                # For Arduino projects, also preserve these directories
                special_dirs = [
                    'libraries',     # Local libraries
                    '.vscode',       # VSCode configuration
                    'build',         # Build output
                    'data'          # Data files
                ]
                special_files = [
                    'arduino.json',      # Arduino VSCode configuration
                    'c_cpp_properties.json', # C/C++ VSCode configuration
                    '.gitignore',        # Git ignore file
                    'README.md'          # Project documentation
                ]
            else:
                # General software project
                special_dirs = [
                    'src',          # Source code
                    'include',      # Headers
                    'lib',          # Libraries
                    'test',         # Tests
                    'docs',         # Documentation
                    'build',        # Build output
                    '.vscode'       # VSCode configuration
                ]
                special_files = [
                    'CMakeLists.txt',   # CMake configuration
                    'Makefile',         # Make configuration
                    'README.md',        # Documentation
                    '.gitignore'        # Git ignore
                ]

            # Copy special directories
            for dir_name in special_dirs:
                source_dir = os.path.join(source_path, dir_name)
                if os.path.exists(source_dir):
                    target_dir = os.path.join(software_path, dir_name)
                    try:
                        if os.path.exists(target_dir):
                            shutil.rmtree(target_dir)
                        shutil.copytree(source_dir, target_dir, symlinks=True)
                        print(Colors.success(f"Copied directory: {dir_name}"))
                    except Exception as e:
                        print(Colors.error(f"Error copying directory {dir_name}: {e}"))

            # Copy special files
            for file_name in special_files:
                source_file = os.path.join(source_path, file_name)
                if os.path.exists(source_file):
                    target_file = os.path.join(software_path, file_name)
                    try:
                        shutil.copy2(source_file, target_file)
                        print(Colors.success(f"Copied file: {file_name}"))
                    except Exception as e:
                        print(Colors.error(f"Error copying file {file_name}: {e}"))

            # For Arduino projects, also look for libraries in parent directories
            if project_type == 'arduino':
                parent_libraries = os.path.join(os.path.dirname(source_path), 'libraries')
                if os.path.exists(parent_libraries):
                    target_libraries = os.path.join(software_path, 'libraries')
                    try:
                        shutil.copytree(parent_libraries, target_libraries, dirs_exist_ok=True)
                        print(Colors.success("Copied parent libraries directory"))
                    except Exception as e:
                        print(Colors.error(f"Error copying parent libraries: {e}"))

            print(Colors.success(f"Preserved {project_type} project structure in {software_path}"))
            
            # Update project.yaml with project type
            yaml_path = os.path.join(target_path, "project.yaml")
            if os.path.exists(yaml_path):
                with open(yaml_path, 'r') as f:
                    data = yaml.safe_load(f)
                data['software_type'] = project_type
                with open(yaml_path, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False)
                
        except Exception as e:
            print(Colors.error(f"Error copying software project: {e}"))
