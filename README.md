# Project Aegis: NC3 Network Simulator

## Table of Contents
1.  [Project Description](#project-description)
2.  [Core Features](#core-features)
3.  [Technology Stack](#technology-stack)
4.  [Project Structure](#project-structure)
5.  [Getting Started](#getting-started)
6.  [Running Tests](#running-tests)
7.  [Development Process](#development-process)

---

### Project Description

Project Aegis is a Python-based simulation tool designed to model a resilient and distributed communications network, mirroring the complex environments relevant to Nuclear Command, Control, and Communications (NC3). The primary purpose of this simulator is to analyze network performance, test routing protocol resilience, and evaluate the system's integrity when subjected to various disruptions, such as node failures or link degradation.

This project serves as a practical application of software engineering principles, including object-oriented design, agile methodologies, and DevSecOps practices.

### Core Features

* **Network Modeling:** Dynamically create network topologies consisting of interconnected nodes (e.g., ground stations, mobile units, satellites).
* **Object-Oriented Design:** Utilizes a clear, modular structure with classes for `Node`, `Message`, `Network`, and other core components.
* **Event-Driven Simulation:** The simulator operates on a queue of events, allowing for complex and time-dependent interactions.
* **Resilience Testing:** Functionality to simulate network disruptions, such as shutting down nodes or severing links, to observe network recovery and message rerouting.
* **Logging and Analysis:** Comprehensive logging of all simulation events to allow for post-run analysis of message latency, path efficiency, and network stability.

### Technology Stack

* **Backend:** Python 3
* **Testing:** `pytest` for unit and integration testing
* **Security:** `bandit` for Static Application Security Testing (SAST)
* **Version Control:** Git
* **CI/CD & Hosting:** GitLab
* **Project Management:** Atlassian Jira (Agile Kanban/Sprints)
* **Documentation:** Atlassian Confluence

### Project Structure

The repository is organized to separate application logic from testing and documentation.

project-aegis/
│
├── src/                  # Main source code for the application
│   ├── init.py
│   └── models.py         # Core classes (Node, Message, Network)
│
├── tests/                # Test suite
│   └── test_models.py    # Tests for the core classes
│
├── .gitignore            # Specifies intentionally untracked files
├── README.md             # This file
└── requirements.txt      # Project dependencies

### Getting Started

Follow these instructions to set up the development environment on a local machine.

1.  **Clone the Repository**
    ```bash
    git clone <your-gitlab-repo-url>
    cd project-aegis
    ```

2.  **Create and Activate a Python Virtual Environment**
    This isolates the project's dependencies from the system-wide Python installation.
    ```bash
    # For macOS / Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    The `requirements.txt` file contains all necessary Python packages.
    ```bash
    pip install -r requirements.txt
    ```

### Running Tests

To ensure the integrity of the codebase, run the test suite using `pytest`.

From the root `project-aegis` directory, execute the following command:
```bash
pytest

The test runner will automatically discover and execute all tests located in the tests/ directory.


