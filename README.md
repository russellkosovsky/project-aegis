# **Project Aegis: A Resilient Network Simulator**

## **Table of Contents**

1. [Project Description](https://www.google.com/search?q=%23project-description)  
2. [Core Features](https://www.google.com/search?q=%23core-features)  
3. [Technology Stack](https://www.google.com/search?q=%23technology-stack)  
4. [Getting Started](https://www.google.com/search?q=%23getting-started)  
5. [Running the Simulator](https://www.google.com/search?q=%23running-the-simulator)  
   * [Interactive Mode](https://www.google.com/search?q=%23interactive-mode)  
   * [Automated Test Mode](https://www.google.com/search?q=%23automated-test-mode)  
6. [Interactive Commands](https://www.google.com/search?q=%23interactive-commands)  
7. [Project Structure](https://www.google.com/search?q=%23project-structure)  
8. [Development Process](https://www.google.com/search?q=%23development-process)

### **Project Description**

Project Aegis is a Python-based simulation tool designed to model a resilient and distributed communications network, mirroring the complex environments relevant to Nuclear Command, Control, and Communications (NC3). The primary purpose of this simulator is to analyze network performance, test routing protocol resilience, and evaluate the system's integrity when subjected to various disruptions, such as node failures or dynamic link degradation.

This project serves as a practical application of software engineering principles, including object-oriented design, agile methodologies, and DevSecOps practices.

### **Core Features**

* **Configurable Network Topology:** Define complex networks with nodes and weighted links using a simple network\_config.yml file.  
* **Advanced Pathfinding:** Utilizes **Dijkstra's algorithm** to find the fastest path based on link latency, not just the number of hops.  
* **Resilience Simulation:** Interactively take nodes offline or modify link latencies to simulate network disruptions and observe how the system adapts.  
* **Interactive CLI:** A command-line interface allows for real-time control over the simulation, perfect for live demonstrations and scenario testing.  
* **Automated Test Suite:** A comprehensive test suite using pytest and unittest.mock ensures code quality and prevents regressions.  
* **Topology Visualization:** Generate .png images of the network graph using matplotlib and networkx, with nodes color-coded by status.  
* **Event Reporting:** Log all message routing events during a session and export the data to a .csv file for analysis.  
* **Schema Validation:** Ensures the integrity of the network configuration file at startup using jsonschema.

### **Technology Stack**

* **Backend:** Python 3  
* **Core Libraries:** networkx (Graph Theory), matplotlib (Visualization), PyYAML (Config Parsing), jsonschema (Validation)  
* **Testing:** pytest for unit/integration testing, unittest.mock for mocking  
* **Code Quality:** black (Formatter), bandit (SAST)  
* **Version Control & CI/CD:** Git & GitLab  
* **Project Management:** Atlassian Jira & Confluence

### **Getting Started**

Follow these instructions to set up the development environment.

1. **Clone the Repository**  
   git clone https://gitlab.com/russellkosovsky-group/russellkosovsky-project.git  
   cd project-aegis

2. **Create and Activate a Virtual Environment**  
   \# For macOS / Linux  
   python3 \-m venv venv  
   source venv/bin/activate

3. **Install Dependencies**  
   pip install \-r requirements.txt

### **Running the Simulator**

The simulator can be run in two modes from the root project directory.

#### **Interactive Mode**

This is the default mode, which launches the command-line interface.

python main.py  
\# OR explicitly  
python main.py \--mode interactive

#### **Automated Test Mode**

This mode runs a predefined script that showcases several features, generates output files, and then exits.

python main.py \--mode auto

### **Interactive Commands**

| Command | Description |
| :---- | :---- |
| status | Shows the status (ONLINE/OFFLINE) and neighbors of all nodes. |
| visualize \[filename.png\] | Generates a .png image of the network topology. |
| path \<from\> \<to\> | Finds and displays the fastest path and total latency between two nodes. |
| route \<from\> \<to\> \<payload\> | Routes a message from a source to a destination node. |
| set\_latency \<from\> \<to\> \<ms\> | Changes the latency of a link between two nodes. |
| offline \<node\_name\> | Takes a specified node offline. |
| online \<node\_name\> | Brings a specified node back online. |
| report \[filename.csv\] | Saves the session log to a .csv file. |
| help | Displays the list of available commands. |
| exit / quit | Exits the simulator. |

### **Project Structure**

project-aegis/  
│  
├── output/                 \# Generated reports and images  
│   ├── csv/  
│   └── png/  
│  
├── src/                    \# Main source code for the application  
│   ├── \_\_init\_\_.py  
│   ├── models.py           \# Core classes (Node, Message, Network)  
│   ├── reporter.py         \# CSV reporting logic  
│   ├── validator.py        \# Configuration schema and validation  
│   └── visualizer.py       \# Graph visualization logic  
│  
├── tests/                  \# Test suite for the project
│   ├── test_main.py
│   ├── test_models.py  
│   └── test_reporter.py
│  
├── .gitlab-ci.yml          \# GitLab CI/CD pipeline configuration  
├── .gitignore              \# Specifies intentionally untracked files  
├── main.py                 \# Main application entry point (CLI)  
├── network\_config.yml      \# Network topology definition  
├── pytest.ini              \# Pytest configuration  
├── pyproject.toml          \# Python project definition  
├── README.md               \# This file  
└── requirements.txt        \# Project dependencies

### **Development Process**

This project adheres to an agile development methodology and utilizes GitLab for CI/CD.

* **Branching Strategy:** Development follows a GitFlow-like model.  
* **Merge Requests:** All new code must be submitted through a GitLab Merge Request.  
* **CI/CD Pipeline:** Each merge request automatically triggers a CI pipeline that runs the pytest suite and a bandit security scan. A successful pipeline is required for a merge.