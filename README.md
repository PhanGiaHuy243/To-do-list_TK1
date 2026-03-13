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
