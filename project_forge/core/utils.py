# project_forge/core/utils.py
import os
import re
from pathlib import Path
from typing import List, Tuple

class PathUtils:
    """Utility functions for path handling"""
    
    @staticmethod
    def ensure_unix_path(path: str) -> str:
        """Convert Windows path to Unix/WSL format if needed"""
        if ':' in path:  # Windows path detected
            drive = path[0].lower()
            path_without_drive = path[2:].replace('\\', '/').lstrip('/')
            return f"/mnt/{drive}/{path_without_drive}"
        return path

    @staticmethod
    def clean_name(name: str) -> str:
        """Clean name for folder/file use"""
        clean = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        clean = re.sub(r'_+', '_', clean)
        return clean.strip('_')

    @staticmethod
    def ensure_unique_path(path: str) -> str:
        """Ensure path is unique by adding counter if needed"""
        counter = 1
        original = path
        while os.path.exists(path):
            base, ext = os.path.splitext(original)
            path = f"{base}_{counter}{ext}"
            counter += 1
        return path

    @staticmethod
    def split_path_components(path: str) -> Tuple[str, str, str]:
        """Split path into directory, name, and extension"""
        directory = os.path.dirname(path)
        name = os.path.basename(path)
        base, ext = os.path.splitext(name)
        return directory, base, ext
