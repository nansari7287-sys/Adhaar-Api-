from flask import Flask, request, jsonify
import requests
import hashlib
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import os

app = Flask(name)

--- Configuration ---

SECRET_SEED = "APIMPDS$9712Q"
IV_STR = "AP4123IMPDS@12768F"
API_URL = 'http://impds.nic.in/impdsmobileapi/api/getrationcard'
TOKEN = "91f01a0a96c526d28e4d0c1189e80459"
USER_AGENT = 'Dalvik/2.1.0 (Linux; U; Android 14; 22101320I Build/UKQ1.240624.001)'

✅ আপনার নতুন এক্সেস কী (Access Key)

ACCESS_KEY = "nexxon07"

--- Utility Functions ---

def get_md5_hex(input_string: str) -> str:
return hashlib.md5(input_string.encode('iso-8859-1')).hexdigest()

def generate_session_id() -> str:
return "28" + datetime.now().strftime("%Y%m%d%H%M%S")

def encrypt_payload(plaintext_id: str, session_id: str) -> str:
inner_hash = get_md5_hex(SECRET_SEED)
key_material = get_md5_hex(inner_hash + session_id)
aes_key = hashlib.sha256(key_material.encode('utf-8')).digest()[:16]
iv = IV_STR.encode('utf-8')[:16]

cipher = AES.new(aes_key, AES.MODE_CBC, iv)  
padded_data = pad(plaintext_id.encode('utf-8'), AES.block_size, style='pkcs7')  
ciphertext = cipher.encrypt(padded_data)  
  
return base64.b64encode(base64.b64encode(ciphertext)).decode('utf-8')

--- Routes ---

@app.route('/', methods=['GET'])
def home():
return jsonify({
"status": "Aadhaar to Family API is Live",
"developer": "CREATOR SHYAMCHAND",
"usage": "/fetch?aadhaar=XXXXXXXXXXXX&key=nexxon07"
})

@app.route('/fetch', methods=['GET'])
def fetch():
try:
# ✅ এক্সেস কী চেক
key = request.args.get("key", "").strip()
if key != ACCESS_KEY:
return jsonify({"error": "Invalid API key"}), 401

aadhaar_input = request.args.get("aadhaar", "").strip()  
    if not aadhaar_input or len(aadhaar_input) != 12 or not aadhaar_input.isdigit():  
        return jsonify({"error": "Invalid format. Must be 12 digits."}), 400  

    session_id = generate_session_id()  
    encrypted_id = encrypt_payload(aadhaar_input, session_id)  

    headers = {  
        'User-Agent': USER_AGENT,  
        'Content-Type': 'application/json; charset=utf-8'  
    }  
    payload = {  
        "id": encrypted_id,  
        "idType": "U",  
        "userName": "IMPDS",  
        "token": TOKEN,  
        "sessionId": session_id  
    }  

    response = requests.post(API_URL, headers=headers, json=payload, timeout=15)  
    data = response.json()  
      
    # আপনার কাস্টম ক্রেডিট  
    if isinstance(data, dict):  
        data["credits"] = "Developed by CREATOR 𝑫𝒓𝒂𝒌𝒐𝑿𝑵𝒂𝒆𝒆𝒎 | @frexxxy"  
          
    return jsonify(data)  

except Exception as e:  
    return jsonify({"error": str(e)}), 500

Vercel handler

app_handler = app