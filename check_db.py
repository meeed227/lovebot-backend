import sqlite3

conn = sqlite3.connect('love_messages.db')
c = conn.cursor()

# นับจำนวนข้อความ
c.execute('SELECT COUNT(*) FROM love_messages')
count = c.fetchone()[0]
print(f'ในฐานข้อมูลมีทั้งหมด {count} ข้อความ')

# ดึง 5 ข้อความตัวอย่างมาโชว์
c.execute('SELECT content FROM love_messages LIMIT 5')
rows = c.fetchall()

print('\nตัวอย่างข้อความ:')
for row in rows:
    print(f'- {row[0]}')

conn.close()
