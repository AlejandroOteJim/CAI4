from flask import Flask, request, redirect
import os, sys

app = Flask(__name__)

HSTS = os.environ.get("HSTS", "0") == "1"
REDIRIGIR = os.environ.get("REDIRIGIR", "0") == "1"

PAGINA = """<html><body>
<h2>Login Hospital</h2>
<form method="POST" action="/login">
  Usuario: <input name="usuario"><br>
  Password: <input name="password" type="password"><br>
  <input type="submit" value="Entrar">
</form>
</body></html>"""

@app.before_request
def forzar_https():
    if REDIRIGIR and not request.is_secure:
        return redirect(request.url.replace("http://", "https://", 1), code=301)

@app.after_request
def cabecera_hsts(resp):
    if HSTS and request.is_secure:
        resp.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return resp

@app.route("/")
def index():
    return PAGINA

@app.route("/login", methods=["POST"])
def login():
    return f"<html><body>Bienvenido {request.form.get('usuario')}</body></html>"

if __name__ == "__main__":
    puerto = int(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2] == "ssl":
        app.run(host="0.0.0.0", port=puerto, ssl_context=("server.crt", "server.key"))
    else:
        app.run(host="0.0.0.0", port=puerto)
