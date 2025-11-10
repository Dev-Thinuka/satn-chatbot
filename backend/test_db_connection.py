"""
Test database connection for SA Thomson Chatbot backend.
"""

from app.db.session import engine

try:
    print("🔧 Testing PostgreSQL connection...")
    conn = engine.connect()
    print("✅ Database connection successful!")
    conn.close()
except Exception as e:
    print("❌ Database connection failed:")
    print("   ", e)
