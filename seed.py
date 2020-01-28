from Bio import SeqIO
from config import Config
from app.models import Sequence
import re
from app.__init__ import db
import sqlalchemy
from app.routes import bonus_one
from suffix_tree import SuffixTree

engine = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)  # connect to server
create_str = "CREATE DATABASE IF NOT EXISTS %s ;" % (Config.SQLALCHEMY_DATABASE_NAME)
engine.execute(create_str)
engine.execute("USE {}".format(Config.SQLALCHEMY_DATABASE_NAME))
db.create_all()
db.session.commit()

with open(Config.SEED_DATA_LOCATION, 'rU') as handle: 
    for record in SeqIO.parse(handle, 'fasta'):
        suffix_tree = SuffixTree(str(record.seq))
        sequence = Sequence(
            name=record.name.split('|')[1], 
            description= record.description, 
            sequence = str(record.seq)) 
        db.session.add(sequence)
db.session.commit()
db.session.close()
