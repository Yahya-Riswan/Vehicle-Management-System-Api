# 🏍️ Vehicle Management System API

A high-performance, RESTful API built with **FastAPI** and **TiDB (Serverless MySQL)** to manage a used bike dealership. This system handles staff authentication, inventory management, and sales tracking.

## 🚀 Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
* **Database:** [TiDB Serverless](https://tidbcloud.com/) (MySQL Compatible)
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
* **Validation:** [Pydantic](https://docs.pydantic.dev/)
* **Authentication:** Passlib (Bcrypt)
* **Deployment:** Vercel / Render / Local

---

## ✨ Features

* **Staff Management**
    * 🔐 **Authentication:** Secure Login & Registration with password hashing.
    * 👥 **CRUD Operations:** Create, Read, Update, and Delete staff members.
    * 🛡️ **Role-Based:** Tracks staff roles (e.g., Admin, Salesman).
* **Database Integration**
    * ☁️ **Cloud Native:** Connects securely to TiDB Cloud using SSL.
    * ⚡ **Connection Pooling:** Optimized for serverless environments to prevent timeouts.

---

## 📂 Project Structure

```text
├── api/
│   ├── database.py       # Database connection & session handling
│   ├── index.py          # Main application entry point
│   ├── models/           # SQLAlchemy Database Models (Tables)
│   │   ├── __init__.py
│   │   └── staff.py
│   ├── routers/          # API Route Logic (Endpoints)
│   │   └── staff.py
│   └── schemas/          # Pydantic Schemas (Data Validation)
│       ├── __init__.py
│       └── staff.py
├── .env                  # Environment Variables (Secrets)
├── requirements.txt      # Python Dependencies
└── vercel.json           # Deployment Configuration
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
* Python 3.9 or higher
* A TiDB Cloud Account (Free Tier is sufficient)

### 2. Clone the Repository
```bash
git clone [https://github.com/your-username/zeymoto-api.git](https://github.com/your-username/zeymoto-api.git)
cd zeymoto/api
```

### 3. Install Dependencies
It is recommended to use a virtual environment.
```bash
# Create virtual environment (optional)
python -m venv venv
# Activate it (Windows)
.\venv\Scripts\activate
# Activate it (Mac/Linux)
source venv/bin/activate

# Install libraries
pip install -r ../requirements.txt
```

### 4. Configuration (`.env`)
Create a `.env` file in the `api` directory. Add your TiDB credentials:

```ini
TIDB_HOST=gateway01.ap-southeast-1.prod.aws.tidbcloud.com
TIDB_USER=your_tidb_user
TIDB_PASSWORD=your_tidb_password
TIDB_PORT=4000
TIDB_DATABASE=test
```

---

## 🏃‍♂️ Running Locally

To start the server, run the following command from the **`api`** folder:

```bash
uvicorn index:app --reload
```

* **Server URL:** `http://127.0.0.1:8000`
* **Interactive Docs:** `http://127.0.0.1:8000/docs` (Swagger UI)
* **Alternative Docs:** `http://127.0.0.1:8000/redoc`

---

## 🔌 API Endpoints

### Staff (`/staff`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/staff/` | Get list of all staff members |
| `POST` | `/staff/register` | Register a new staff member |
| `GET` | `/staff/login` | Login (Returns staff details on success) |
| `GET` | `/staff/{id}` | Get specific staff details |
| `PUT` | `/staff/{id}` | Update staff information |
| `DELETE` | `/staff/{id}` | Remove a staff member |

---

## ⚠️ Common Issues & Fixes

**1. `AttributeError: module 'bcrypt' has no attribute '__about__'`**
* **Cause:** Incompatibility between `passlib` and newer versions of `bcrypt`.
* **Fix:** Downgrade bcrypt to a compatible version:
  ```bash
  pip install "bcrypt==4.0.1"
  ```

**2. `ModuleNotFoundError: No module named 'routers'`**
* **Fix:** Ensure you are running `uvicorn` from the correct directory. If you are inside the `api` folder, use `uvicorn index:app --reload`.

**3. `SSL: CERTIFICATE_VERIFY_FAILED`**
* **Fix:** The `database.py` file includes a smart switch. It automatically disables strict SSL verification when running on local Windows machines while keeping it secure for production.

---

## 🚀 Deployment (Vercel)

1.  Install Vercel CLI: `npm i -g vercel`
2.  Login: `vercel login`
3.  Deploy: `vercel`
4.  **Important:** Go to Vercel Dashboard -> Settings -> Environment Variables and add all your `.env` values there (`TIDB_HOST`, `TIDB_PASSWORD`, etc.).

---

## 📜 License
This project is licensed under the MIT License.
