# project_forge/cli/menu.py
import argparse
import yaml
import sys
import os
import shutil
from typing import Optional, List
from ..cli.colors import Colors

def print_menu(title: str, options: List[str], width: int = 50) -> None:
    """Print a styled menu"""
    print(f"\n{Colors.header('='*width)}")
    print(f"{Colors.header(title.center(width))}")
    print(f"{Colors.header('='*width)}")
    for idx, option in enumerate(options, 1):
        print(Colors.info(f"{idx}. {option}"))

class CLI:
    def __init__(self, config_path: str = 'project_config.yaml'):
        self.config_path = config_path
        self.manager = None  # Initialize manager as None

    def create_manager(self):
        from ..core.project_manager import ProjectManager
        if self.manager is None:
            self.manager = ProjectManager(self.config_path)
        return self.manager

    def parse_args(self) -> Optional[argparse.Namespace]:
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(description='Project Forge Tool')
        parser.add_argument('--config', default='project_config.yaml',
                            help='Path to configuration file')
        parser.add_argument('--reconfigure', action='store_true',
                            help='Reconfigure master folders and base path')
        
        subparsers = parser.add_subparsers(dest='command', help='Commands')

        # Create project command
        create_parser = subparsers.add_parser('create', help='Create new project')
        create_parser.add_argument('name', help='Project name')
        create_parser.add_argument('--status', 
                                   choices=[f['name'] for f in self.create_manager().master_folders],
                                   default=self.create_manager().defaults['status'],
                                   help='Project status')

        # Organize project command
        organize_parser = subparsers.add_parser('organize', help='Organize existing project')
        organize_parser.add_argument('source', help='Source directory')
        organize_parser.add_argument('name', help='Project name')
        organize_parser.add_argument('--status',
                                     choices=[f['name'] for f in self.create_manager().master_folders],
                                     default=self.create_manager().defaults['status'],
                                     help='Project status')
        organize_parser.add_argument('--pattern',
                                     choices=list(self.create_manager().naming_patterns.keys()),
                                     help='Naming pattern')

        return parser.parse_args()

    def interactive_mode(self) -> None:
        """Run interactive CLI menu"""
        # Show master folders check message
        if self.create_manager().check_master_folders_exist():
            print(Colors.success("\n✓ Master folders structure exists"))
        else:
            print(Colors.error("\n✗ Master folders structure is incomplete"))

        while True:
            print_menu("Project Forge", [
                "Create new project",
                "Organize existing project",
                "Move project between statuses",
                "List all projects",
                "Manage folder structure",
                "Exit"
            ])

            choice = input(Colors.info("\nSelect an option (1-6): "))

            if choice == '1':
                self._create_project_interactive()
            elif choice == '2':
                self._organize_project_interactive()
            elif choice == '3':
                self._move_project_interactive()
            elif choice == '4':
                self._list_projects()
            elif choice == '5':
                self._manage_folder_structure()
            elif choice == '6':
                print(Colors.success("\nGoodbye!"))
                break
            else:
                print(Colors.error("Invalid choice!"))

    def _manage_folder_structure(self):
        """Manage folder structure"""
        while True:
            print(Colors.header("\n=== Project Forge - Manage Folder Structure ==="))
            
            print_menu("Select Action", [
                "Add custom folders to existing structure",
                "Reinitialize folder structure (with backup)",
                "Return to main menu"
            ])
            
            choice = input(Colors.info("\nSelect option (1-3): "))
            
            if choice == '1':
                self.create_manager().add_custom_folders()
            elif choice == '2':
                confirm = input(Colors.warning("\nThis will create a backup of your current structure and reinitialize it. Continue? (y/n): "))
                if confirm.lower() == 'y':
                    self.create_manager().reinitialize_folder_structure()
            elif choice == '3':
                return
            else:
                print(Colors.error("Invalid choice!"))

    def _create_project_interactive(self):
        """Interactive project creation"""
        while True:
            print(Colors.header("\n=== Project Forge - Create New Project ==="))
            print_menu("Select Action", [
                "Create a new project",
                "Return to main menu"
            ])
            
            choice = input(Colors.info("\nSelect option (1-2): "))
            
            if choice == '2':
                return
            elif choice != '1':
                print(Colors.error("Invalid choice!"))
                continue
            
            # Get project name
            project_name = input(Colors.info("\nPlease specify the new name for the project: "))
            
            # Select status
            print_menu("Select Project Status", 
                    [f"{f['name']}: {f['desc']}" for f in self.create_manager().master_folders])
            
            while True:
                try:
                    status_idx = int(input(Colors.info("\nSelect status (number): "))) - 1
                    if 0 <= status_idx < len(self.create_manager().master_folders):
                        status = self.create_manager().master_folders[status_idx]['name']
                        break
                    print(Colors.error("Invalid selection"))
                except ValueError:
                    print(Colors.error("Please enter a number"))

            try:
                self.create_manager().create_project(project_name, status)
                print(Colors.success(f"\nProject '{project_name}' created successfully!"))
                input(Colors.info("\nPress Enter to continue..."))
            except Exception as e:
                print(Colors.error(f"Error creating project: {e}"))
                input(Colors.info("\nPress Enter to continue..."))

    def _organize_project_interactive(self):
        """Interactive project organization"""
        while True:
            print(Colors.header("\n=== Project Forge - Organize Project ==="))
            
            # First ask if these are code snippets
            print_menu("Select Organization Type", [
                "Full Project - Copy and organize to new location",
                "Code Snippets",
                "Return to main menu"
            ])
            
            try:
                choice = int(input(Colors.info("\nSelect type (1-3): ")))
                if choice == 3:  # Return to main menu
                    return
                    
                if choice not in [1, 2]:
                    print(Colors.error("Invalid choice!"))
                    continue
                    
                # Get source directory
                source = input(Colors.info("\nPlease enter the path of the directory you wish to organize: "))
                if not os.path.exists(source):
                    print(Colors.error("Source directory does not exist!"))
                    input(Colors.info("\nPress Enter to continue..."))
                    continue

                if choice == 2:  # Code Snippets
                    self._organize_snippets(source)
                else:  # Full Project
                    print(Colors.info("""
=== Copy and Organize to New Location ===
This will:
 - Create a new project in your project workspace
 - Copy all files from the source directory
 - Organize them according to Project Forge structure
 - The original files will remain unchanged.
"""))

                    # Get project details
                    project_name = input(Colors.info("Enter project name: "))
                    
                    # Select status
                    print_menu("Select Project Status", 
                            [f"{f['name']}: {f['desc']}" for f in self.create_manager().master_folders])
                    
                    while True:
                        try:
                            status_idx = int(input(Colors.info("\nSelect status (number): "))) - 1
                            if 0 <= status_idx < len(self.create_manager().master_folders):
                                status = self.create_manager().master_folders[status_idx]['name']
                                break
                            print(Colors.error("Invalid selection"))
                        except ValueError:
                            print(Colors.error("Please enter a number"))

                    # Select naming pattern
                    print_menu("Select Naming Pattern", 
                            [f"{name}: {info['description']}" 
                            for name, info in self.create_manager().naming_patterns.items()])
                    
                    while True:
                        try:
                            pattern_idx = int(input(Colors.info("\nSelect pattern (number): "))) - 1
                            if 0 <= pattern_idx < len(self.create_manager().naming_patterns):
                                pattern = list(self.create_manager().naming_patterns.keys())[pattern_idx]
                                break
                            print(Colors.error("Invalid selection"))
                        except ValueError:
                            print(Colors.error("Please enter a number"))

                    # Final confirmation
                    confirm = input(Colors.warning(f"\nThis will copy and organize files from '{source}' to a new project. Continue? (y/n): "))
                    
                    if confirm.lower() != 'y':
                        print(Colors.warning("Operation cancelled."))
                        input(Colors.info("\nPress Enter to continue..."))
                        continue

                    try:
                        self.create_manager().organize_existing_project(source, project_name, status, pattern)
                        print(Colors.success(f"\nProject '{project_name}' organized successfully in new location!"))
                        input(Colors.info("\nPress Enter to continue..."))
                    except Exception as e:
                        print(Colors.error(f"Error organizing project: {e}"))
                        input(Colors.info("\nPress Enter to continue..."))

            except ValueError:
                print(Colors.error("Invalid input!"))
                input(Colors.info("\nPress Enter to continue..."))

    def _organize_snippets(self, source_path: str):
        """Organize code snippets into Code_Archives with folders"""
        print(Colors.header("\n=== Project Forge - Organizing Code Snippets ==="))
        
        try:
            self.create_manager().snippet_handler.organize_snippets(source_path)
            input(Colors.info("\nPress Enter to continue..."))
        except Exception as e:
            print(Colors.error(f"Error organizing snippets: {e}"))
            input(Colors.info("\nPress Enter to continue..."))

    def _move_project_interactive(self):
        """Interactive project movement between statuses"""
        while True:
            print(Colors.header("\n=== Project Forge - Move Project ==="))
            
            print_menu("Select Action", [
                "Move a project",
                "Return to main menu"
            ])
            
            choice = input(Colors.info("\nSelect option (1-2): "))
            
            if choice == '2':
                return
            elif choice != '1':
                print(Colors.error("Invalid choice!"))
                continue
            
            # Get all projects
            projects = self.create_manager()._get_all_projects()
            if not projects:
                print(Colors.warning("No projects found!"))
                input(Colors.info("\nPress Enter to continue..."))
                continue

            # Show all projects with numbers
            all_projects = []  # List to store (status, project) tuples
            for status, project_list in projects.items():
                if project_list:  # Only show status if it has projects
                    print(f"\n{Colors.header(status)}:")
                    for project in project_list:
                        idx = len(all_projects) + 1
                        all_projects.append((status, project))
                        print(Colors.info(f"{idx}. {project}"))

            if not all_projects:
                print(Colors.warning("No projects found in any status!"))
                input(Colors.info("\nPress Enter to continue..."))
                continue

            # Select project by number
            while True:
                try:
                    project_idx = input(Colors.info("\nSelect project number (or 'q' to quit): "))
                    if project_idx.lower() == 'q':
                        break
                        
                    project_idx = int(project_idx) - 1
                    if 0 <= project_idx < len(all_projects):
                        current_status, project_name = all_projects[project_idx]
                        break
                    else:
                        print(Colors.error(f"Please enter a number between 1 and {len(all_projects)}"))
                except ValueError:
                    print(Colors.error("Please enter a valid number or 'q' to quit"))

            if project_idx.lower() == 'q':
                continue

            # Show available status options
            print("\n" + Colors.header("Available Statuses:"))
            status_list = [folder['name'] for folder in self.create_manager().master_folders]
            for idx, status in enumerate(status_list, 1):
                print(Colors.info(f"{idx}. {status}"))

            # Select new status
            while True:
                try:
                    status_idx = input(Colors.info("\nSelect new status number (or 'q' to quit): "))
                    if status_idx.lower() == 'q':
                        break
                        
                    status_idx = int(status_idx) - 1
                    if 0 <= status_idx < len(status_list):
                        new_status = status_list[status_idx]
                        if new_status == current_status:
                            print(Colors.warning("Project is already in this status!"))
                            continue
                        break
                    else:
                        print(Colors.error(f"Please enter a number between 1 and {len(status_list)}"))
                except ValueError:
                    print(Colors.error("Please enter a valid number or 'q' to quit"))

            if status_idx.lower() == 'q':
                continue

            # Confirm move
            confirm = input(Colors.warning(
                f"\nMove '{project_name}' from {current_status} to {new_status}? (y/n): "))
            if confirm.lower() != 'y':
                print(Colors.warning("Operation cancelled."))
                input(Colors.info("\nPress Enter to continue..."))
                continue

            # Move project
            try:
                old_path = os.path.join(self.create_manager().base_path, current_status, project_name)
                new_path = os.path.join(self.create_manager().base_path, new_status, project_name)
                
                if os.path.exists(new_path):
                    print(Colors.error(f"A project named '{project_name}' already exists in {new_status}!"))
                    input(Colors.info("\nPress Enter to continue..."))
                    continue
                    
                shutil.move(old_path, new_path)
                
                # Update project.yaml
                yaml_path = os.path.join(new_path, "project.yaml")
                if os.path.exists(yaml_path):
                    with open(yaml_path, 'r') as f:
                        data = yaml.safe_load(f)
                    data['status'] = new_status
                    with open(yaml_path, 'w') as f:
                        yaml.dump(data, f, default_flow_style=False)
                        
                print(Colors.success(f"\nSuccessfully moved '{project_name}' to {new_status}"))
                input(Colors.info("\nPress Enter to continue..."))
                
            except Exception as e:
                print(Colors.error(f"Error moving project: {e}"))
                input(Colors.info("\nPress Enter to continue..."))

    def _list_projects(self):
        """List all projects"""
        print(Colors.header("\n=== Project Forge - Project List ==="))
        
        projects = self.create_manager()._get_all_projects()
        if not projects:
            print(Colors.warning("No projects found!"))
            input(Colors.info("\nPress Enter to return to main menu..."))
            return

        for status in self.create_manager().master_folders:
            if status['name'] in projects:
                print(f"\n{Colors.header(status['name'])}:")
                for project in projects[status['name']]:
                    print(Colors.info(f"- {project}"))

        input(Colors.info("\nPress Enter to return to main menu..."))

def main():
    """Main entry point for the CLI"""
    try:
        cli = CLI()
        args = cli.parse_args()
        
        if args.reconfigure:
            manager = cli.create_manager()
            manager.configure_base_path()
            manager.get_or_configure_master_folders()
            print(Colors.success("Configuration updated successfully!"))
            return

        if not args.command:
            cli.interactive_mode()
        else:
            manager = cli.create_manager()
            if args.command == 'create':
                manager.create_project(args.name, args.status)
            elif args.command == 'organize':
                manager.organize_existing_project(args.source, args.name, 
                                                  args.status, args.pattern)

    except KeyboardInterrupt:
        print(Colors.warning("\nOperation cancelled by user"))
        sys.exit(0)
    except Exception as e:
        print(Colors.error(f"Fatal error: {e}"))
        sys.exit(1)

if __name__ == "__main__":
    main()
