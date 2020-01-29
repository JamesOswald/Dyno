from app import app
from flask import Flask
from app import db
from app.models import Sequence

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Sequence': Sequence}

app = Flask(__name__)
app.run()

if __name__ =='__main__':
    app.run()