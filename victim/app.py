from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Fake sensitive data
USER_DATA = {
    "username": "admin",
    "email": "admin@lab.com",
    "flag": "FLAG{CORS_MISCONFIG_123}"
}

# 🔴 LAB 1: Wildcard CORS
@app.route("/api/userinfo")
def userinfo():
    res = make_response(jsonify(USER_DATA))
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res

# 🔴 LAB 2: Credentials Misconfig
@app.route("/api/secure-data")
def secure_data():
    res = make_response(jsonify({"secret": "FLAG{CREDENTIALS_LEAK}"}))
    res.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
    res.headers["Access-Control-Allow-Credentials"] = "true"
    return res

# 🔴 LAB 3: Origin Reflection
@app.route("/api/reflection")
def reflection():
    res = make_response(jsonify({"flag": "FLAG{REFLECTED_ORIGIN}"}))
    res.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
    return res

# 🔴 LAB 4: Broken Validation
@app.route("/api/broken")
def broken():
    origin = request.headers.get("Origin", "")
    
    if "trusted.com" in origin:  # BAD CHECK
        res = make_response(jsonify({"flag": "FLAG{BYPASS_ORIGIN}"}))
        res.headers["Access-Control-Allow-Origin"] = origin
        return res
    
    return "Forbidden", 403

# 🔴 LAB 5: Preflight Misconfig
@app.route("/api/admin", methods=["OPTIONS", "POST"])
def admin():
    if request.method == "OPTIONS":
        res = make_response()
        res.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
        res.headers["Access-Control-Allow-Methods"] = "*"
        res.headers["Access-Control-Allow-Headers"] = "*"
        return res

    return jsonify({"flag": "FLAG{PREFLIGHT_BYPASS}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)