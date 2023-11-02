import json
from flask import Flask
app = Flask(__name__)

@app.route('/')
async def index():
    return json.dumps({'name': 'alice',
                       'email': 'alice@outlook.com'})

if __name__ == "__main__":
    app.run(debug=True)