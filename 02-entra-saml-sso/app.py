import os
from flask import Flask, request, redirect, session, url_for
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "saml-lab-secret-change-me")

def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=os.path.join(os.path.dirname(__file__), 'saml'))
    return auth

def prepare_flask_request(request):
    return {
        'https': 'on',
        'http_host': request.host,
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy()
    }

@app.route("/")
def index():
    user = session.get("user")
    if user:
        rows = "".join(f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in user.get("attributes", {}).items())
        return f"""
        <h2>SAML Sign-in Successful</h2>
        <p><b>NameID:</b> {user.get('nameid')}</p>
        <h3>Attributes</h3>
        <table border=1>{rows}</table>
        <br><a href='/logout'>Sign out</a>
        """
    return '<a href="/login">Sign in with Microsoft (SAML)</a>'

@app.route("/login")
def login():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    return redirect(auth.login())

@app.route("/saml/acs", methods=["POST"])
def saml_acs():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    auth.process_response()
    with open('/tmp/saml_response.xml', 'w') as f:
      f.write(str(auth.get_last_response_xml()))
    errors = auth.get_errors()
    if errors:
        reason = auth.get_last_error_reason()
        xml = auth.get_last_response_xml()
        return f"<pre>Errors: {errors}\nReason: {reason}\nXML: {xml}</pre>", 400
    if not auth.is_authenticated():
        return "Not authenticated", 401
    session["user"] = {
        "nameid": auth.get_nameid(),
        "attributes": auth.get_attributes()
    }
    return redirect(url_for("index"))

@app.route("/saml/metadata")
def metadata():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)
    if errors:
        return f"Metadata errors: {', '.join(errors)}", 400
    return metadata, 200, {'Content-Type': 'text/xml'}

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
