# 🔧 AutoService Management System

> A web-based automotive service management platform developed as a **team coursework project at Kaunas University of Technology (KTU)** for the **Fundamentals of Information Systems** module.

AutoService is designed to digitalize the day-to-day operations of an automotive service center by centralizing **customers, employees, appointments, repair orders, vehicles, services, spare parts, inventory, invoices, and payments** in one system.

The project addresses common problems in automotive service centers, including information being lost through verbal communication or paper records, scheduling conflicts, insufficient spare parts, and limited visibility into repair progress.

**🚧 Project status:** In development  
**🎓 Project type:** KTU team coursework / Information Systems project

---

## ⚡ Quick Start

### Prerequisites

Make sure the following are installed:

- 🐍 **Python 3.12+**
- 🐘 **PostgreSQL**
- 📦 **pip**
- 🔀 **Git**
- 🟢 **Node.js / npm** — required for the Tailwind CSS workflow

Check your versions:

```bash
python --version
pip --version
git --version
psql --version
node --version
npm --version
```

### 1. Clone the repository

```bash
git clone <repository-url>
cd AutoService
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
```

**Linux / macOS:**

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows CMD:**

```cmd
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

After activation, your terminal should show:

```text
(.venv)
```

### 4. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a local `.env` file in the project root.

Use `.env.example` as the starting point:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True

DB_NAME=autoservice
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=5432

STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

> 🔐 **Never commit `.env` to Git.** It may contain database credentials, Django secrets, API keys, and payment credentials.

### 6. Create the PostgreSQL database

Open PostgreSQL and create a development database:

```sql
CREATE DATABASE autoservice;
```

Make sure the credentials in `.env` match your local PostgreSQL configuration.

### 7. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create a superuser

```bash
python manage.py createsuperuser
```

### 9. Start the development server

```bash
python manage.py runserver
```

Open:

**http://127.0.0.1:8000/**

Django administration:

**http://127.0.0.1:8000/admin/**

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Objectives](#-key-objectives)
- [User Roles](#-user-roles)
- [System Modules](#-system-modules)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Django Applications](#-django-applications)
- [Development Workflow](#-development-workflow)
- [Development Commands](#-development-commands)
- [Database](#-database)
- [Frontend](#-frontend)
- [Payments](#-payments)
- [External Integrations](#-external-integrations)
- [Security](#-security)
- [Git Workflow](#-git-workflow)
- [System Function Hierarchy](#-system-function-hierarchy)
- [Future Improvements](#-future-improvements)
- [Academic Context](#-academic-context)
- [License](#-license)

---

# 🧭 Overview

Traditional automotive service workflows often rely on paper records, phone calls, or verbal communication. This can result in:

- ❌ Lost or incomplete customer information
- ❌ Multiple appointments being assigned to the same mechanic at the same time
- ❌ Poor visibility into repair progress
- ❌ Outdated or incorrect inventory information
- ❌ Difficulty tracking spare parts used during repairs
- ❌ Manual invoice preparation
- ❌ Inefficient communication between customers and service employees

**AutoService** aims to provide a centralized digital solution for these processes.

### Core workflow

```text
Customer
   │
   ├── Register / Login
   ├── Register Vehicle
   └── Book Appointment
            │
            ▼
     Service Manager
            │
            ├── Review Appointment
            ├── Create Repair Order
            ├── Select Services / Parts
            └── Assign Mechanic
                     │
                     ▼
                  Mechanic
                     │
                     ├── View Assigned Orders
                     ├── Update Repair Status
                     └── Update Inventory
                              │
                              ▼
                           System
                              │
                              ├── Generate Invoice
                              └── Calculate Total
                                      │
                                      ▼
                                   Customer
                                      │
                                      ├── Review Invoice
                                      └── Pay via Stripe
```

---

# 🎯 Key Objectives

The main objective is to create an integrated information system supporting the core operational processes of an automotive service center.

The system is designed to:

- 👥 Centralize customer and employee information
- 📅 Digitalize appointment scheduling
- 🚗 Manage customer vehicles
- 🔧 Organize repair orders and services
- 👨‍🔧 Assign repair orders to mechanics
- 📊 Track repair progress
- 📦 Maintain spare-part inventory
- 🚫 Reduce scheduling conflicts
- 💰 Automatically calculate repair costs
- 🧾 Generate invoices based on completed work
- 💳 Provide electronic payment functionality
- 📧 Notify customers about important order status changes
- 🔐 Provide role-based access to system functionality

---

# 👤 User Roles

The system supports three primary user roles.

## 👔 Service Manager

The **Service Manager** has the broadest access to the system.

Managers can:

- 👨‍🔧 Create and manage mechanic accounts
- 📅 Create and manage appointments
- 🔧 Create and manage repair orders
- 💵 Create services and define service prices
- 📦 Manage spare parts and inventory
- 📋 Monitor repair orders
- 📈 Monitor repair progress
- 🧾 Review invoices
- 💳 Review payment status
- 📊 Review inventory demand forecasts

---

## 🛠️ Mechanic

Mechanics are added to the system by a Service Manager.

Mechanics can:

- 🔑 Log into their assigned account
- 📅 View their work schedule
- 🔧 View assigned repair orders
- 📋 Review repair information
- ✏️ Update assigned repair orders
- 🔄 Update repair status
- 📦 Update spare-part inventory quantities

Mechanics only have access to repair orders assigned to them, while managers can view all repair orders.

---

## 👨‍💼 Customer

Customers manage their own accounts and vehicles.

Customers can:

- 📝 Register an account
- 🔑 Log in and manage their profile
- 🚗 Register vehicles
- 📅 Book appointments
- ✏️ Modify appointments
- 👀 View appointment information
- 📧 Receive repair status notifications
- 🧾 View generated invoices
- 💳 Pay invoices through Stripe
- 🚗 Review vehicle information

---

# 🧩 System Modules

The system is divided into five main functional subsystems.

```text
                    AutoService Management System
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
 User Management        Work Management       Vehicle Management
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
               Inventory              Finance
               Management            Management
```

---

## 1️⃣ User Management

Responsible for authentication, registration, profiles, and user roles.

### Main functionality

- Customer registration
- Customer login
- Customer profile management
- Customer account deletion
- Mechanic account creation
- Mechanic account management
- Role-based authorization
- Email address management
- Password management

Customers create their own accounts, while mechanic accounts are created and managed by service managers.

---

## 2️⃣ Work Management

Responsible for appointments, repair orders, and services.

### Main functionality

- 📅 Appointment creation
- ✏️ Appointment editing
- 👀 Appointment viewing
- 🔧 Repair order creation
- 📋 Repair order management
- 🔄 Repair status management
- 💵 Service creation
- 💰 Service price management
- 👨‍🔧 Mechanic assignment
- 📊 Mechanic workload management

A mechanic is assigned to a repair order using an assignment algorithm that considers factors such as:

- Mechanic availability
- Existing workload
- Required competencies

---

## 3️⃣ Vehicle Management

Responsible for storing and managing customer vehicle information.

### Main functionality

- 🚗 Vehicle registration
- 📋 Vehicle information management
- 🔎 Vehicle lookup
- 👤 Customer-to-vehicle relationships
- 🔐 VIN verification through an external service

Both customers and service managers can register vehicles.

---

## 4️⃣ Inventory Management

Responsible for automotive spare parts and service resources.

### Main functionality

- 📦 Spare-part registration
- 📋 Spare-part information management
- 🔢 Inventory quantity tracking
- 🔄 Inventory updates
- 🧾 Spare-part usage tracking
- ⚠️ Inventory availability checking
- 📈 Demand forecasting

Managers can add new spare parts, while both managers and mechanics can update inventory quantities.

The system is also planned to provide demand forecasting for frequently used automotive parts.

---

## 5️⃣ Financial Management

Responsible for invoice generation, invoice management, and payments.

### Main functionality

- 🧾 Automatic invoice generation
- 👀 Invoice viewing
- 💵 Service cost calculation
- 📦 Spare-part cost calculation
- 🧮 Total repair cost calculation
- 💳 Payment processing
- 🔄 Payment status tracking

An invoice will be calculated from:

```text
Service costs
      +
Used spare parts
      │
      ▼
Total invoice amount
```

Customers will be able to pay invoices electronically through **Stripe**.

---

# 🧱 Technology Stack

The application is planned around a modular Django web architecture.

| Layer | Technology | Purpose |
|---|---|---|
| 🐍 Backend | Python 3.12+ | Application and business logic |
| 🌐 Framework | Django | Web application framework |
| 🐘 Database | PostgreSQL | Relational data storage |
| 🔗 ORM | Django ORM | Database abstraction |
| 📄 Templates | Django Templates | Server-side HTML rendering |
| 🎨 Styling | Tailwind CSS | Utility-first responsive UI |
| 🎨 Custom styling | CSS | Project-specific styles |
| ⚡ Client-side | JavaScript | Browser-side interaction |
| 🧩 JS Library | jQuery | DOM and AJAX utilities |
| 💳 Payments | Stripe | Electronic payment processing |
| 🔀 Version control | Git | Source code management |
| ☁️ Repository | GitHub | Collaboration and code hosting |

---

## 🐍 Python + Django

Python is used for the backend because of its clear syntax, extensive ecosystem, and suitability for web applications.

Django provides the core infrastructure required by the system:

- URL routing
- Request/response handling
- Authentication
- Authorization
- Form processing
- Database access
- ORM
- Session management
- Administrative interface
- Security mechanisms

The **Django ORM** will be used to interact with PostgreSQL through Python models.

---

## 🐘 PostgreSQL

PostgreSQL is the primary database management system.

The database will store information such as:

- Users and roles
- Vehicles
- Appointments
- Repair orders
- Services
- Spare parts
- Inventory quantities
- Invoices
- Payments
- Repair statuses

PostgreSQL was selected because of its:

- ✅ Strong data integrity
- ✅ Transaction support
- ✅ Referential integrity
- ✅ Advanced relational features
- ✅ Django compatibility
- ✅ Scalability

---

## 🎨 Frontend

The frontend will be implemented as a browser-based application using:

- HTML5
- CSS3
- Tailwind CSS
- JavaScript
- jQuery
- Django Templates

### Tailwind CSS

Tailwind CSS will provide the main UI utility framework for:

- Responsive layouts
- Forms
- Navigation
- Tables
- Buttons
- Typography
- Spacing
- Component states

### JavaScript + jQuery

JavaScript and jQuery will be used for interactive functionality such as:

- Dynamic forms
- Appointment selection
- Client-side interactions
- AJAX requests
- Modal windows
- Interactive tables
- Dynamic status updates

---

# 🏗️ Architecture

The application will follow Django's **Model-View-Template (MVT)** architecture.

```text
┌──────────────────────────────────────────────┐
│                 Web Browser                  │
│          HTML / CSS / JavaScript             │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│                    Django                    │
│                                              │
│       URLs → Views → Services → Models      │
│                         │          │         │
│              Authentication       ORM       │
└─────────────────────────┼──────────┼─────────┘
                          │          │
                          ▼          ▼
                    External      PostgreSQL
                    Services       Database
```

### Application responsibilities

```text
HTTP Request
     │
     ▼
   urls.py
     │
     ▼
   views.py
     │
     ▼
 business/service logic
     │
     ▼
  models.py
     │
     ▼
 Django ORM
     │
     ▼
 PostgreSQL
```

Business logic should remain separated from templates and HTTP-specific code wherever practical.

---

# 📁 Project Structure

The project is organized into separate Django applications according to business responsibilities.

```text
AutoService/
│
├── .github/
│   └── function-hierarchy.png
│
├── apps/
│   ├── accounts/
│   ├── workorders/
│   ├── vehicles/
│   ├── inventory/
│   └── billing/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   ├── accounts/
│   ├── workorders/
│   ├── vehicles/
│   ├── inventory/
│   └── billing/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

> 💡 The exact structure may evolve during implementation as requirements and application boundaries are refined.

---

# 🧱 Django Applications

## `accounts`

Handles users, authentication, authorization, and profiles.

Potential responsibilities:

```text
accounts
├── User
├── CustomerProfile
├── MechanicProfile
├── Authentication
├── Authorization
└── Profile management
```

The application will define the project's user model and role-based permissions.

---

## `workorders`

Handles the core service workflow.

Potential entities:

```text
Appointment
RepairOrder
Service
RepairStatus
MechanicAssignment
```

This application connects customers, vehicles, mechanics, services, and repair work.

---

## `vehicles`

Handles vehicle-related information.

Potential entities:

```text
Vehicle
VehicleOwner
```

The application will also contain integration logic for external VIN verification.

---

## `inventory`

Handles spare parts and inventory.

Potential entities:

```text
Part
InventoryItem
InventoryTransaction
```

Inventory transactions can maintain a traceable history of stock changes instead of simply overwriting the current quantity.

---

## `billing`

Handles invoices and payments.

Potential entities:

```text
Invoice
InvoiceItem
Payment
```

The application will also contain the Stripe integration layer.

```text
RepairOrder
     │
     ├── Services
     │
     └── Parts
          │
          ▼
       Invoice
          │
          ▼
       Payment
          │
          ▼
        Stripe
```

---

# 🗄️ Database

The project uses **PostgreSQL** as its primary relational database.

A simplified conceptual model is:

```text
                    ┌──────────┐
                    │   User   │
                    └────┬─────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        ┌───────────┐         ┌──────────┐
        │ Customer  │         │ Mechanic │
        └─────┬─────┘         └────┬─────┘
              │                    │
              ▼                    │
        ┌───────────┐              │
        │  Vehicle  │              │
        └─────┬─────┘              │
              │                    │
              └────────┬───────────┘
                       ▼
                ┌──────────────┐
                │ Repair Order │
                └──────┬───────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
         ┌──────────┐      ┌────────┐
         │ Services │      │ Parts  │
         └────┬─────┘      └───┬────┘
              │                │
              └───────┬────────┘
                      ▼
                ┌──────────┐
                │ Invoice  │
                └────┬─────┘
                     ▼
                ┌──────────┐
                │ Payment  │
                └──────────┘
```

Django migrations will be used to version and manage database schema changes.

---

# 💳 Payments

The system is planned to integrate **Stripe** for electronic invoice payments.

```text
Customer
    │
    ▼
View Invoice
    │
    ▼
Pay Invoice
    │
    ▼
Create Stripe Checkout Session
    │
    ▼
Stripe
    │
    ▼
Payment Completed
    │
    ▼
Webhook
    │
    ▼
Update Payment Status
```

Payment credentials and webhook secrets will be stored exclusively in environment variables.

---

# 🔌 External Integrations

The system is planned to communicate with several external services.

### 💳 Stripe

Used for:

- Electronic payments
- Payment confirmation
- Payment status tracking

### 🚗 VIN Verification Service

Used to retrieve additional vehicle information based on a vehicle identification number.

### 📧 Email Service

Used to notify customers about events such as:

- Appointment information
- Repair status changes
- Completed repairs
- Invoice availability

> ℹ️ Exact providers and implementation details may change during development.

---

# 🔐 Security

Because the system handles customer and payment-related information, security is an important architectural consideration.

Planned security measures include:

- 🔒 Password hashing
- 🛡️ CSRF protection
- 👥 Role-based authorization
- ✅ Server-side validation
- 🔐 Secure session handling
- 🌱 Environment-based secret management
- 🗄️ Database constraints
- 🚪 Permission checks on protected resources
- 🔒 HTTPS in production
- 💳 Stripe webhook signature validation

Sensitive credentials must never be committed to the repository.

---

# 🧪 Development Commands

### Start the development server

```bash
python manage.py runserver
```

### Create migrations

```bash
python manage.py makemigrations
```

### Apply migrations

```bash
python manage.py migrate
```

### Create a superuser

```bash
python manage.py createsuperuser
```

### Run tests

```bash
python manage.py test
```

### Check the Django project

```bash
python manage.py check
```

### Open Django shell

```bash
python manage.py shell
```

### Inspect migrations

```bash
python manage.py showmigrations
```

### Collect static files

```bash
python manage.py collectstatic
```

---

# 🔀 Git Workflow

The project uses Git and GitHub for collaborative development.

The planned branching model is:

```text
                    ┌── feature/*
                    │
main ◄──── dev ◄────┤
                    │
                    └── bugfix/*
```

| Branch | Purpose |
|---|---|
| `main` | Stable / release-ready code |
| `dev` | Integration and development |
| `feature/*` | New functionality |
| `bugfix/*` | Bug fixes |

### Pull Request flow

```text
feature/* → Pull Request → dev → Pull Request → main
```

Direct pushes to `main` should be avoided.

---

# 👥 Team Development

Since this is a team project, development should be organized around clearly separated features and responsibilities.

Example feature areas:

```text
Authentication
Appointment Management
Repair Order Management
Vehicle Management
Inventory Management
Invoice Generation
Stripe Integration
Frontend / UI
```

### Recommended commit style

Good:

```text
Add customer registration
Implement appointment validation
Add vehicle model
Implement mechanic assignment
Add inventory transaction tracking
Integrate Stripe checkout
```

Avoid vague commits:

```text
update
changes
fix
stuff
test
```

Developers should avoid mixing unrelated changes in the same branch.

---

# 📊 System Function Hierarchy

The system's functional hierarchy is divided into five primary subsystems:

```text
                    AutoService Management System
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
       ▼                       ▼                       ▼
 User Management       Work Management       Vehicle Management
       │                       │                       │
       │                       │                       ├── Vehicle Registration
       │                       │                       ├── Vehicle Viewing
       │                       │                       └── VIN Verification
       │                       │
       │                       ├── Appointment Management
       │                       ├── Repair Order Management
       │                       ├── Service Management
       │                       └── Mechanic Assignment
       │
       ├── Registration
       ├── Authentication
       ├── Employee Management
       ├── Profile Management
       └── Notifications
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
          Inventory Management        Financial Management
                 │                           │
                 ├── Part Registration       ├── Invoice Generation
                 ├── Stock Management        ├── Invoice Viewing
                 ├── Stock Updates           ├── Payment Processing
                 └── Demand Forecasting      └── Payment Status
```

### Function hierarchy diagram

The complete functional hierarchy is illustrated below:

![AutoService System Function Hierarchy](.github/function-hierarchy.png)

> 📌 Place the provided hierarchy diagram at `.github/function-hierarchy.png`.

---

# 🚀 Future Improvements

The architecture is designed to allow additional functionality to be introduced as the system evolves.

Potential extensions include:

- 📅 Advanced mechanic scheduling
- ⚖️ Improved workload balancing
- 📈 More sophisticated spare-part demand forecasting
- 📱 SMS notifications
- 🚗 Extended vehicle history
- 📜 Customer service history
- 📊 Advanced reporting and analytics
- 🧾 Extended audit logging
- ⏰ Automated appointment reminders
- 💳 Additional payment providers
- 🔌 REST API
- 🐳 Docker-based development
- ⚙️ CI/CD pipeline
- 📡 Production monitoring

These features are outside the initial coursework scope unless project requirements change.

---

# 🎓 Academic Context

This project is developed as a **team coursework project at Kaunas University of Technology (KTU)** for the module:

> **Fundamentals of Information Systems**

The project focuses not only on implementing a functional web application but also on applying information-system engineering principles.

The project covers:

- 📋 Requirements analysis
- 🧩 System decomposition
- 🌳 Functional hierarchy
- 👥 Role-based access control
- 🗄️ Data modelling
- 🧱 Database design
- 🏗️ Software architecture
- 🔀 Team-based development
- 📝 Version control
- 🔗 Requirements-to-implementation traceability

The functional structure of the system is based on requirements defined during the analysis and design stages of the project.

---

# 📜 License

This project was developed for **educational purposes** as part of a KTU university coursework project.

---

<div align="center">

### 🔧 AutoService Management System

**KTU · Fundamentals of Information Systems · Team Coursework**

Built with 🐍 Python · Django · 🐘 PostgreSQL · 🎨 Tailwind CSS · 💳 Stripe

</div>
