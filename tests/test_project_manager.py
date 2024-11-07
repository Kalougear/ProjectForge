# tests/test_project_manager.py
import pytest
import os
import yaml
from pathlib import Path
from project_forge.core.project_manager import ProjectManager
from project_forge.constants.defaults import (
    DEFAULT_PROJECT_STRUCTURE,
    DEFAULT_FILE_CATEGORIES,
    DEFAULT_NAMING_PATTERNS,
    DEFAULT_IGNORE_PATTERNS
)

class TestProjectManager:
    @pytest.fixture
    def manager(self, tmp_path):
        """Create a ProjectManager instance with temporary config"""
        config_path = tmp_path / "test_config.yaml"
        
        # Create test config
        test_config = {
            'project_structure': DEFAULT_PROJECT_STRUCTURE,
            'file_categories': DEFAULT_FILE_CATEGORIES,
            'naming_patterns': DEFAULT_NAMING_PATTERNS,
            'ignore_patterns': DEFAULT_IGNORE_PATTERNS,
            'defaults': {
                'status': 'ONGOING',
                'create_readme': True,
                'readme_template': "# {project_name}\nCreated: {date}\nStatus: {status}\n"
            }
        }
        
        # Write test config to file
        with open(config_path, 'w') as f:
            yaml.dump(test_config, f)
            
        return ProjectManager(str(config_path), test_mode=True)

    def test_create_project(self, manager):
        """Test basic project creation"""
        project_name = "test_project"
        project_path = manager.create_project(project_name, "ONGOING")
        
        assert os.path.exists(project_path)
        assert os.path.exists(os.path.join(project_path, "project.yaml"))
        assert os.path.exists(os.path.join(project_path, "README.md"))

    def test_organize_project(self, manager, tmp_path):
        """Test project organization"""
        # Create source directory with test files
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "test.txt").write_text("test content")
        
        project_name = "organized_project"
        result_path = manager.organize_existing_project(
            str(source_dir),
            project_name,
            "ONGOING",
            "snake_case"
        )
        
        assert os.path.exists(result_path)
        assert os.path.exists(os.path.join(result_path, "_docs"))