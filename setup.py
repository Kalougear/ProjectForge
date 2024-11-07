from setuptools import setup, find_packages

setup(
    name="project-forge",  # Changed from project-management-tool
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'PyYAML>=5.1',
        'pathlib>=1.0',
    ],
    entry_points={
        'console_scripts': [
            'project-forge=project_forge.cli.menu:main',  # Fixed package name
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A project forge tool for organizing files and projects",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Kalougear/ProjectForge",  # Updated repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
