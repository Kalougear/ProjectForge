import pytest
from project_forge.handlers.software_handler import SoftwareHandler

class TestSoftwareHandler:
    @pytest.fixture
    def handler(self):
        """Create a SoftwareHandler instance"""
        test_config = {
            'software_project_markers': {
                'files': ['setup.py', 'package.json'],
                'directories': ['src', 'test']
            }
        }
        return SoftwareHandler(test_config)

    def test_detect_project_type(self, handler, tmp_path):
        """Test software project detection"""
        # Create a test project
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        # Test Python project
        (project_dir / "setup.py").write_text("")
        assert handler.detect_project_type(str(project_dir)) == "general"
        
        # Test Arduino project
        (project_dir / "sketch.ino").write_text("")
        assert handler.detect_project_type(str(project_dir)) == "arduino"