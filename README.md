# To-Do List API

Dự án tạo API quản lý danh sách công việc (To-Do List) sử dụng FastAPI.

## Cấp 0 — Làm quen FastAPI (Hello To-Do)

### Mục tiêu
Tạo API tối thiểu chạy được với 2 endpoints cơ bản.

### Yêu cầu
- Tạo project FastAPI
- **Endpoint GET /health** → trả `{"status": "ok"}`
- **Endpoint GET /** → trả message chào

### Hướng dẫn chạy

1. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

2. **Chạy server:**
```bash
uvicorn main:app --reload
```

3. **Test endpoints:**
- `http://localhost:8000/` - Xem message chào
- `http://localhost:8000/health` - Kiểm tra trạng thái server
- `http://localhost:8000/docs` - Xem Swagger UI documentation

---
**Status:** ✅ Hoàn thành

## Cấp 1 — CRUD cơ bản (dữ liệu trong RAM)

### Mục tiêu
Implement CRUD với list/dict trong bộ nhớ (chưa dùng DB).

### Model TodoBase
```json
{
  "id": 1,
  "title": "Học lập trình",
  "is_done": false,
  "created_at": "2026-03-13T10:30:00"
}
```

### Endpoints
- **POST /todos** → Tạo todo mới
- **GET /todos** → Lấy danh sách tất cả
- **GET /todos/{id}** → Lấy chi tiết 1 todo
- **PUT /todos/{id}** → Cập nhật todo
- **DELETE /todos/{id}** → Xóa todo

### Tiêu chí đạt
✅ Validate dữ liệu bằng Pydantic  
✅ Trả lỗi 404 khi không tìm thấy  
✅ CRUD đầy đủ

---
**Status:** ✅ Hoàn thành

## Cấp 2 — Validation "xịn" + Filter/Sort/Pagination

### Mục tiêu
API giống thực tế hơn với validation mạnh mẽ và query filters.

### Validation cải tiến
- `title`: Không được rỗng, độ dài 3–100 ký tự

### GET /todos - Query Parameters
```bash
# Filter theo trạng thái
GET /todos?is_done=true
GET /todos?is_done=false

# Search theo title
GET /todos?q=keyword

# Sort
GET /todos?sort=created_at      # tăng dần
GET /todos?sort=-created_at     # giảm dần

# Pagination
GET /todos?limit=20&offset=0

# Kết hợp
GET /todos?is_done=true&q=learn&sort=-created_at&limit=10&offset=0
```

### Response Format
```json
{
  "items": [
    {
      "id": 1,
      "title": "Học FastAPI",
      "is_done": false,
      "created_at": "2026-03-13T10:30:00"
    }
  ],
  "total": 50,
  "limit": 10,
  "offset": 0
}
```

### Tiêu chí đạt
✅ Validation title (3-100 ký tự)  
✅ Filter by is_done  
✅ Search by title  
✅ Sort by created_at  
✅ Pagination (limit, offset)  
✅ Response có structure chuẩn

---
**Status:** ✅ Hoàn thành

## Cấp 3 — Tách tầng (Router/Service/Repository) + Cấu hình

### Mục tiêu
Viết code như dự án thực tế với clean architecture.

### Cấu trúc thư mục
```
app/
├── main.py           # Khởi tạo FastAPI
├── core/
│   ├── __init__.py
│   └── config.py     # Cấu hình từ environment
├── schemas/          # Pydantic models
│   ├── __init__.py
│   └── todo.py
├── repositories/     # Data access layer
│   ├── __init__.py
│   └── todo.py
├── services/         # Business logic layer
│   ├── __init__.py
│   └── todo.py
└── routers/          # Endpoints (controllers)
    ├── __init__.py
    └── todos.py
```

### Key Features
- **Pydantic Settings**: Cấu hình từ env variables (`APP_NAME`, `DEBUG`, etc)
- **APIRouter**: Endpoints tổ chức với prefix `/api/v1`
- **Separation of Concerns**:
  - `routers/` → Xử lý HTTP requests
  - `services/` → Business logic
  - `repositories/` → Data access

### Cấu hình (.env)
```
APP_NAME=To-Do List API
DEBUG=True
VERSION=1.0.0
API_V1_PREFIX=/api/v1
```

### Endpoints sau tách tầng
```
GET    /api/v1/todos
POST   /api/v1/todos
GET    /api/v1/todos/{id}
PUT    /api/v1/todos/{id}
DELETE /api/v1/todos/{id}
```

### Tiêu chí đạt
✅ Tách thư mục (routers, schemas, services, repositories, core)  
✅ Không có business logic trong routers  
✅ Sử dụng APIRouter với prefix  
✅ Config bằng Pydantic Settings  
✅ main.py sạch và đơn giản

---
**Status:** ✅ Hoàn thành

## Cấp 4 — Database (SQLite) + ORM (SQLAlchemy)

### Mục tiêu
Lưu dữ liệu thực sự vào database thay vì RAM.

### Công nghệ
- **Database**: SQLite (dễ học, không cần setup)
- **ORM**: SQLAlchemy để quản lý models
- **Migrations**: Alembic để quản lý schema changes

### Bảng Todos Schema
```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    is_done BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Cấu trúc mới
```
app/core/
├── config.py
├── database.py       # SQLAlchemy engine & session
└── models.py         # SQLAlchemy ORM models

migrations/           # Alembic migrations
├── env.py
├── script.py.mako
└── versions/
    └── 001_initial_migration.py
```

### Endpoints mới/cập nhật
```
GET    /api/v1/todos                    # Lấy danh sách (từ DB)
POST   /api/v1/todos                    # Tạo todo
GET    /api/v1/todos/{id}               # Lấy chi tiết
PUT    /api/v1/todos/{id}               # Cập nhật toàn bộ
PATCH  /api/v1/todos/{id}               # Cập nhật một phần
POST   /api/v1/todos/{id}/complete      # Đánh dấu hoàn thành
DELETE /api/v1/todos/{id}               # Xóa todo
```

### Features
✅ **created_at/updated_at tự động:**
- `created_at`: Được set khi tạo, không thay đổi
- `updated_at`: Tự cập nhật mỗi lần sửa

✅ **PATCH endpoint**: Cập nhật một phần field
```json
PATCH /api/v1/todos/1
{"is_done": true}
```

✅ **POST /complete**: Shortcut để đánh dấu done
```
POST /api/v1/todos/1/complete
```

✅ **Dependency Injection**: Mỗi endpoint nhận DB session tự động

### Hướng dẫn chạy

1. **Cài dependencies:**
```bash
pip install -r requirements.txt
```

2. **Chạy migrations (tạo tables):**
```bash
alembic upgrade head
```

3. **Chạy server:**
```bash
uvicorn main:app --reload
```

4. **Test:**
- Vào [Swagger UI](http://localhost:8000/docs)
- DB file sẽ được tạo ở `./todolist.db`

### Tiêu chí đạt
✅ Dùng SQLAlchemy ORM  
✅ Bảng todos có đầy đủ fields  
✅ created_at/updated_at tự động  
✅ PATCH endpoint  
✅ POST complete endpoint  
✅ Alembic migrations  
✅ Pagination từ DB thực sự

---
**Status:** ✅ Hoàn thành

## Cấp 5 — Authentication + Multi-User (JWT)

### Mục tiêu
Mỗi user có todos riêng, không thể xem/xóa todos của user khác.

### Công nghệ
- **JWT (JSON Web Tokens)** → Xác thực user
- **Bcrypt** → Hash password an toàn
- **HTTPBearer** → Lấy token từ header

### Bảng Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Bảng Todos (cập nhật)
```sql
ALTER TABLE todos ADD COLUMN owner_id INTEGER NOT NULL;
ALTER TABLE todos ADD FOREIGN KEY (owner_id) REFERENCES users(id);
```

### Auth Endpoints
```
POST   /api/v1/auth/register      # Đăng ký user mới
POST   /api/v1/auth/login         # Đăng nhập, lấy JWT token
GET    /api/v1/auth/me            # Lấy info user hiện tại
```

### Todo Endpoints (cập nhật - cần auth)
```
POST   /api/v1/todos              # Tạo (gắn owner = current user)
GET    /api/v1/todos              # Lấy danh sách của current user
GET    /api/v1/todos/{id}         # Lấy chi tiết (kiểm tra owner)
PUT    /api/v1/todos/{id}         # Cập nhật (kiểm tra owner)
PATCH  /api/v1/todos/{id}         # Cập nhật một phần (kiểm tra owner)
POST   /api/v1/todos/{id}/complete# Đánh dấu done (kiểm tra owner)
DELETE /api/v1/todos/{id}         # Xóa (kiểm tra owner)
```

### Test Cấp 5

1. **Cài dependencies:**
```bash
pip install -r requirements.txt
```

2. **Chạy migrations:**
```bash
alembic upgrade head
```

3. **Start server:**
```bash
uvicorn main:app --reload
```

4. **Test workflow (Swagger UI):**
   - POST /api/v1/auth/register → Tạo user A + nhận token
   - Copy token A
   - POST /api/v1/todos → Tạo todo (lưu ID todo A)
   - POST /api/v1/auth/register (user B) → Nhận token B
   - GET /api/v1/todos/{todo_A_id} với token B → ❌ 404 (không thấy)
   - GET /api/v1/todos/{todo_A_id} với token A → ✅ 200 (thấy)

### Tiêu chí đạt
✅ Bảng users với email unique  
✅ Hash password bằng bcrypt  
✅ JWT token generation & validation  
✅ Auth endpoints (register/login/me)  
✅ Todo gắn owner_id  
✅ Owner check (User A không xem todo B)  
✅ HTTPBearer auto extract token  
✅ Alembic migration users table

---
**Status:** ✅ Hoàn thành

## Cấp 6 — Advanced Features (Tags + Due Date + Overdue/Today Endpoints)

### Mục tiêu
Thêm tags (nhãn) cho todos, deadline, và endpoints lọc todos hôm nay/quá hạn.

### Bảng Tags & Many-to-Many
```sql
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE todo_tags (
    todo_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (todo_id, tag_id),
    FOREIGN KEY (todo_id) REFERENCES todos(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);
```

### Bảng Todos (cập nhật)
```sql
ALTER TABLE todos ADD COLUMN due_date DATE;  -- Ngày hạn
```

### Schema Todo (cập nhật)
```json
{
  "id": 1,
  "title": "Học FastAPI",
  "description": "Học Docker + Deployment",
  "is_done": false,
  "due_date": "2026-03-20",
  "tags": [
    {"id": 1, "name": "learning"},
    {"id": 2, "name": "urgent"}
  ],
  "owner_id": 1,
  "created_at": "2026-03-14T10:00:00",
  "updated_at": "2026-03-14T10:00:00"
}
```

### Todo Endpoints (cập nhật)
```
POST   /api/v1/todos              # Tạo todo (có thể gắn tags + due_date)
GET    /api/v1/todos              # Lấy danh sách (filter, sort, pagination)
GET    /api/v1/todos/{id}         # Lấy chi tiết
PUT    /api/v1/todos/{id}         # Cập nhật đầy đủ
PATCH  /api/v1/todos/{id}         # Cập nhật một phần
POST   /api/v1/todos/{id}/complete# Đánh dấu done
DELETE /api/v1/todos/{id}         # Xóa
POST   /api/v1/todos/{id}/restore # **NEW** - Khôi phục (Cấp 8)
DELETE /api/v1/todos/{id}/permanent # **NEW** - Xóa vĩnh viễn (Cấp 8)
```

### Filter Advanced
```bash
# Lọc todos hôm nay
GET /api/v1/todos/today/list

# Lọc todos quá hạn
GET /api/v1/todos/overdue/list

# Filter theo tag
GET /api/v1/todos?tags=learning,urgent

# Filter theo due_date
GET /api/v1/todos?due_date_from=2026-03-15&due_date_to=2026-03-20
```

### Tiêu chí đạt
✅ Bảng tags với many-to-many relationship  
✅ Due date support  
✅ Tags assign/update/delete  
✅ /today/list endpoint  
✅ /overdue/list endpoint  
✅ Alembic migration cho tags + due_date

---
**Status:** ✅ Hoàn thành

## Cấp 7 — Testing + Docker + Documentation

### Mục tiêu
Viết comprehensive tests, containerize app, tạo đầy đủ documentation.

### Testing (Pytest)
```bash
# Cài dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Chạy tất cả tests
pytest tests/ -v

# Với code coverage
pytest tests/ --cov=app --cov-report=html

# Test file structure
tests/
├── conftest.py          # Fixtures (db, client, test_user)
├── test_auth.py         # Auth endpoints tests
└── test_todos.py        # Todo CRUD + advanced tests
```

### Test Coverage
- ✅ Registration (success, duplicate, invalid email)
- ✅ Login (success, wrong password)
- ✅ Todo CRUD (create, read, update, delete)
- ✅ Multi-user isolation
- ✅ Overdue/today filtering
- ✅ Authorization checks
- **25+ test cases**

### Docker Support
```bash
# Build image
docker build -t todolist-api:latest .

# Run container
docker run -p 8000:8000 todolist-api:latest

# Docker Compose
docker-compose up -d
```

### Files
- `Dockerfile` - Multi-stage build, production-ready
- `docker-compose.yml` - Include FastAPI + SQLite volume
- `.dockerignore` - Exclude unnecessary files

### Documentation
- `README.md` **tổng hợp tất cả Cấp 0-8** với:
  - Architecture diagram (clean code layers)
  - Quick start (local + Docker)
  - All 20 endpoints with examples
  - Testing guide
  - Deployment checklist
  - Project structure

### Tiêu chí đạt
✅ Pytest suite với 25+ test cases  
✅ In-memory SQLite for testing  
✅ Test fixtures (db, client, user, token)  
✅ Dockerfile multi-stage  
✅ docker-compose.yml  
✅ Comprehensive README  
✅ Code examples for every endpoint

---
**Status:** ✅ Hoàn thành

## Cấp 8 — Soft Delete + CI/CD Pipeline

### Mục tiêu
Implement soft delete (archive todos instead of removing), GitHub Actions CI/CD automation.

### Soft Delete Feature
```sql
ALTER TABLE todos ADD COLUMN deleted_at DATETIME;
CREATE INDEX idx_deleted_at ON todos(deleted_at);
```

### Soft Delete Behavior
- **Xóa bình thường** → Set `deleted_at = NOW()` (không xóa DB)
- **Khôi phục** → Set `deleted_at = NULL`
- **Xóa vĩnh viễn** → DELETE FROM database
- **GET queries** → Tự động filter `WHERE deleted_at IS NULL`

### New Endpoints
```
POST   /api/v1/todos/{id}/restore     # Khôi phục deleted todo
DELETE /api/v1/todos/{id}/permanent   # Xóa vĩnh viễn (hard delete)
```

### Bảng Todos (final)
```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_done BOOLEAN DEFAULT 0,
    due_date DATE,
    owner_id INTEGER NOT NULL,
    deleted_at DATETIME,  # **NEW - for soft delete**
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);
```

### CI/CD Pipeline (GitHub Actions)
```yaml
# .github/workflows/ci-cd.yml
Jobs:
  1. test       - Run pytest, check coverage, lint (flake8)
  2. security   - Run Bandit security scanner
  3. build      - Build Docker image, test it
```

### Migration Path
```
Migration 001: Create todos table
Migration 002: Add users + owner_id (batch_alter for SQLite)
Migration 003: Add tags table + todo_tags + due_date
Migration 004: Add deleted_at (soft delete column) ← **NEW**
```

### Workflow
1. Push code to GitHub
2. GitHub Actions triggers automatically
3. Tests run → Security check → Build Docker image
4. If all pass → Ready for deployment

### Tiêu chí đạt
✅ Soft delete logic (deleted_at column + index)  
✅ Restore & permanent delete endpoints  
✅ All queries filter soft-deleted items  
✅ Alembic migration 004  
✅ GitHub Actions CI/CD workflow  
✅ Automated testing on every push  
✅ Security scanning (Bandit)  
✅ Docker build validation

---
**Status:** ✅ Hoàn thành

---

## 📊 Project Architecture

### 5-Layer Clean Architecture
```
HTTP Layer (FastAPI Routes)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Data Access)
    ↓
ORM Models (SQLAlchemy)
    ↓
Database (SQLite)
```

### Directory Structure
```
todolist_TK1/
├── app/
│   ├── core/
│   │   ├── config.py          # Environment settings
│   │   ├── database.py        # SQLAlchemy setup
│   │   ├── models.py          # ORM models (User, Todo, Tag)
│   │   ├── security.py        # JWT + password hashing
│   │   └── dependencies.py    # Dependency injection
│   ├── schemas/
│   │   ├── auth.py            # Pydantic models for auth
│   │   └── todo.py            # Pydantic models for todos
│   ├── repositories/
│   │   ├── user.py            # User data access
│   │   ├── todo.py            # Todo data access (soft delete logic)
│   │   └── tag.py             # Tag data access
│   ├── services/
│   │   ├── auth.py            # Auth business logic
│   │   └── todo.py            # Todo business logic
│   └── routers/
│       ├── auth.py            # Auth endpoints
│       └── todos.py           # Todo endpoints
├── migrations/
│   └── versions/
│       ├── 001_create_todos.py
│       ├── 002_add_users.py
│       ├── 003_add_tags.py
│       └── 004_add_soft_delete.py
├── tests/
│   ├── conftest.py            # Test fixtures
│   ├── test_auth.py           # Auth tests
│   └── test_todos.py          # Todo tests
├── main.py                    # FastAPI app entry point
├── requirements.txt           # Dependencies
├── alembic.ini                # Alembic config
├── Dockerfile                 # Docker image
├── docker-compose.yml         # Docker orchestration
├── pytest.ini                 # Pytest config
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions pipeline
└── README.md                  # This file
```

## 🚀 API Summary (20 Endpoints)

### Health Check (2)
- GET / → App status
- GET /health → Server health

### Authentication (3)
- POST /api/v1/auth/register → Create user
- POST /api/v1/auth/login → Get JWT token
- GET /api/v1/auth/me → Current user info

### Todos CRUD (7)
- POST /api/v1/todos → Create
- GET /api/v1/todos → List (filter + sort + pagination)
- GET /api/v1/todos/{id} → Get one
- PUT /api/v1/todos/{id} → Update full
- PATCH /api/v1/todos/{id} → Update partial
- POST /api/v1/todos/{id}/complete → Mark done
- DELETE /api/v1/todos/{id} → Soft delete

### Advanced Todos (6)
- GET /api/v1/todos/today/list → Today's todos
- GET /api/v1/todos/overdue/list → Overdue todos
- POST /api/v1/todos/{id}/restore → Restore deleted (Cấp 8)
- DELETE /api/v1/todos/{id}/permanent → Hard delete (Cấp 8)

**Total: 20 endpoints**

## 📦 Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Framework** | FastAPI | 0.104.1 |
| **Server** | Uvicorn | 0.24.0 |
| **Database** | SQLite | Built-in |
| **ORM** | SQLAlchemy | 2.0.23 |
| **Migrations** | Alembic | 1.12.1 |
| **Authentication** | python-jose JWT | 3.3.0 |
| **Password** | bcrypt/passlib | 4.1.2 / 1.7.4 |
| **Validation** | Pydantic | 2.5.0 |
| **Testing** | pytest | 9.0.2 |
| **Container** | Docker | Latest |
| **Environment** | python-dotenv | 1.2.2 |

## 🎯 Key Features

✅ **Multi-layer Architecture** - Clean code separation  
✅ **Database Migrations** - Alembic for version control  
✅ **JWT Authentication** - Secure token-based auth  
✅ **Multi-user Support** - Data isolation per user  
✅ **Advanced Filtering** - Today, overdue, tags, dates  
✅ **Soft Delete** - Archive instead of destroy  
✅ **Comprehensive Tests** - 25+ pytest cases  
✅ **Docker Ready** - Container & compose files  
✅ **CI/CD Pipeline** - GitHub Actions automation  
✅ **Production-Ready** - Full documentation

## 📍 Quick Start

### Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database
alembic upgrade head

# 3. Run server
uvicorn main:app --reload

# 4. Access API
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### Docker
```bash
docker-compose up -d
# API available at http://localhost:8000
```

### Testing
```bash
pytest tests/ -v --cov=app
```

## 🔐 Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ HTTPBearer scheme
- ✅ Owner-based authorization
- ✅ Bandit security scanning
- ✅ SQL injection prevention (SQLAlchemy)

## 📝 License

Educational project - Free to use and modify

---

**Project Status: ✅ COMPLETE (Cấp 0-8)**  
*Last Updated: March 14, 2026*
