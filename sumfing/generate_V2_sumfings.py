import random
import itertools
import re
import math
from datetime import datetime, timedelta

# Define the tiles

nums = ['1','2','3','4','5','6','7','8','9']
ops1 = ['+','-','*','/']
ops2= ['^', '!']
ops = ops1+ops2


# Define the levels of difficulty
# This program will generate 3 maths puzzles.
# EASY will have either 3, 4 or 5 tiles and one or two operator
# MEDIUM will have either 5 or 6 tiles and one or two operators
# HARD will have either 5 or 6 tiles and will use an extended set of operators

def settings(difficulty):

    if difficulty == "Easy":
        min_tiles, max_tiles = 5,5
        min_answer, max_answer = 0,20
        operators = ops1
    
    elif difficulty == "Medium":
        min_tiles, max_tiles = 5,6
        min_answer, max_answer = 20,50
        operators = ops1

    elif difficulty == "Hard":
        min_tiles, max_tiles = 5,6
        min_answer, max_answer = 50,10000
        operators = ops1+ops2
    
    else:
        print("difficulty not specified")
        return(None)       

    return (min_tiles, max_tiles, min_answer, max_answer, operators)







# Function to evaluate a mathematical expression and return only positive integer values
def evaluate(expr):
    
    # reject expressions that don't start or end with a valid character
    if expr[0] not in "1234567890-" or expr[-1] not in "1234567890!":
        return None
    
    # preprocess to handle exponent and factorial notation
    preprocessed_expr = preprocess_expression(expr) 

    # evaulate the expression
    try:
        result = eval(preprocessed_expr)
        if result == int(result) and result >= 0:
            return int(result)
    except:
        return None


def preprocess_expression(expr):
    # Replace factorial notation with math.factorial function calls

    def factorial_replacer(match):
        number = int(match.group(1))
        if number <10:
            integer = math.factorial(number)            
            return f'{integer}'
        else:
            return None
    
    # Use regex to find all occurrences of n!
    if '!' in expr:
        for substring in ['!0','!1','!2','!3','!4','!5','!6','!7','!8','!9']:
            if substring in expr:
                return None
        expr = re.sub(r'(\d+)!', factorial_replacer, expr)
        if factorial_replacer == None:
            return None
    
    # replace exponent operator
    if '^' in expr:
        for substring in ['^+', '^/', '^^', '^!', '^*', '-^', '+^', '/^', '*^']:
            if substring in expr:
                return None

        expr = expr.replace('^', '**')

    return expr



# Function to generate all valid sums which can be made using the tiles
def generate_valid_sums(tiles, max_tiles, min_answer, max_answer):
    valid_sums = {}
    
    # Iterate over lengths from 1 to num_tiles
    for length in range (1,max_tiles+1):
        for r in range(1, length+1):
            # Generate all permutations of the given length
            for perm in itertools.permutations(tiles, r):
                expr = ''.join(perm)
                
                # Only evaluate expressions with digits
                if re.search(r'\d', expr):
                    result = evaluate(expr)
                    if result:
                        if result >= min_answer and result <= max_answer: 
                            if result not in valid_sums:
                                valid_sums[result]=[expr]
                            else:
                                if expr not in valid_sums[result]:
                                    valid_sums[result].append(expr)
            
    return valid_sums


def factorial(n):
    ans = 1
    for i in range(1,n+1):
        ans*=i
    return(ans)


def generate_good_sums(level, tiles, min_tiles ,max_tiles, min_answer, max_answer):

    # get all sums with a result in the valid range
    valid_sums = generate_valid_sums(tiles, max_tiles,min_answer, max_answer)
    #print (f'Valid {level} results with up to {max_tiles} tiles: {len(valid_sums)}')
    
    # Select only sums with results which cannot be achieved with fewer tiles. It will be the shortest expressions for each result
      
    shortest_sums = {}
    for (result, expressions) in valid_sums.items():
        expression_lengths = [len(expression) for expression in expressions]
        min_expr_length = min(expression_lengths)
        for expression in expressions:
            if len(expression) == min_expr_length:
                if result not in shortest_sums:
                    shortest_sums[result]=[expression]
                else:
                    shortest_sums[result].append(expression)        
    
    # keep only sums which use minimum number of tiles
    sums_with_minimum_tiles = {}
    for result, expressions in shortest_sums.items():
        if len(expressions[0])>=min_tiles:
            sums_with_minimum_tiles[result]=expressions

    good_sums = sums_with_minimum_tiles.copy()
    for result, expressions in sums_with_minimum_tiles.items():

        operators=['+','-','/','*','^','!']
    
        for expression in expressions:

        # exclude easy sums without 5 tiles and 2 operators (those are medium)
            if level == "Easy":
                if expression[1] not in operators or expression[3] not in operators:
                    del(good_sums[result])
                    break
                
        # no medium sums with 5 tiles and 2 operators (those are easy)
            if level == "Medium":
                if expression[1] in operators and expression[3] in operators:
                    del(good_sums[result])
                    break
            
        # hard sums cannot only include + and -
            if level == "Hard":
                if '*' not in expression and '/' not in expression and '^' not in expression and '!' not in expression:
                    del(good_sums[result])
                    break
        
    #print (f'Good {level} results with between {min_tiles} and {max_tiles} tiles: {len(good_sums)}')
    
    sorted_good_sums = sorted(good_sums.items(), key=lambda x: len(x[1]), reverse=True)
    return sorted_good_sums


def generate_puzzle():

    numtiles = random.sample(nums,4)
    #numtiles[0]=  random.choice(['1','2'])
    numtiles.sort()
    #print (f'Number tiles: {numtiles}')

    # initiate a new puzzle dictionary
    puzzle = {'Tiles':numtiles}

    # get the easy, medium and hard sums
    for level in ["Easy", "Medium", "Hard"]:
    
        (min_tiles, max_tiles, min_answer, max_answer, operators) = settings(level)
        
        tiles = numtiles + operators
        
        sums = generate_good_sums(level, tiles, min_tiles, max_tiles, min_answer, max_answer)
        
        if sums:
            puzzle[level] = random.choice(sums)
        else:
            return None
    
    return puzzle


# Generate a dictionary of puzzles, where the key is the date

def generate_puzzles(start_date, number_of_puzzles):
    puzzles = {}

    for i in range (number_of_puzzles):
        date = start_date + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        puzzle = None
        while not puzzle:
            puzzle = generate_puzzle()
            if puzzle in puzzles.items():
                puzzle = None
        puzzles[date_str]=puzzle

    return puzzles


# main

start_date = datetime.today()
number_of_puzzles = 30
puzzles = generate_puzzles(start_date, number_of_puzzles)

print (puzzles)