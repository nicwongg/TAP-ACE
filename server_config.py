import os
from routes import *

app.debug = True
host = os.environ.get("IP", '0.0.0.0')
port = int(os.environ.get('PORT', 5000))
app.run(host=host, port=port)