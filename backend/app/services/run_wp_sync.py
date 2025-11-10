# backend/app/services/run_wp_sync.py
from app.services.etl_wordpress import run_full_sync

if __name__ == "__main__":
    run_full_sync()

