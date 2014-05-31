from flask import Flask

app = Flask(__name__)
app.secret_key = "very secret key"

import chota.routes
