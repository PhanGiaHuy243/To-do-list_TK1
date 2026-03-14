import sqlite3

conn = sqlite3.connect('todolist.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print(f'✅ Tables: {tables}')

# Get todos columns
cursor.execute('PRAGMA table_info(todos)')
cols = cursor.fetchall()
print('\n✅ Todos table columns:')
for col in cols:
    print(f'   - {col[1]} ({col[2]})')

print(f'\n✅ Total: {len(cols)} columns')
print('✅ deleted_at column exists!' if any(c[1] == 'deleted_at' for c in cols) else '❌ deleted_at missing')

conn.close()
