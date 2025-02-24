import os
import json
from datetime import datetime, timedelta

RATE_LIMIT_FILE = "storage/rate_limits.json"
CACHE_FILE = "storage/cache.json"
STORAGE_DIR = "storage"

def ensure_storage_exists():
  if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)
  
  if not os.path.exists(RATE_LIMIT_FILE):
    with open(RATE_LIMIT_FILE, "w") as f:
      json.dump({}, f)
  
  if not os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "w") as f:
      json.dump({}, f)

def load_cache():
  ensure_storage_exists()
  if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
      return json.load(f)
  return {}

def save_cache(data):
  ensure_storage_exists()
  with open(CACHE_FILE, "w") as f:
    json.dump(data, f)

def load_rate_limits():
  ensure_storage_exists()
  if os.path.exists(RATE_LIMIT_FILE):
    with open(RATE_LIMIT_FILE, "r") as f:
      return json.load(f)
  return {}

def save_rate_limits(data):
  ensure_storage_exists()
  with open(RATE_LIMIT_FILE, "w") as f:
    json.dump(data, f)

def check_rate_limit(ip_address, limit_key):
  rate_limits = load_rate_limits()
  now = datetime.now()
  if ip_address not in rate_limits:
    return True
  limit_info = rate_limits[ip_address].get(limit_key, {})
  last_request_time = datetime.fromisoformat(limit_info.get("last_request_time", "1970-01-01T00:00:00"))
  request_count = limit_info.get("count", 0)
  time_window = timedelta(minutes=1)
  if now - last_request_time > time_window:
    request_count = 0
  if request_count < 5:
    rate_limits[ip_address][limit_key] = {
      "count": request_count + 1,
      "last_request_time": now.isoformat()
    }
    save_rate_limits(rate_limits)
    return True
  return False
