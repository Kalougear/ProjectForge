import os
import re
import shutil
from typing import Set, Tuple, List
from ..cli.colors import Colors

class SnippetHandler:
    """Handler for organizing code snippets"""
    
    def __init__(self, config):
        self.config = config
        self.base_path = config.get('base_path', '')
        self.code_extensions = ['.cpp', '.ino', '.py', '.js', '.html', '.css']  # Common code file extensions

    def organize_snippets(self, source_path: str):
        """Organize code snippets into Code_Archives with folders"""
        target_path = os.path.join(self.base_path, "Code_Archives")
        os.makedirs(target_path, exist_ok=True)
        
        organized_files = set()  # Use set to avoid duplicates
        skipped_files = []
        
        try:
            # First handle standalone files in the source directory
            for item in os.listdir(source_path):
                item_path = os.path.join(source_path, item)
                
                # Process standalone code files
                if os.path.isfile(item_path):
                    ext = os.path.splitext(item)[1].lower()
                    if ext in self.code_extensions:
                        # Create folder and copy file
                        base_name = self._clean_name(os.path.splitext(item)[0])
                        snippet_dir = self._ensure_unique_path(os.path.join(target_path, base_name))
                        os.makedirs(snippet_dir)
                        
                        new_file_name = f"{base_name}{ext}"
                        target_file = os.path.join(snippet_dir, new_file_name)
                        
                        try:
                            shutil.copy2(item_path, target_file)
                            organized_files.add((item_path, target_file))
                            print(Colors.success(f"Created {base_name}/{new_file_name} (standalone file)"))
                        except Exception as e:
                            print(Colors.error(f"Error copying {item}: {e}"))
                            skipped_files.append(item_path)

            # Then handle directories
            for item in os.listdir(source_path):
                item_path = os.path.join(source_path, item)
                
                if os.path.isdir(item_path):
                    folder_name = self._clean_name(item)
                    has_code_files = False
                    code_files = []
                    
                    # First check if directory has any valid code files
                    for root, _, files in os.walk(item_path):
                        for file in files:
                            ext = os.path.splitext(file)[1].lower()
                            if ext in self.code_extensions:
                                has_code_files = True
                                source_file = os.path.join(root, file)
                                code_files.append((source_file, ext))
                    
                    if has_code_files:
                        # Create snippet folder
                        snippet_dir = self._ensure_unique_path(os.path.join(target_path, folder_name))
                        os.makedirs(snippet_dir)
                        
                        # Copy unique code files
                        for source_file, ext in code_files:
                            if os.path.getsize(source_file) > 0:  # Skip empty files
                                new_file_name = f"{folder_name}{ext}"
                                target_file = os.path.join(snippet_dir, new_file_name)
                                
                                # For .ini files, only copy if we don't have one yet
                                if ext == '.ini' and any(f[1].endswith('.ini') for f in organized_files if f[1].startswith(snippet_dir)):
                                    continue
                                
                                try:
                                    shutil.copy2(source_file, target_file)
                                    organized_files.add((source_file, target_file))
                                    print(Colors.success(f"Created {folder_name}/{new_file_name}"))
                                except Exception as e:
                                    print(Colors.error(f"Error copying {os.path.basename(source_file)}: {e}"))
                                    skipped_files.append(source_file)
        
        except Exception as e:
            print(Colors.error(f"Error accessing directory: {e}"))
            return
        
        # Print summary
        print(Colors.header("\nCode Snippets Organization Summary:"))
        if organized_files:
            for folder in sorted(os.listdir(target_path)):
                folder_path = os.path.join(target_path, folder)
                if os.path.isdir(folder_path):
                    files = os.listdir(folder_path)
                    print(Colors.info(f"\n{folder}:"))
                    for file in sorted(files):
                        print(f"  - {file}")
        
        print(Colors.success(f"\nTotal folders created: {len(os.listdir(target_path))}"))
        print(Colors.success(f"Total files organized: {len(organized_files)}"))
        print(Colors.warning(f"Files skipped: {len(skipped_files)}"))

    def _clean_name(self, name: str) -> str:
        """Clean name for folder/file use"""
        clean = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        clean = re.sub(r'_+', '_', clean)
        return clean.strip('_')

    def _ensure_unique_path(self, path: str) -> str:
        """Ensure path is unique by adding counter if needed"""
        counter = 1
        original = path
        while os.path.exists(path):
            path = f"{original}_{counter}"
            counter += 1
        return path
