import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Set
from ..cli.colors import Colors

class FileHandler:
    """Handler for file organization and management"""
    
    def __init__(self, config):
        self.config = config
        self.file_categories = config.get('file_categories', {})
        self.naming_patterns = config.get('naming_patterns', {})
        self.ignore_patterns = config.get('ignore_patterns', [])

    def organize_files(self, source_path: str, target_path: str, naming_pattern: str = None) -> Tuple[List[Tuple[str, str]], List[str]]:
        """Organize files from source to target"""
        organized_files = []
        skipped_files = []
        
        try:
            for root, _, files in os.walk(source_path):
                for file in files:
                    if self._should_ignore(file):
                        continue
                        
                    source_file = os.path.join(root, file)
                    relative_path = os.path.relpath(source_file, source_path)
                    
                    # Skip files that are part of the software structure
                    if any(part in self.config.get('preserved_software_structure', []) 
                          for part in Path(relative_path).parts):
                        continue
                    
                    ext = os.path.splitext(file)[1].lower()
                    category = self._get_file_category(file)
                    
                    if category:
                        target_dir = os.path.join(target_path, category)
                        os.makedirs(target_dir, exist_ok=True)
                        
                        # Generate new filename if pattern specified
                        if naming_pattern:
                            base_name = os.path.splitext(file)[0]
                            new_name = self._generate_new_filename(base_name, naming_pattern) + ext
                        else:
                            new_name = file
                            
                        target_file = os.path.join(target_dir, new_name)
                        
                        # Handle duplicates
                        counter = 1
                        while os.path.exists(target_file):
                            base, ext = os.path.splitext(new_name)
                            target_file = os.path.join(target_dir, f"{base}_{counter}{ext}")
                            counter += 1
                        
                        try:
                            shutil.copy2(source_file, target_file)
                            organized_files.append((source_file, target_file))
                            print(Colors.success(f"Organized: {relative_path}"))
                        except Exception as e:
                            print(Colors.error(f"Error copying {relative_path}: {e}"))
                            skipped_files.append(source_file)
                    else:
                        skipped_files.append(source_file)
        
        except Exception as e:
            print(Colors.error(f"Error in organization: {e}"))
            return [], []

        # Print summary
        print(Colors.header("\nOrganization Summary:"))
        print(Colors.success(f"Files organized: {len(organized_files)}"))
        print(Colors.warning(f"Files skipped: {len(skipped_files)}"))

        return organized_files, skipped_files

    def _should_ignore(self, filename: str) -> bool:
        """Check if file should be ignored"""
        return any(re.match(pattern, filename) for pattern in self.ignore_patterns)

    def _get_file_category(self, filename: str) -> str:
        """Determine file category based on extension"""
        ext = os.path.splitext(filename)[1].lower()
        
        # Traverse nested file categories
        for category, content in self.file_categories.items():
            # Handle nested categories
            if isinstance(content, dict):
                for subcategory, extensions in content.items():
                    if isinstance(extensions, list) and ext in extensions:
                        # Map categories to project structure
                        if category == 'code':
                            if subcategory == 'programming':
                                return 'software/src'
                        elif category == 'documents':
                            if subcategory == 'notes':
                                return '_docs/notes'
                            elif subcategory == 'office_docs':
                                return '_docs/references'
                            elif subcategory == 'technical':
                                return '_docs/datasheets'
                        elif category == 'images':
                            return '_docs/images'
                        elif category == 'data':
                            if subcategory == 'structured':
                                return '_docs/data'
                            elif subcategory == 'tabular':
                                return '_docs/data'
                            elif subcategory == 'database':
                                return 'software/db'
                        elif category == 'media':
                            return '_docs/media'
                        elif category == 'design':
                            if subcategory == 'cad':
                                return 'cad/models'
                            elif subcategory == 'design_tools':
                                return '_docs/design'
            # Handle flat categories
            elif isinstance(content, list) and ext in content:
                if category == 'archives':
                    return 'builds'
                elif category == 'config':
                    return 'software/config'
        
        return None

    def _generate_new_filename(self, filename: str, pattern: str) -> str:
        """Generate new filename based on pattern"""
        name, ext = os.path.splitext(filename)
        pattern_config = self.naming_patterns[pattern]
        formatter = lambda s: s  # Default formatter
        
        if pattern == 'snake_case':
            formatter = lambda s: '_'.join(word.lower() for word in re.split('[-_ ]', s))
        elif pattern == 'PascalCase':
            formatter = lambda s: ''.join(word.capitalize() for word in re.split('[-_ ]', s))
            
        new_name = formatter(name)
        return new_name
