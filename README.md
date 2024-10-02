# 🛠️ Mechanic Tools Management
Mechanic Tools Management is a web application developed with Flask that allows you to manage mechanics, tools, perform daily inventory checks, and generate PDF reports on missing tools.

## 📑 Table of Contents
- [Key Features](#-key-features)
- [Demonstration Video]
- [How It Works](#-how-it-works)
- [Tools and Technologies Used](#-tools-and-technologies-used)
- [Prerequisites](#-prerequisites)
- [Installation Instructions](#-installation-instructions)
    - [Clone this repository](#1-clone-this-repository)
    - [Navigate to the project directory](#2-navigate-to-the-project-directory)
    - [Create and activate a virtual environment](#3-create-and-activate-a-virtual-environment)
        - [Install the virtualenv library](#31-install-the-virtualenv-library)
        - [Create a virtual environment named venv](#32-then-create-a-virtual-environment-named-venv)
            - [Linux or macOS](#linux-or-macos)
            - [Windows](#windows)
        - [Activate the virtual environment](#33-activate-the-virtual-environment)
            - [Linux or macOS](#linux-or-macos-1)
            - [Windows](#windows-1)
    - [Install dependencies]
    - [Configure the database]
    - [Run the application]
📌 Observations

## 🚀 Key Features
- **Mechanic and Tool Management:** Allows adding, editing, viewing, and deleting mechanics and tools.
- **Default Inventory:** Assigns a standard set of tools to each mechanic, simplifying inventory management.
- **Daily Tool Conference:** Records missing tools during daily conferences based on the default inventory.
- **PDF Report Generation:** Creates daily and aggregate reports on missing tools, as well as inventory checklists per mechanic.
- **RESTful API:** Provides endpoints for interacting with the application, enabling future integrations or frontend development.

## 📹 Demonstration Video

## 💡 How It Works
- **Data Management:**
  - **Mechanics:** Add, edit, view, and delete mechanic information.
  - **Tools:** Manage the available tools catalog, including name and category.
- **Default Inventory:**
  - Assign a standard set of tools to each mechanic, facilitating initial setup and ensuring each mechanic has the necessary tools.
- **Daily Conference:**
  - Conduct daily conferences where mechanics report the tools they have. The application identifies which tools are missing based on the default inventory and records these absences.
- **Report Generation:**
  - **Daily Report:** Lists the missing tools on a specific date, grouped by mechanic.
  - **Aggregate Report:** Shows the number of missing instances per tool on a specific date.
  - **Inventory Checklist:** Generates a checklist of standard tools grouped by category for each mechanic.

## 🔧 Tools and Technologies Used
- [**Flask:**](https://flask.palletsprojects.com/en/3.0.x/) A lightweight and flexible web framework for Python application development.
- [**SQLAlchemy:**](https://www.sqlalchemy.org/) An ORM (Object-Relational Mapping) tool for efficient database interactions.
- [**SQLite:**](https://www.sqlite.org/) A lightweight database used for data storage.
- [**ReportLab:**](https://www.reportlab.com/) A library for generating PDF documents.
- [**Python:**](https://www.python.org/) A versatile and widely-used programming language.

## 📋 Prerequisites
Before running the application, ensure you have the following prerequisites installed:
- [**Git:**](https://git-scm.com/downloads) A distributed version control system.
- [**Python 3.7+**](https://www.python.org/downloads/) A compatible version of Python.
- [**Pip:**](https://pip.pypa.io/en/stable/installation/) A package manager for installing and managing Python libraries.
- [**Virtualenv:**](https://virtualenv.pypa.io/en/latest/) A tool for creating Python virtual environments.

## 📝 Installation Instructions
### 1. Clone this repository
```bash
git clone https://github.com/Eloin-Centro-Automotivo/toolbox-backend.git
```
### 2. Navigate to the project directory
```bash
cd toolbox-backend
```
### 3. Create and activate a virtual environment
- #### 3.1. Install the virtualenv library
    ```bash
    pip install virtualenv
    ```
- #### 3.2. Then, create a virtual environment named `venv`
  - ##### Linux or macOS
      ```bash
      virtualenv venv
      ```
  - ##### Windows
      ```bash
      python -m virtualenv venv
      ```
- #### 3.3. Activate the virtual environment
    - ##### Linux or macOS
        ```bash
        source venv/bin/activate
        ```
    - ##### Windows
        ```bash
        .\venv\Scripts\activate.bat
        ```
    
