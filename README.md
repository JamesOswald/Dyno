# Installation

 - git clone git@github.com:JamesOswald/dyno.git
 - create a virtualenv: python3 -m venv <name of venv> 
 - pip install -r requirements.txt
 - flask run
 
# Thought Process while initially building
 
  - It has been along time since I have used flask, to do this quickly I will need to use Django
  - Although I have used AWS Lambda and EC2 before, I have not used beanstalk or RDS. 
  - I will have to follow the tutorial, conveniently, they also use Django in the AWS tutorial
 
### Initial Thoughts
   - Build a Django app which looks through all of the genome strings
   - Populate the database with the genome strings in an easy to use table 
   - Build some type of frontend
   
### 10 minutes later
 
 - Okay, the link provided to me by Jeff looks really good. I could just do this, but it could be dangerous as my experience with flask is minimal and I have limited time
 - There is even a link to a github repo that performs CRUD on a database, I could just modify this code with the searching  through the gene function
 - Okay time to follow the tutorial.
 
### 20 minutes later
 - The library the guy uses is out of date, so pip installs are failing, I will update his requirements.txt to the newest versions, hopefully this fixes things and hopefully doesn’t break anything down the road.
 - Okay that didn’t work, the internet says to reinstall python. I don’t think that will fix the issue
 - It seems to be a python3 vs python type of thing (syntax errors in underlying requirements)
 - Instead I will follow his tutorial on the AWS side and create my own project on the code side.

### Progress so far
  - I have setup a rudimentary application following this tutorial in pure flask: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
  - I am now ready to create the database and need to read the FASTA file and place it into my model and into my db.
  - I am not trying to write an interpreter for this functionality and I imagine someone has already done it, so im going to look online.
  - I found a package called Bio, I am going to use this. (https://www.biostars.org/p/710/) and (https://pypi.org/project/bio/)
  
## Parsing data
 - I have setup a rudimentary application following this tutorial in pure flask: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
 - I am now ready to create the database and need to read the FASTA file and place it into my model and into my db. I am not trying to write an interpreter for this functionality and I imagine someone has already done it, so im going to look online.
 - After about 2 minutes, I found a package called Bio, I am going to use this. (https://www.biostars.org/p/710/) and (https://pypi.org/project/bio/)

## Models 
  - After looking at the Bio.Seq.Seq() object, it looks like we can just pull the Sequence string out using the __str__ class method: yay!
   - We will need some extra work however to parse the description into a readable format 
   - Looking at the format of the challenge it actually seems as if I wont need any of the fields in the description. 
   - I will save it to the database all in one string field for the sake of time. 
   - This means our DB model, will just have 3 fields, name, sequence, description

# Thought process for Implementation

 - Querying is simple: https://stackoverflow.com/questions/4926757/sqlalchemy-query-where-a-column-contains-a-substring/4926793 this should be optimized under the hood
 - Now to implement the hamming distance functionality 
 - I want to do my best to keep this to one query
 - This seems similar https://en.wikipedia.org/wiki/Closest_string It mentions bioinformatics. So seems like im on the right path
## After a few minutes
 - We basically need to search through our database for the entire Hamming Space(n=1) of the input string. 
 - This is probably a brute force solution, but I am thinking that:
 - Generate the hamming space for the input string
 - For each of the generated strings, execute the query from above
 - Run these queries in separate threads to minimize query time
 - Im being silly, I can do this by generating regex strings that will cover the n=1 hamming space
 - Now I have to figure out how to make this one query
 
 ## Results
  - Filter function actually performs the search function on a QuerySet object, not as a raw SQL  query, so I can sequentially add the filters, and then call .distinct() to resolve it to the solution set with one query to the db
  - After messing with the syntax a bit, I think I have a working solution. I am a little worried about my query being accurate, checking now
  - The result set looks good using this regex checker https://regex101.com/r/eZ1gT7/2246 and, importantly it doesn’t match the exact match

## More results
  - Most of the work is done now, I am going to work on outputting now
  - I have found a bug, when the search function is run twice, the form I am using to capture the input is no longer defined, should be a quick fix, but worth noting
  - Ok, that was dumb, I wrote input.html in the wrong place, all good. 
  - Looking at the summarized output, it seems weird to me that the single substitution list is smaller than the exact match list a lot of the time, I am going to investigate this
  - Ok the source of the issue is the fact that I subtract from the single substitution set the exact match set, to remove duplicates. 
  - This effect goes away as the search string gets larger, this makes sense: for smaller search strings, the probability that a sequence contains an exact match is very high, so most strings in the 470 items match but as string length this probability decreases and the single substitution probability shrinks much slower than the exact match probability
  
  #Bonus 1
  - Code modifications: Add a field to the form for inputting an integer, If n perform bonus calculation, add an output page for this
  - How to do bonus calculation:
  - example say my database is [AACT, CAATCAC, ACACAC, ACTC] and my input string is ACTCCG, and n = 2 this should return AC since ACTC only occurs in one
  - Brute force: loop over input string, generate all possible substrings, order them according to length, query the database in descending order until the result set is of length n
  - Improvement maybe: https://en.wikipedia.org/wiki/Longest_common_substring_problem 
  - Since I am running low on time, I will implement the brute force approach, this could be sped up with multiprocessing, and definetly sped up with this: https://link.springer.com/article/10.1007/s00453-009-9369-1  
  - I wish I had seen this when I started, I would have implemented the entire question this way: https://en.wikipedia.org/wiki/Suffix_tree
  
 #Bonus 2
  - Did not have time, however, to do this I would refactor my existing code completely, 
  - I would create a new model called SuffixTreeNode and SuffixTree in the database
  - Then we could search throught the tree at a specific n for the most frequently occuring substring
  
