from app import app

from app import app, db
from app.models import Sequence

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Sequence': Sequence}