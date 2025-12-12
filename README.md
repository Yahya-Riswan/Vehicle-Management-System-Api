Here is a professional README.md file tailored for your Zeymoto Vehicle Management System API. You can copy and paste this directly into a file named README.md in your api folder or the root folder.🏍️ Zeymoto - Vehicle Management System APIA high-performance, RESTful API built with FastAPI and TiDB (Serverless MySQL) to manage a used bike dealership. This system handles staff authentication, inventory management, and sales tracking.🚀 Tech StackFramework: FastAPI (Python)Database: TiDB Serverless (MySQL Compatible)ORM: SQLAlchemyValidation: PydanticAuthentication: Passlib (Bcrypt)Deployment: Vercel / Render / Local✨ FeaturesStaff Management🔐 Authentication: Secure Login & Registration with password hashing.👥 CRUD Operations: Create, Read, Update, and Delete staff members.🛡️ Role-Based: Tracks staff roles (e.g., Admin, Salesman).Database Integration☁️ Cloud Native: Connects securely to TiDB Cloud using SSL.⚡ Connection Pooling: Optimized for serverless environments to prevent timeouts.📂 Project StructurePlaintext├── api/
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
🛠️ Installation & Setup1. PrerequisitesPython 3.9 or higherA TiDB Cloud Account (Free Tier is sufficient)2. Clone the RepositoryBashgit clone https://github.com/your-username/zeymoto-api.git
cd zeymoto/api
3. Install DependenciesIt is recommended to use a virtual environment.Bash# Create virtual environment (optional)
python -m venv venv
# Activate it (Windows)
.\venv\Scripts\activate
# Activate it (Mac/Linux)
source venv/bin/activate

# Install libraries
pip install -r ../requirements.txt
4. Configuration (.env)Create a .env file in the root directory (next to api/) or inside api/ depending on your run context. Add your TiDB credentials:Ini, TOMLTIDB_HOST=gateway01.ap-southeast-1.prod.aws.tidbcloud.com
TIDB_USER=your_tidb_user
TIDB_PASSWORD=your_tidb_password
TIDB_PORT=4000
TIDB_DATABASE=test
🏃‍♂️ Running LocallyTo start the server, run the following command from the api folder:Bashuvicorn index:app --reload
Server URL: http://127.0.0.1:8000Interactive Docs: http://127.0.0.1:8000/docs (Swagger UI)Alternative Docs: http://127.0.0.1:8000/redoc🔌 API EndpointsStaff (/staff)MethodEndpointDescriptionGET/staff/Get list of all staff membersPOST/staff/registerRegister a new staff memberGET/staff/loginLogin (Returns staff details on success)GET/staff/{id}Get specific staff detailsPUT/staff/{id}Update staff informationDELETE/staff/{id}Remove a staff member⚠️ Common Issues & Fixes1. ModuleNotFoundError: No module named 'routers'Fix: Ensure you are running uvicorn from the correct directory. If you are inside the api folder, use uvicorn index:app --reload. If you are outside, use uvicorn api.index:app --reload.2. SSL: CERTIFICATE_VERIFY_FAILEDFix: The database.py file includes a smart switch. It automatically disables strict SSL verification when running on local Windows machines while keeping it secure for production.3. ValueError: password cannot be longer than 72 bytesFix: This is a version conflict between passlib and bcrypt. Run pip install "bcrypt==4.0.1" to fix it.🚀 Deployment (Vercel)Install Vercel CLI: npm i -g vercelLogin: vercel loginDeploy: vercelImportant: Go to Vercel Dashboard -> Settings -> Environment Variables and add all your .env values there (TIDB_HOST, TIDB_PASSWORD, etc.).📜 LicenseThis project is licensed under the MIT License.
