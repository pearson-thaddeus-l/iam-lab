import os
from flask import Flask, redirect, request, session, url_for
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-in-prod")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read"]

def get_msal_app():
    return ConfidentialClientApplication(
        CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY
    )

@app.route("/")
def index():
    user = session.get("user")
    if user:
        return f"""
        <h2>Signed in successfully</h2>
        <p><b>Name:</b> {user.get('name')}</p>
        <p><b>Email:</b> {user.get('preferred_username')}</p>
        <p><b>Tenant:</b> {user.get('tid')}</p>
        <p><b>Object ID:</b> {user.get('oid')}</p>
        <br>
        <a href='/logout'>Sign out</a> | 
        <a href='/token'>View raw ID token claims</a>
        """
    return '<a href="/login">Sign in with Microsoft</a>'

@app.route("/login")
def login():
    auth_url = get_msal_app().get_authorization_request_url(
        SCOPE,
        redirect_uri=REDIRECT_URI
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: no code returned", 400
    result = get_msal_app().acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI
    )
    if "error" in result:
        return f"Auth error: {result.get('error_description')}", 400
    session["user"] = result.get("id_token_claims")
    session["token"] = result.get("id_token")
    return redirect(url_for("index"))

@app.route("/token")
def token():
    claims = session.get("user")
    if not claims:
        return redirect(url_for("index"))
    rows = "".join(f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in claims.items())
    return f"<h2>ID Token Claims</h2><table border=1>{rows}</table><br><a href='/'>Back</a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"{AUTHORITY}/oauth2/v2.0/logout?post_logout_redirect_uri=http://localhost:5000"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
