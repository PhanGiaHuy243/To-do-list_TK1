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
