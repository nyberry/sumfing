import random
import itertools
import re
from datetime import datetime, timedelta

# Define the tiles
nums = ['1','1','2','2','2','3','3','4','4','5','5','6','7','8','9']
ops1 = ['+','-','*','/']
ops2= ['^', '!']
ops = ops1+ops2

# Function to evaluate a mathematical expression safely
def safe_eval(expr):
    try:
        # Evaluate the expression and ensure it's an integer
        result = evaluate_left_to_right(expr)
        if result:
            if result == int(result) and result >0:
                return int(result)
    except:
        return None
    


def evaluate_left_to_right(expr):

    # reject expressions that don't start with a valid character
    if expr[0] not in "1234567890-":
        return None
 
    # Tokenize the expression
    expr = "0"+expr
    tokens = re.findall(r'\d+|[+\-/^*!]', expr)
    #print(tokens)
    
    if not tokens:
        return None

    # Convert the first token to a number
    result = float(tokens.pop(0))

    while tokens:
        # Get the operator and the next number
        operator = tokens.pop(0)

        if operator == '!':
            if result<0:
                return None
            if result != int(result):
                return None
            if result >=10:
                return None
            else:
                result = factorial(int(result))

        else:
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

    return result

# Function to generate all valid sums
def generate_valid_sums(tiles, num_tiles):
    solutions = {}
    
    # Iterate over lengths from 1 to num_tiles
    for length in range (1,num_tiles+1):
        for r in range(1, length+1):
            # Generate all permutations of the given length
            for perm in itertools.permutations(tiles, r):
                expr = ''.join(perm)
                
                # Only evaluate expressions digits
                if re.search(r'\d', expr):
                    result = safe_eval(expr)
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


def generate_good_sums(tiles, minlength , maxlength, order, maxval):

    sums = generate_valid_sums(tiles, maxlength)
    good_sums = {}

    for (result, expressions) in sums.items():

        for expression in expressions:
            if len(expression)>= minlength and len(expression)<= maxlength:

                if result <= maxval:

                    reject = False

                    if order:
                        for i in range(len(expression)):
                            if (order[i] == "D" and expression[i] in nums) or (order[i] == "O" and expression[i] in ops):
                                pass
                            else:
                                reject = True
                                

                    if reject == False:
                        if result not in good_sums:
                            good_sums[result]=[expression]
                        else:
                            good_sums[result].append(expression)

                    if reject == True:
                        if result in good_sums:
                            del(good_sums[result])
                        break
        
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

    numtiles = random.sample(nums,4)
    tiles = numtiles+ops1

    # easy

    sums = generate_good_sums(
        numtiles+ops1,
        minlength = 5,
        maxlength = 5,
        order = "DODOD",
        maxval = 100)
    if sums:
        easy_sum = random.choice(sums[-10:])

    sums = generate_good_sums(
        numtiles+ops1,
        minlength = 6,
        maxlength = 6,
        order = None,
        maxval = 120)
    if sums:
        medium_sum = random.choice(sums[-10:])

    sums = generate_good_sums(
        numtiles+ops1+ops2,
        minlength = 5,
        maxlength = 6,
        order = None,
        maxval = 1000)
    if sums:
        hard_sum = random.choice(sums[-10:])

    try:
        return {'Tiles':numtiles, 'Easy':easy_sum, 'Medium': medium_sum, 'Hard':hard_sum}
    except:
        return None

puzzles = {}
start_date = datetime.today()

for i in range (10):
    date = start_date + timedelta(days=i)
    date_str = date.strftime("%Y-%m-%d")
    puzzle = None
    while not puzzle:
        puzzle = generate_puzzle()
    puzzles[date_str]=puzzle

print (puzzles)