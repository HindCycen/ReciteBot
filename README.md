# ReciteBot - Memorization Learning Assistant

![Godot Engine](https://img.shields.io/badge/Godot-Engine-478cbf?logo=godot-engine)
![C#](https://img.shields.io/badge/C%23-Programming-239120?logo=c-sharp)

ReciteBot is a memorization learning assistant application developed using the Godot Engine, designed specifically for efficient memorization and learning. Through intelligent learning management features, it helps users better master learning content.

*This program is still under development.*

## 📋 Features

- **Intelligent Learning Management**: Unified management of learning data and processes through `StudyManager`
- **Chapter-based Learning**: Supports organizing learning content by chapters for staged memorization
- **Study Set Management**: Flexible creation and management of different study collections
- **Python API Integration**: Integration with external Python scripts for advanced data processing
- **User-friendly Interface**: Intuitive input interface and learning scene design

## 🏗️ Technical Architecture

### Project Structure
```
ReciteBot/
├── Scenes/              # Scene files
│   └── StudyScene.cs    # Main learning scene logic
├── Scripts/             # Core scripts
│   ├── Data/            # Data models
│   │   ├── Chapter.cs   # Chapter data model
│   │   └── StudySet.cs  # Study set data model
│   ├── Manager/         # Managers
│   │   └── StudyManager.cs # Study manager (core)
│   ├── PythonScript/    # External script integration
│   │   └── api_call.py  # Python API call script
│   ├── InputScene.cs    # Input scene logic
│   └── Main.cs          # Main program entry point
└── README.md            # Project documentation
```

### Core Components

- **StudyManager**: Unified data manager responsible for the entire application's data flow and state management
- **Chapter & StudySet**: Data model classes for organizing and storing learning content
- **StudyScene**: Main learning interaction scene
- **InputScene**: User input and configuration interface
- **api_call.py**: External Python script for handling complex API calls or data processing tasks

## 🚀 Usage Instructions

### Requirements
- Godot Engine 4.x
- C# support (.NET 6.0 or higher)
- Python 3.8+ (for external script functionality)

### Installation Steps
1. Clone or download this project locally
2. Open the project with Godot Engine
3. Ensure C# toolchain is properly configured
4. For Python integration features, ensure Python is installed and environment variables are configured

### Running the Application
1. Click the "Play" button in the Godot editor
2. Or export as an executable and run directly

## 🔧 Configuration Guide

### Learning Content Configuration
Learning content is organized through `StudySet` and `Chapter` classes:
- `StudySet`: Represents a complete study collection (e.g., a textbook)
- `Chapter`: Represents specific chapters within a study collection

### Python Integration Configuration
External Python scripts interact with the main program through standard communication mechanisms (such as `OS.execute()` or file I/O), with processing results automatically incorporated into the main application's data flow.

## 📝 Development Guidelines

- **Data Flow Management**: All components must share data through `StudyManager` to avoid data isolation
- **External Script Integration**: Python scripts must be called through standard communication mechanisms, ensuring processing results are correctly transmitted
- **Code Style**: Follow C# naming conventions and Godot best practices

## 🤝 Contribution Guidelines

Issues and Pull Requests are welcome! Please ensure:
1. Follow the project's code guidelines
2. Maintain data flow integrity
3. Thoroughly test new features

## 📄 License

This project is open-sourced under the [MIT License](LICENSE).

## 📧 Contact

For questions or suggestions, please submit feedback through the Issues page.

---

**Happy Learning! 📚**