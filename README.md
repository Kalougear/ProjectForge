# 🛠️ Project|Forge - Crafting Order from Chaos

Got project files everywhere? Arduino sketches scattered across your PC? Random STL files you can't find? Fear not, fellow maker! This tool will transform your chaotic project folders into a well-organized maker's paradise!

![Thumbs Up Kid](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNWxzNmc2NnIxaXdveW9sMm0zajVzMDgwd2lxZWp0OHNxMnZxbzU0ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XreQmk7ETCak0/giphy.gif)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20WSL-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
## Made with 🛠️ by [SKTech] - For Makers, By Makers!

## Contributors
 - [Lopofsky](https://github.com/Lopofsky)



# 📑 Table of Contents

## Getting Started

- [Overview & Features](#-perfect-for)
- [Quick Start Guide](#-project-forge-setup-guide)
  - [For Beginners](#-wsl-setup-for-beginners-friendly-edition)
  - [For WSL Users](#-for-wsl-users)
  - [For Linux Users](#-for-linux-pros)

## Basic Usage

- [Project Structure](#-project-structure-youll-get)
- [Using The Tool](#-using-the-project-forge)
- [Common Examples](#-real-world-examples)

## Help & Support

- [Path Guide](#️-path-guide-for-everyone)
- [Troubleshooting](#-quick-troubleshooting)
- [Pro Tips](#-pro-tips)

## 🎯 Perfect for:

- 🛠️ Hardware+Software projects
- 🔧 Arduino/PlatformIO development
- 💾 Code snippet management
- 🗂️ Project organization
- 📁 Multi-project workspaces

## 🌟 Key Features

- **Smart Project Detection**: Automatically identifies Arduino, PlatformIO projects
- **Code Snippet Organization**: Keep your valuable code bits organized
- **Project Lifecycle**: Track projects from idea to completion
- **Simple Configuration**: Easy to set up and use
- **Windows Friendly**: Works great with WSL!

# 🚀 Project|Forge Setup Guide

## 🌟 Choose Your Path:

### 🐣 Complete Beginner ("Help! What's Linux?")

### 🔧 WSL User ("I know this stuff!")

### 🐧 Linux Pro ("Just give me the commands!")

---

# 👣 WSL Setup for Beginners (Friendly Edition)

1. **Install WSL on Windows**

   - Press `Windows + X` to open the Power User menu
   - Click on "Windows Powershell (Admin)"
   - Run: `wsl --install`
   - Restart when prompted

2. **Create Your Linux User**

   - After restart, WSL will ask for a username and password
   - Remember these credentials!

3. **Get Project Forge Running**
   - Press `Windows + X` and click "Windows Powershell" (not admin)
   - Copy and paste these commands one by one:

## 1. Install required package (one-time setup)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-yaml git
```
## 2. Clone the repo (one-time setup)
```
git clone https://github.com/Kalougear/ProjectForge.git
cd ProjectForge
```

## 3. Run the script
```
python3 -m project_forge
```

🚀 **Quick Access Tip:** Next time, just open Windows Powershell and run:

```bash
cd ~/ProjectForge
python3 -m project_forge
```

# 🔧 For WSL Users

Quick setup in one go:

```bash
# Complete setup
sudo apt update && sudo apt install python3 python3-pip python3-yaml git
git clone https://github.com/Kalougear/ProjectForge.git
cd ProjectForge
python3 -m project_forge
```

Remember: Use WSL paths! (`/mnt/c/Users/...`)

# 🐧 For Linux Users

One-line setup:

```bash
sudo apt update && sudo apt install python3 python3-pip git && pip3 install PyYAML && git clone https://github.com/Kalougear/ProjectForge.git && cd ProjectForge && python3 -m project_forge
```
# 🍎 For Mac/MacOS Users

### 1. Install Homebrew (if not installed)
```/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"```

### 2. Complete Mac setup in one go:
```brew update && \
brew install python3 git && \
pip3 install PyYAML && \
git clone https://github.com/Kalougear/ProjectForge.git && \
cd ProjectForge && \
python3 -m project_forge
```
---

## 🗺️ Path Guide (For Everyone!)

```bash
Windows Path              →  Linux/WSL Path
----------------            --------------
C:\Users\Name\Projects  →  /mnt/c/Users/Name/Projects
D:\Maker_Projects      →  /mnt/d/Maker_Projects
```

## 🆘 Quick Troubleshooting

### WSL Issues?

```bash
# WSL not installing?
wsl --install --no-distribution
wsl --install -d Ubuntu

# Still problems?
# Windows + X → PowerShell (Admin):
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```

### Python Issues?

```bash
# Python not found?
sudo apt install --reinstall python3

# pip issues?
sudo apt install --reinstall python3-pip
```

### Can't Run Script?

```bash
# Check where you are
pwd

# Check if script is there
ls project_forge.py

# Check Python
python3 --version
```

## 📁 Project Structure You'll Get

```
YourPath/
├── ONGOING/                  # Active projects
├── IDEAS/                    # Future projects
├── HOLD/                    # Paused projects
├── DONE/                    # Completed projects
├── Test_And_Experiments/    # Test code
└── Code_Archives/          # Code snippets
```

Each project gets:

```
Project_Name/
├── software/          # All your code
├── hardware/         # Schematics, PCB files
├── cad/             # 3D models, STLs
├── _docs/           # Documentation
└── builds/          # Build outputs
```

## ❗ Troubleshooting

### Common Issues

1. **"Command not found"**

   ```bash
   # Make sure you're in the right directory:
   cd /path/to/where/you/put/project_forge.py
   ```

2. **Path Not Found**

   ```bash
   # Make sure to use WSL paths:
   ❌ C:\Projects
   ✅ /mnt/c/Projects
   ```

3. **Python Issues**
   ```bash
   # Install Python & pip:
   sudo apt update
   sudo apt install python3 python3-pip
   ```

# 🎮 Using The Project|Forge

## Interactive Mode - Your Main Interface

```bash
# Start the program:
python3 project_forge.py

# You'll see this menu:
==================================================
                Project|Forge
==================================================
1. Create new project
2. Organize existing project
3. Move project between statuses
4. List all projects
5. Exit
```

## 🎯 Common Use Cases

### 1. Starting a New Project

```bash
Select option: 1

Enter project name: My_Arduino_Project
# Pro tip: Use underscores for spaces!

Select status:
1. ONGOING: Active projects     # Choose this for new projects
2. IDEAS: Future plans
3. HOLD: Paused projects
4. DONE: Completed projects
5. Test_And_Experiments        # Good for quick tests
6. Code_Archives              # For code snippets
```

### 2. Cleaning Up Messy Projects

```bash
Select option: 2

Select type:
1. Full Project    # Choose this for complete projects
2. Code Snippets   # For single files/small code bits

Enter path: /mnt/c/Users/YourName/Desktop/messy_project
# Remember to use WSL paths!
```

### 3. Moving Projects (e.g., from ONGOING to DONE)

```bash
Select option: 3
# Just follow the prompts - it's easy!
```

## 📁 Real World Examples

### Example 1: Arduino Project Organization

Before (Messy Desktop):

```
Desktop/
├── led_code.ino
├── schematic.pdf
├── case_v1.stl
└── notes.txt
```

After Running Tool:

```
ONGOING/Arduino_LED_Project/
├── software/
│   └── src/
│       └── led_code.ino      # Your code, safe and sound
├── hardware/
│   └── schematics/
│       └── schematic.pdf    # Hardware docs organized
├── cad/
│   └── 3dprint/
│       └── case_v1.stl     # 3D files in the right place
└── _docs/
    └── notes/
        └── notes.txt      # Documentation where it belongs
```

### Example 2: Code Snippet Organization

Turn this:

```
random_folder/
├── uart_code.cpp
├── old_uart.cpp
└── uart.h
```

Into this:

```
Code_Archives/
└── UART_Handler/
    └── UART_Handler.cpp   # Clean, organized, reusable!
```

## 💣 Example 3: Super Messy Project Clean-up

### Initial Chaos (Before):

```
~/Desktop/robot_mess/
├── main_v1.cpp
├── main_final.cpp
├── main_final_GOOD.cpp
├── robot_test.ino
├── servo.h
├── old_servo.h
├── config_backup.h
├── platformio.ini
├── random_todo.txt
├── notes_jan15.txt
├── meeting_notes.md
├── schematic_v1.pdf
├── schematic_FINAL.pdf
├── pcb_design.kicad_pcb
├── gerbers.zip
├── BOM_v2.xlsx
├── parts_list.csv
├── robot_case.f3d
├── case_v1.stl
├── case_v2.stl
├── case_final.stl
├── IMG_001.jpg
├── wiring_diagram.jpg
└── project_photo.jpg
```

## 🎯 Organization Process - Step by Step

```bash
$ python3 project_forge.py

Select option: 2  # Organize existing project
Select type: 1    # Full Project

# Providing paths
Enter source: ~/Desktop/robot_mess
Enter name: Robot_Arm_Project
```

### 🔍 What's Happening Behind the Scenes:

1. **Project Analysis**

   ```bash
   Analyzing project structure...
   - Found PlatformIO config (platformio.ini)
   - Found Arduino sketches (.ino)
   - Detected 23 files to organize
   ```

2. **Smart Detection**

   ```bash
   Detected project types:
   ✓ PlatformIO project
   ✓ Arduino sketches
   ✓ CAD files present
   ✓ Hardware documentation
   ```

3. **File Analysis**

   ```bash
   Analyzing files:
   - Found multiple main file versions
   - Found scattered documentation
   - Found CAD iterations
   - Found hardware design files
   ```

4. **Organization Actions**
   ```bash
   Performing organization:
   → Moving source files to software/
   → Consolidating documentation to _docs/
   → Organizing CAD files
   → Structuring hardware files
   ```

### 📊 Organization Results (After):

(See detailed structure in previous example)

### 🎯 What The Tool Did:

1. **Code Management**

   ```bash
   Software cleanup:
   ✓ Detected main version files
   ✓ Created archive for old versions
   ✓ Preserved build configurations
   ✓ Organized libraries
   ```

2. **Documentation Organization**

   ```bash
   Documentation cleanup:
   ✓ Gathered scattered notes
   ✓ Organized by type (notes, images)
   ✓ Maintained date context
   ✓ Structured for easy access
   ```

3. **Hardware Files**

   ```bash
   Hardware file organization:
   ✓ Separated schematics versions
   ✓ Organized production files
   ✓ Structured BOMs and parts lists
   ```

4. **CAD Files**
   ```bash
   CAD file management:
   ✓ Separated source and output files
   ✓ Organized STL versions
   ✓ Maintained original CAD files
   ```

### 🎉 Final Results:

```bash
Organization Complete!

Files Processed: 23
├── Software Files: 8
├── Documentation: 6
├── Hardware Files: 5
└── CAD Files: 4

Structure Compliance: 100%
File Naming: Standardized
Version Control Ready: Yes
```

## ✨ Final Project Structure

```
Robot_Arm_Project/                 # Your organized project
│
├── 📂 software/                   # All code in one place
│   ├── 📂 src/                    # Current source code
│   │   ├── 📜 Main.cpp            # Main program
│   │   ├── 📜 Robot.ino          # Arduino sketch
│   │   └── 📜 Config.h           # Configuration
│   │
│   ├── 📂 libs/                   # Project libraries
│   │   ├── 📜 ServoLib.cpp       # Servo control
│   │   └── 📜 ServoHandler.h     # Servo headers
│   │
│   ├── 📂 archive/                # Old versions, safe but out of the way
│   │   ├── 📜 Main_v1.cpp
│   │   └── 📜 Main_backup.cpp
│   │
│   └── 📜 platformio.ini         # Build configuration
│
├── 📂 hardware/                   # All hardware files
│   ├── 📂 schematics/
│   │   ├── 📜 Schematic_v2.pdf   # Current version
│   │   └── 📜 Schematic_v1.pdf   # Previous version
│   │
│   ├── 📂 pcb/                   # PCB design files
│   │   └── 📜 MainBoard.kicad_pcb
│   │
│   └── 📂 production/            # Manufacturing files
│       ├── 📂 gerber/
│       │   └── 📦 Gerbers.zip
│       └── 📂 assembly/
│           └── 📊 BOM.xlsx
│
├── 📂 cad/                       # 3D design files
│   ├── 📂 models/                # Source files
│   │   └── 📜 RobotCase.f3d     # Fusion 360 file
│   │
│   └── 📂 3dprint/              # Print files
│       └── 📂 stl/
│           ├── 📜 Case.stl
│           └── 📜 Mount.stl
│
├── 📂 _docs/                     # All documentation
│   ├── 📂 notes/                 # Project notes
│   │   ├── 📝 BuildNotes.txt
│   │   └── 📝 TODO.md
│   │
│   ├── 📂 images/               # Project images
│   │   ├── 📸 Prototype.jpg
│   │   └── 📸 Wiring.jpg
│   │
│   └── 📂 diagrams/             # Technical diagrams
│       └── 📊 Pinout.svg
│
├── 📜 README.md                  # Project documentation
└── 📜 project.yaml              # Project metadata

```

## 📊 Organization Statistics

```
Files Organized: 23 total
│
├── 📊 By Category
│   ├── Software: 35% (8 files)
│   ├── Hardware: 22% (5 files)
│   ├── CAD: 17% (4 files)
│   └── Docs: 26% (6 files)
│
└── 📈 Results
    ├── Structure: 100% compliant
    ├── Naming: Standardized
    ├── Versions: Tracked
    └── Ready for: Git, Sharing, Team Work
```

## 💡 Pro Tips

### For Windows Users

- Always use `/mnt/c/...` style paths
- Copy-paste paths from Windows Explorer and add `/mnt/c/` at start
- Use Tab completion in WSL to verify paths

### For Project Organization

- Use descriptive project names
- Start with ONGOING or Test_And_Experiments
- Move to DONE when complete
- Use Code_Archives for useful snippets

### For Arduino/PlatformIO Projects

The tool automatically:

- Detects project type
- Preserves build settings
- Keeps libraries intact
- Organizes supporting files

## 🔮 Coming Soon

- [ ] Project templates
- [ ] Backup features
- [ ] Git integration
- [ ] Project health checks

## 🆘 Need Help?

### Common Questions

1. "Where should I put my project?"

   - ONGOING: For active projects
   - Test_And_Experiments: For quick tests
   - Code_Archives: For useful code bits

2. "What happens to my original files?"

   - They stay where they are
   - Tool creates organized copy
   - Original files untouched

3. "I messed up the organization!"
   - Just run again with a new project name
   - Original files are safe
   - Try different organization patterns

## 🤝 Contributing

Love organizing? Got ideas? Contributions welcome!

1. Fork the repo
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Inspired by every maker's need for organization
- Built with ❤️ for the maker community
- Thanks to all contributors!

---

Made with 🛠️ by [SKTech] - For Makers, By Makers!
