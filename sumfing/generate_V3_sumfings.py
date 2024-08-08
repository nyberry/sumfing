import random
import itertools
import re
import math
from datetime import datetime, timedelta

# This program will generate daily maths puzzles, for a specified number of days.
# Each day's will have an easy puzzle, a medium puzzle and a hard puzzle.
# 4 number tiles are selected at random. The day's puzzles need to be solved using those tiles.

# Define the tiles

nums = ['1','2','3','4','5','6','7','8','9']
ops = ['+','-','*','/']
extra_ops = ['^', '!']

times_tables_numbers = set([i*j for i in range (1,13) for j in range(1,13)])
print (times_tables_numbers)

def settings(difficulty):

    # Function to define the levels of difficulty
    # EASY will have 5 tiles and two operators. This means all the number terms will have just 1 digit.
    # MEDIUM will have either 5 or 6 tiles and one or two operators. This allows larger numbers to be formed with 2 or 3 digits.
    # HARD will have 6 tiles and the answer will be a larger number than at the easy and medium levels.

    if difficulty == "Easy":
        min_tiles, max_tiles = 5,5
        min_answer, max_answer = 0,20
        operators = ops
    
    elif difficulty == "Medium":
        min_tiles, max_tiles = 5,6
        min_answer, max_answer = 20,50
        operators = ops

    elif difficulty == "Hard":
        min_tiles, max_tiles = 6,6
        min_answer, max_answer = 50,200
        operators = ops # optionally, append extra_ops
    
    else:
        print("difficulty not specified")
        return(None)       

    return (min_tiles, max_tiles, min_answer, max_answer, operators)


def format_for_factorials(expr):

    # Function to replace factorial notation with math.factorial function calls

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
    return expr


def format_for_indices(expr):
    
    # function replace exponent operator '^' with '**' and exclude invalid compound operations

    if '^' in expr:
        for substring in ['^+', '^/', '^^', '^!', '^*', '-^', '+^', '/^', '*^']:
            if substring in expr:
                return None

        expr = expr.replace('^', '**')

    return expr


def evaluate_L2R(expr):

    # function to evaluate an expression from left to right
    try:

        # Tokenize the expression
        tokens = re.findall(r'\d+|[+\-/^*]', expr)
    
        # Convert the last token to a number
        result = float(tokens.pop(0))

        while tokens:
            # Get the operator before it
            operator = tokens.pop(0)
            # Get the token before it. Return None if it's not a number (invalid expression)
            next_number = float(tokens.pop(0))
        
            # Evaluate the expression from left to right
            if operator == '+':
                result += next_number
            elif operator == '-':
                result -= next_number
            elif operator == '*':
                result *= next_number
            elif operator == '/':
                result /= next_number
            elif operator == "^":
                result = result**next_number
    except:
        return None

    return result


def check_for_fraction_step(expr):

    # functon to check if the first two terms evaluate to a fraction: we don't want that, it's messy.

    try:

        # Tokenize the expression
        expr = "0"+expr
        tokens = re.findall(r'\d+|[+\-/^*]', expr)

        operator1 = tokens[1]
        if operator1 == '/':
            term1 = tokens[0]
            term2 = tokens[2]
            if term1 / term2 != int (term1 / term2):
                return True    
        
        return False

    except:

        return False
    

def check_if_sum_is_times_tables_friendly(expr):

    try:

        # Tokenize the expression
        expr = "0"+expr
        tokens = re.findall(r'\d+|[+\-/^*]', expr)

        # Convert the last token to a number
        result = float(tokens.pop(0))

        while tokens:
            # Get the operator before it
            operator = tokens.pop(0)
            # Get the token before it. Return None if it's not a number (invalid expression)
        
            next_number = float(tokens.pop(0))
    
            # Evaluate the expression from left to right
            if result not in times_tables_numbers or next_number not in times_tables_numbers:
                    return None
            if operator == '+':
                result += next_number
            elif operator == '-':
                result -= next_number
            elif operator == '*':
                result *= next_number
            elif operator == '/':
                result /= next_number
            elif operator == "^":
                result = result**next_number
    except:
        return None

    return result


def generate_valid_sums(tiles, max_tiles, min_answer, max_answer):

    
    # Function to generate all valid sums which can be made using the tiles

    bidmas_sums = {}
    L2R_sums = {}
    
    # Iterate over lengths from 1 to num_tiles
    for length in range (1,max_tiles+1):

        for r in range(1, length+1):
            # Generate all permutations of the given length

            for perm in itertools.permutations(tiles, r):
                expr = ''.join(perm)
                
                # Only evaluate expressions with digits and valid first and last characters
                if re.search(r'\d', expr) and expr[0] in "1234567890-" and expr[-1] in "1234567890!":

                    #pre-format for ! 
                    expr_formatted_for_factorials = format_for_factorials(expr)
                    if expr_formatted_for_factorials:

                        # evaluate BIDMAS
                        expr_formatted_for_factorials_and_indices = format_for_indices(expr_formatted_for_factorials)
                        try:
                            result = eval(expr_formatted_for_factorials_and_indices)
                        except:
                            result = None
                        
                        if result:
                            if result >= min_answer and result <= max_answer and result == int(result):

                                # OK, now we have a valid sum. Add it to the dictionary 
                                result = int(result)
                                if result not in bidmas_sums:
                                    bidmas_sums[result]=[expr]
                                else:
                                    if expr not in bidmas_sums[result]:
                                        bidmas_sums[result].append(expr)
                        
                        # evaluate L2R
                        try:
                            L2R_result = evaluate_L2R(expr_formatted_for_factorials)
                        except:
                            result = None
                        
                        if L2R_result:
                            if  L2R_result >= min_answer and L2R_result <= max_answer and L2R_result == int(L2R_result):

                                # We have a sum which can be made L to R. Add it to the dictionary 
                                L2R_result = int(L2R_result)
                                if L2R_result not in L2R_sums:
                                    L2R_sums[L2R_result]=[expr]
                                else:
                                    if expr not in L2R_sums[L2R_result]:
                                        L2R_sums[L2R_result].append(expr)

    # Lets only keep result keys that evaluate both by Bidmas and L2R
    selected_sums = {}
    for result,expr in bidmas_sums.items():
        if result in L2R_sums:
                           
            # add the matching epxressions only to valid sums dictionary
            common_exprs = list(set(expr) & set(L2R_sums[result]))

            if common_exprs:
                selected_sums[result]=common_exprs

    # Check for the case that the default answer results in a fraction after the first operation. We don't want that. Messy.
    for result,expr in selected_sums.items():
        solution = expr[0]
        if check_for_fraction_step(solution):
            selected_sums[result][0].remove()
            selected_sums[result].append(solution)

    return selected_sums


def generate_good_sums(level, tiles, min_tiles ,max_tiles, min_answer, max_answer):

    # Function to generate a dictionary of answer:[expressions] we can use for a given level of difficulty and a given set of tiles

    # get all sums with a result in the valid range
    valid_sums = generate_valid_sums(tiles, max_tiles,min_answer, max_answer)
   
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

        # From 'easy sums', exclude those without 5 tiles and 2 operators (those are medium)
            if level == "Easy":
                if expression[1] not in operators or expression[3] not in operators:
                    del(good_sums[result])
                    break
                
        # no medium sums with 5 tiles and 2 operators (those are easy)
            if level == "Medium":
                if expression[1] in operators and expression[3] in operators:
                    del(good_sums[result])
                    break

                if not check_if_sum_is_times_tables_friendly(expression):
                    del(good_sums[result])
                    break
            
        # hard sums cannot only include + and -
            if level == "Hard":
                if '*' not in expression and '/' not in expression and '^' not in expression and '!' not in expression:
                    del(good_sums[result])
                    break
    
    sorted_good_sums = sorted(good_sums.items(), key=lambda x: len(x[1]), reverse=True)
    return sorted_good_sums


def generate_puzzle():

    # function to generate a single day's puzzle

    numtiles = random.sample(nums,4)
    numtiles.sort()

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



def generate_puzzles(start_date, number_of_puzzles):

    # Function to generate a dictionary of puzzles, where the key is the date

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

print(puzzles)
