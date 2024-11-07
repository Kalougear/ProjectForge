import pytest
from project_forge.handlers.file_handler import FileHandler
from project_forge.constants.defaults import (
    DEFAULT_FILE_CATEGORIES,
    DEFAULT_IGNORE_PATTERNS,
    DEFAULT_NAMING_PATTERNS
)

class TestFileHandler:
    @pytest.fixture
    def handler(self):
        """Create a FileHandler instance with test config"""
        test_config = {
            'file_categories': DEFAULT_FILE_CATEGORIES,
            'ignore_patterns': DEFAULT_IGNORE_PATTERNS,
            'naming_patterns': DEFAULT_NAMING_PATTERNS
        }
        return FileHandler(test_config)

    def test_should_ignore(self, handler):
        """Test file ignore patterns"""
        assert handler._should_ignore(".gitignore") == True
        assert handler._should_ignore("test.txt") == False
        assert handler._should_ignore("file~") == True

    def test_get_file_category(self, handler):
        """Test file categorization"""
        assert handler._get_file_category("test.txt") == "docs/text"
        assert handler._get_file_category("test.py") == "software/src"
        assert handler._get_file_category("test.unknown") is None