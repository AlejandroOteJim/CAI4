from flask import Flask, request
import sys

app = Flask(__name__)

PAGINA = """<html><body>
<h2>Login Hospital</h2>
<form method="POST" action="/login">
  Usuario: <input name="usuario"><br>
  Password: <input name="password" type="password"><br>
  <input type="submit" value="Entrar">
</form>
</body></html>"""

@app.route("/")
def index():
    return PAGINA

@app.route("/login", methods=["POST"])
def login():
    return f"<html><body>Bienvenido {request.form.get('usuario')}</body></html>"

if __name__ == "__main__":
    puerto = int(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2] == "ssl":
        app.run(host="0.0.0.0", port=puerto, ssl_context=("cert.pem", "key.pem"))
    else:
        app.run(host="0.0.0.0", port=puerto)