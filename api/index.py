from flask import Flask, request, jsonify
from datetime import datetime, timezone
import os
import uuid
import re

app = Flask(__name__)

# ============================================================
# Frexxy × 𝑫𝒓𝒂𝒌𝒐𝑿𝑵𝒂𝒆𝒆𝒎
# ============================================================

APP_NAME = "Frexxy API"
DEVELOPER = "𝑫𝒓𝒂𝒌𝒐𝑿𝑵𝒂𝒆𝒆𝒎"
VERSION = "1.0.0"
MODE = "TEST"

# ============================================================
# API KEY
# ============================================================
# Change this value to your own private key.
# Better: set FREXXY_API_KEY as an environment variable.

ACCESS_KEY = os.getenv(
    "FREXXY_API_KEY",
    "Frexxy-Test-Key"
)


# ============================================================
# Response Helper
# ============================================================

def api_response(success, message, data=None, status=200):
    result = {
        "success": success,
        "service": APP_NAME,
        "developer": DEVELOPER,
        "version": VERSION,
        "mode": MODE,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    if message:
        result["message"] = message

    if data is not None:
        result["data"] = data

    return jsonify(result), status


# ============================================================
# API Key Verification
# ============================================================

def check_api_key():
    key = request.headers.get("X-API-Key", "").strip()

    # Query parameter support
    if not key:
        key = request.args.get("key", "").strip()

    return key == ACCESS_KEY


# ============================================================
# Home
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return api_response(
        True,
        "Frexxy API is live",
        {
            "name": APP_NAME,
            "developer": DEVELOPER,
            "version": VERSION,
            "status": "online",
            "endpoints": {
                "health": "/health",
                "test": "/fetch"
            }
        }
    )


# ============================================================
# Health Check
# ============================================================

@app.route("/health", methods=["GET"])
def health():

    return api_response(
        True,
        "API is healthy",
        {
            "status": "online"
        }
    )


# ============================================================
# TEST FETCH ENDPOINT
# ============================================================

@app.route("/fetch", methods=["GET"])
def fetch():

    # --------------------------------------------------------
    # API KEY
    # --------------------------------------------------------

    if not check_api_key():

        return api_response(
            False,
            "Invalid API key",
            status=401
        )

    # --------------------------------------------------------
    # TEST ID
    # --------------------------------------------------------

    test_id = request.args.get("aadhaar", "").strip()

    if not test_id:

        return api_response(
            False,
            "Missing aadhaar parameter",
            status=400
        )

    if not re.fullmatch(r"[0-9]{12}", test_id):

        return api_response(
            False,
            "Invalid format. Must contain exactly 12 digits.",
            status=400
        )

    # --------------------------------------------------------
    # TEST REQUEST
    # --------------------------------------------------------

    request_id = str(uuid.uuid4())

    # Mask the identifier.
    masked_id = "********" + test_id[-4:]

    return api_response(
        True,
        "Test request processed successfully",
        {
            "request_id": request_id,
            "identifier": masked_id,
            "lookup_performed": False,
            "credits": f"Powered by {DEVELOPER}"
        }
    )


# ============================================================
# 404
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return api_response(
        False,
        "Endpoint not found",
        status=404
    )


# ============================================================
# 405
# ============================================================

@app.errorhandler(405)
def method_not_allowed(error):

    return api_response(
        False,
        "Method not allowed",
        status=405
    )


# ============================================================
# 500
# ============================================================

@app.errorhandler(500)
def server_error(error):

    return api_response(
        False,
        "Internal server error",
        status=500
    )


# ============================================================
# Vercel
# ============================================================

app_handler = app


# ============================================================
# Local Run
# ============================================================

if __name__ == "__main__":

    port = int(os.getenv("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )