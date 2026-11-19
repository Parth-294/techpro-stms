# TechPro Solutions - Service Ticket Management System (STMS)
**Module:** UMDCOM202 Software Engineering  
**Student Name:** Parth Patel  
**Institution:** University of Suffolk (in partnership with Unicaf)  
**System Version:** v1.0.0 (Production Release)  

---

## 1. Project Overview
The **Service Ticket Management System (STMS)** is a secure, role-based desktop software solution engineered for **TechPro Solutions**, a technical support and IT services provider. 

The application implements a robust **Model-View-Controller (MVC)** and **Layered Architecture** utilizing Python, SQLite, and `tkinter`. It governs the full end-to-end lifecycle of technical support tickets across three distinct enterprise user roles:
* **Customers:** Report technical incidents, select urgency/priority levels, and track real-time resolution progress.
* **Support Engineers:** Manage personally assigned work queues, advance ticket resolution stages, and trigger automated audit trails.
* **Administrators:** Exercise global system oversight, monitor enterprise ticket distributions, and dynamically allocate engineers.

---

## 2. Technology Stack & Architectural Design
* **Programming Language:** Python 3.x (Object-Oriented Design with inheritance and polymorphism)
* **Graphical User Interface (GUI):** Python `tkinter` and `ttk` themed components (850×600 responsive desktop window)
* **Database & Persistence:** SQLite3 with relational foreign keys (`PRAGMA foreign_keys = ON;`)
* **Security & Access Control:** Cryptographic SHA-256 password hashing via standard `hashlib` and Role-Based Access Control (RBAC)
* **Verification & QA:** Automated test suite implemented using Python's standard `unittest` framework

---

## 3. Installation & Setup Prerequisites
1. **Python Installation:** Ensure **Python 3.8+** is installed on your system (tested and verified on **Python 3.13**).
2. **Zero External Dependencies:** No external third-party packages or `pip` modules are required. All libraries (`tkinter`, `sqlite3`, `hashlib`, `unittest`) are included natively in Python's standard library.

---

## 4. How to Run the Application & Tests

### Running the Desktop GUI Application
From the project root directory (`TechPro_STMS_Submission/`), execute:
```bash
python src/app.py
```
*(Alternatively, navigate into `src/` and run `python app.py`. The database connection path resolves dynamically.)*

### Running the Automated Unit Test Suite
To verify the system's core business logic, authentication security, role inheritance, and database integrity, run:
```bash
python -m unittest -v tests/test_system.py
```
*(The complete verified terminal test execution log is permanently recorded in `tests/test_output.txt`.)*

---

## 5. Demo Accounts & Credentials Matrix
The system is pre-populated with five default user accounts across all roles (default password for all demo users is `password123`):

| Role | Username | Password | Operational Capabilities |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin_boss` | `password123` | Full visibility across all system tickets; dynamic dropdown engineer assignment. |
| **Support Engineer** | `eng_john` | `password123` | View assigned ticket queue; update status (*In Progress &rarr; Resolved &rarr; Closed*); triggers audit log. |
| **Support Engineer** | `eng_sarah` | `password123` | Alternate engineer account for multi-agent workload distribution testing. |
| **Customer** | `cust_alice` | `password123` | Submit support tickets (Title, Priority, Description); track own tickets. |
| **Customer** | `cust_bob` | `password123` | Secondary customer account verifying data privacy and user isolation. |

---

## 6. Project Directory Structure
```text
TechPro_STMS_Submission/
├── README.md                          # Quick overview, project summary & setup steps
├── src/                               # Source Code (MVC Architecture)
│   ├── app.py                         # Main application entry point & Tkinter GUI
│   ├── models.py                      # User, Customer, Engineer, Admin OOP classes
│   └── database.py                    # Database connection & SQLite query functions
├── database/                          # Data Storage & Setup
│   └── techpro_stms.db                # SQLite database file (pre-populated with demo data)
├── tests/                             # Verification & Quality Assurance
│   ├── test_system.py                 # Automated unittest script
│   └── test_output.txt                # Terminal test execution log output
├── docs/                              # Software Documentation
│   └── User_Manual.pdf                # Setup guide & role-based instructions (Admin, Engineer, Customer)
├── screenshots/                       # Evidence of Verification & UI Workflows
│   ├── 01_login_screen.png            # Login interface with demo credentials
│   ├── 02_customer_dashboard.png      # Ticket creation form & status view
│   ├── 03_admin_dashboard.png         # All tickets view & dynamic engineer assignment dropdown
│   ├── 04_engineer_dashboard.png      # Assigned tickets & status update interface
│   └── 05_unittest_results.png        # Terminal output screenshot showing 5 passed tests
└── reports/                           # Included Copy of Assessment Documents
    ├── Part1_Software_Design_Proposal.pdf
    └── Part3_Reflective_Essay.pdf
```

---

## 7. Software Documentation & Evidence
* **User Manual:** A comprehensive role-by-role guide complete with embedded interface walkthroughs is located in [`docs/User_Manual.pdf`](docs/User_Manual.pdf).
* **Test Verification Log:** The raw terminal output verifying all 5 automated unit test passes is in [`tests/test_output.txt`](tests/test_output.txt).
* **Assessment Reports:** Copies of the Software Design Proposal (Part 1) and Reflective Essay (Part 3) are provided in the [`reports/`](reports/) directory.
