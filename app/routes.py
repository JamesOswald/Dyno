from app import app
from flask import render_template
from app.forms import SequenceInputForm
from app.models import Sequence
from flask import flash
from sqlalchemy import or_, not_, and_
from app import db

exact_matches = []
alphabet = set(['A', 'C', 'G', 'T'])
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SequenceInputForm()
    # find all exact matches, if necessary for speed this could be run in parallel with the single sub queries
    if form.integer_input.data == None: 
        # main question
        exact_matches = set(Sequence.query.filter(Sequence.sequence.contains(form.input_sequence.data)).all())
        single_sub_matches = set(single_sub_query(form.input_sequence.data, exact_matches))
        single_sub_matches -=  exact_matches
        return render_template('output.html', exact_matches=exact_matches, single_sub_matches=single_sub_matches)

    elif form.integer_input.data and form.input_sequence.data:
        #Bonus 1
        sub_string, num_matches = bonus_one(form.integer_input.data, form.input_sequence.data)
        if num_matches and sub_string: 
            return render_template('bonus_one_output.html',sub_string=sub_string, num_needed=form.integer_input.data, num_matches=num_matches)
        else:
            return render_template('none_found.html')
    return render_template('input.html', form=form)

def single_sub_query(input_string, exact_matches):
    """
    creates regex string representing the hamming space at a hamming distance of 1 
    and then queries the database for all matching sequences
    """
    query_strings = []
    query = db.session.query(Sequence)

    for index, char in enumerate(input_string): 
        # filter out the character that is actually in this location
        # as all matching strings that match that case will already be accounted for in exact matches
        characters = [letter for letter in alphabet if letter != char]
        # create a regex string which matches all 3 other possiblities of letters being in this location 
        regex_string = ".*{}[{}]{}.*".format(input_string[:index], "".join(characters), input_string[index + 1:])
        # filter the query set to contain the subset of values
        query.filter(Sequence.sequence.op('regexp')(regex_string))

    # at this point, we want to minimize the number of trips to the database (i.e. lets try and do this in one query)
    # unpacks the query strings and executes the query, making sure there is only one copy of an item in the result set
    return query.distinct()

def bonus_one(n, input_string):
    # find all substrings and sort them in order of length
    all_substrings = sorted([input_string[i: j] for i in range(len(input_string)) 
    for j in range(i + 1, len(input_string) + 1)], key=len, reverse=True)
    #query the database for all the substrings
    for sub_string in all_substrings:
        exact_match_count = Sequence.query.filter(Sequence.sequence.contains(sub_string)).count()
        if exact_match_count >= n: 
            return sub_string, exact_match_count
    return None

def bonus_two(n):
    # need to refactor code to use and store a suffix tree then traverse the tree to find nodes at the given 
    raise NotImplementedError