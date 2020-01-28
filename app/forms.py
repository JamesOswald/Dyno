from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class SequenceInputForm(FlaskForm):
    input_sequence = StringField('Sequence')
    integer_input = IntegerField('Integer n')
    submit = SubmitField('Search')