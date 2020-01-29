from Bio import SeqIO
from config import Config
from app.models import Sequence
import re
from app.__init__ import db
import sqlalchemy
from app.routes import bonus_one

with open(Config.SEED_DATA_LOCATION, 'rU') as handle: 
    for record in SeqIO.parse(handle, 'fasta'):
        sequence = Sequence(
            name=record.name.split('|')[1], 
            description= record.description, 
            sequence = str(record.seq)) 
        db.session.add(sequence)
db.session.commit()
db.session.close()
