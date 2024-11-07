# project_forge/cli/colors.py
class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    INFO = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def header(cls, text: str) -> str:
        return f"{cls.HEADER}{text}{cls.END}"

    @classmethod
    def info(cls, text: str) -> str:
        return f"{cls.INFO}{text}{cls.END}"

    @classmethod
    def success(cls, text: str) -> str:
        return f"{cls.SUCCESS}{text}{cls.END}"

    @classmethod
    def warning(cls, text: str) -> str:
        return f"{cls.WARNING}{text}{cls.END}"

    @classmethod
    def error(cls, text: str) -> str:
        return f"{cls.ERROR}{text}{cls.END}"

    @classmethod
    def bold(cls, text: str) -> str:
        return f"{cls.BOLD}{text}{cls.END}"

    @classmethod
    def underline(cls, text: str) -> str:
        return f"{cls.UNDERLINE}{text}{cls.END}"
