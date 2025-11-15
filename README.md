# AI-assisted Symbolic Execution for Testing and Repairing Software Systems

This project provides a platform for automated bug detection and repair in C/C++ code using symbolic execution (KLEE), constraint solving (Z3), and AI-based repair suggestions (transformers).

## Directory Structure

```
.
├── frontend/          # Streamlit frontend
│   └── app.py
├── backend/           # Node.js/Express backend
│   ├── server.js
│   ├── routes/
│   │   ├── auth.js
│   │   ├── upload.js
│   │   └── reports.js
│   └── package.json
├── symbolic_execution/ # Python pipeline for KLEE and Z3
│   └── pipeline.py
├── ai_repair/         # AI repair module
│   └── repair.py
├── database/          # MongoDB schemas
│   └── schemas.js
├── samples/           # Sample C files for testing
├── docs/              # Documentation
├── requirements.txt   # Python dependencies
├── install_klee.sh    # KLEE installation script
├── install_z3.sh      # Z3 installation script
└── README.md
```

## Setup Instructions

1. **Install MongoDB**: Follow [official docs](https://docs.mongodb.com/manual/installation/) to install MongoDB locally.

2. **Install KLEE**:
   ```bash
   chmod +x install_klee.sh
   ./install_klee.sh
   ```

3. **Install Z3**:
   ```bash
   chmod +x install_z3.sh
   ./install_z3.sh
   ```

4. **Install Backend Dependencies**:
   ```bash
   cd backend
   npm install
   cd ..
   ```

5. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the System

1. **Start MongoDB**:
   ```bash
   mongod
   ```

2. **Start Backend**:
   ```bash
   cd backend
   npm start
   ```

3. **Start Frontend**:
   ```bash
   streamlit run frontend/app.py
   ```

## APIs

- **POST /api/auth/register**: Register a new user.
- **POST /api/auth/login**: Login and get JWT token.
- **POST /api/upload**: Upload code file for analysis (requires auth).
- **GET /api/reports**: Get user's bug reports (requires auth).
- **GET /api/reports/:id**: Get specific report (requires auth).

## End-to-End Workflow

1. User registers/logs in via Streamlit UI.
2. Uploads C/C++ code file.
3. Backend saves file and triggers Python pipeline.
4. Pipeline compiles code with LLVM, runs KLEE for symbolic execution.
5. Uses Z3 to check constraints.
6. Calls AI repair to generate suggestions.
7. Stores results in MongoDB.
8. User views reports and visualizations in dashboard.

## Sample Test Cases

See `samples/` directory for example C files with bugs.

## Demo Run-Through

1. Register/Login in the app.
2. Upload a sample C file (e.g., `samples/buggy.c`).
3. Wait for analysis (may take time for KLEE).
4. View bugs and repair suggestions in dashboard.
5. Visualize bug counts with charts.

## Technologies Used

- Frontend: Streamlit
- Backend: Node.js, Express
- Database: MongoDB
- Symbolic Execution: KLEE
- Constraint Solver: Z3
- AI Repair: Transformers (Hugging Face)
# Ai_testing_and_repairing
