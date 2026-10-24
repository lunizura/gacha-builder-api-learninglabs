import os
from dotenv import load_dotenv

# Muat environment variable dari .env
load_dotenv()

from api.index import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
    print(f"[*] Starting Gacha Builder REST API on http://127.0.0.1:{port} (debug={debug})")
    print(f"[*] Web UI Explorer: http://127.0.0.1:{port}/ui")
    print(f"[*] Endpoint Health: http://127.0.0.1:{port}/api/health")
    print(f"[*] Endpoint Characters: http://127.0.0.1:{port}/api/characters")
    app.run(host="0.0.0.0", port=port, debug=debug)
