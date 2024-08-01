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
        min_tiles, max_tiles = 3,5
        min_answer, max_answer = 0,20
        operators = ops1
    
    if difficulty == "Medium":
        min_tiles, max_tiles = 5,6
        min_answer, max_answer = 0,50
        operators = ops1

    if difficulty == "Hard":
        min_tiles, max_tiles = 5,6
        min_answer, max_answer = 0,1000
        operators = ops1+ops2

    return (min_tiles, max_tiles, min_tiles, min_answer, max_answer, operators)







# Function to evaluate a mathematical expression and return only positive integer values
def evaluate(expr):
    try:
        result = evaluate_bidmas(expr)
        if result:
            if result == int(result) and result >0:
                return int(result)
    except:
        return None

def evaluate_bidmas(expr):

    # reject expressions that don't start with a valid character
    if expr[0] not in "1234567890-":
        return None
    
    # preprocess to handle exponent and factorial notation
    preprocessed_expr = preprocess_expression(expr) 

    # evaluate
    result = eval(preprocessed_expr)
    print (f'{expr} -> {preprocessed_expr} = {result}')
    input (."wait")
    return result

def preprocess_expression(expr):
    # Replace factorial notation with math.factorial function calls

    def factorial_replacer(match):
        number = int(match.group(1))
        if number <10:            
            return math.factorial({number})
        else:
            return None
    
    # Use regex to find all occurrences of n!
    if '!' in expr:
        expr = re.sub(r'(\d+)!', str(factorial_replacer), expr)
        if factorial_replacer == None:
            return None
    
    # replace exponent operator
    if '^' in expr:
        expr = expr.replace('^', '**')

    return expr



# Function to generate all valid sums which can be made using the tiles
def generate_valid_sums(tiles, max_tiles):
    solutions = {}
    
    # Iterate over lengths from 1 to num_tiles
    for length in range (1,max_tiles+1):
        for r in range(1, length+1):
            # Generate all permutations of the given length
            for perm in itertools.permutations(tiles, r):
                expr = ''.join(perm)
                
                # Only evaluate expressions with digits
                if re.search(r'\d', expr):
                    result = evaluate(expr)
                    if result is not None:
                        if result not in solutions:
                            solutions[result]=[expr]
                        else:
                            if expr not in solutions[result]:
                                solutions[result].append(expr)
        
    return solutions


def factorial(n):
    ans = 1
    for i in range(1,n+1):
        ans*=i
    return(ans)


def generate_good_sums(tiles, min_tiles ,max_tiles, min_answer, max_answer):

    # this will return all valid sums
    sums = generate_valid_sums(tiles, min_tiles, max_tiles)
    good_sums = {}

    for (result, expressions) in sums.items():

        for expression in expressions:
            if len(expression)>= min_tiles and len(expression)<= max_tiles:
                if result >= min_answer and result <= max_answer:
                    if result not in good_sums:
                        good_sums[result]=[expression]
                    else:
                        good_sums[result].append(expression)        
            else:
                if result in good_sums:
                    del(good_sums[result])
                break
 
    sorted_sums = sorted(good_sums.items(), key=lambda x: len(x[1]), reverse=True)

    return sorted_sums


def ask_question(difficulty, sum):
    expressions = sum[1]
    result = sum[0]
    print ("Difficulty: ",difficulty)
    display = "_ "*max([len(expressions[i]) for i in range(len(expressions))])+"= "+str(result)
    print(f'{display} ({len(expressions)} valid answers)')
    print(expressions)
    print()


def generate_puzzle():

    # choose number tiles. The first tile must be 1 or 2.
    firsttile = random.choice([1,2])
    othertiles = random.sample(nums,3)
    numtiles = (firsttile+othertiles).sorted()

    # initiate a new puzzle dictionary
    puzzle = {'Tiles':numtiles}

    # get the easy, medium and hard sums
    for level in ["Easy", "Medium", "Hard"]:

        tiles = numtiles+level['operators']
        min_tiles = level['min_tiles']
        max_tiles = level['max_tiles']
        min_answer = level['min_answer']
        max_answer = level['max_answer']

        sums = generate_good_sums(tiles, min_tiles, max_tiles, min_answer, max_answer)

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
        puzzles[date_str]=puzzle

    return puzzles


# main

start_date = datetime.today()
number_of_puzzles = 1
puzzles = generate_puzzles(start_date, number_of_puzzles)

print (puzzles)