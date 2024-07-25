from django.shortcuts import render
import json
import datetime

def numbler(request):
    puzzles = {'2024-07-25': {'Tiles': ['1', '2', '4', '1'], 'Easy': (10, ['1+4*2', '4+1*2']), 'Medium': (46, ['11*4+2', '4*11+2']), 'Hard': (512, ['2^11/4'])}, '2024-07-26': {'Tiles': ['1', '4', '5', '7'], 'Easy': (10, ['4+7-1', '4-1+7', '7+4-1', '7-1+4']), 'Medium': (81, ['17*5-4', '5*17-4']), 'Hard': (335, ['71-4*5'])}, '2024-07-27': {'Tiles': ['6', '2', '2', '1'], 'Easy': (11, ['6*2-1', '2*6-1']), 'Medium': (33, ['6*2+21', '2*6+21']), 'Hard': (85, ['2^6+21'])}, '2024-07-28': {'Tiles': ['9', '2', '6', '3'], 'Easy': (20, ['6*3+2', '3*6+2']), 'Medium': (58, ['29*6/3', '29/3*6', '6*29/3', '6/3*29']), 'Hard': (621, ['3^2*69'])}, '2024-07-29': {'Tiles': ['5', '8', '6', '5'], 'Easy': (9, ['5/5+8', '8+6-5', '8-5+6', '6+8-5', '6-5+8']), 'Medium': (12, ['56/8+5']), 'Hard': (143, ['6!-5/5'])}, '2024-07-30': {'Tiles': ['3', '4', '1', '2'], 'Easy': (10, ['3*4-2', '3*2+4', '4+1*2', '4*3-2', '1+4*2', '2*3+4']), 'Medium': (59, ['3*21-4', '21*3-4']), 'Hard': (328, ['2^3*41'])}, '2024-07-31': {'Tiles': ['4', '3', '5', '3'], 'Easy': (11, ['3*5-4', '5*3-4']), 'Medium': (52, ['3+53-4', '3-4+53', '53+3-4', '53-4+3']), 'Hard': (477, ['5!*4-3'])}, '2024-08-01': {'Tiles': ['2', '5', '4', '3'], 'Easy': (16, ['5+3*2', '3+5*2']), 'Medium': (73, ['2*34+5', '34*2+5']), 'Hard': (285, ['3^5+42'])}, '2024-08-02': {'Tiles': ['5', '7', '6', '1'], 'Easy': (3, ['7+1-5', '7-5+1', '1+7-5', '1-5+7']), 'Medium': (83, ['6*15-7', '15*6-7']), 'Hard': (145, ['6!/5+1'])}, '2024-08-03': {'Tiles': ['1', '5', '2', '4'], 'Easy': (18, ['5+4*2', '5*4-2', '4+5*2', '4*5-2']), 'Medium': (79, ['21*4-5', '4*21-5']), 'Hard': (575, ['4!^2-1'])}}
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    print("hello", today, date_str)
    puzzle = puzzles.get(date_str)
    if puzzle == None:
        puzzle = puzzles['2024-07-24']

    num_tiles = puzzle['Tiles']

    # Initialize session variable for difficulty if not set, or if completed
    if 'difficulty' not in request.session:
        request.session['difficulty'] = 'Easy'

    if request.session['difficulty'] == "Completed":
        request.session['difficulty'] = 'Easy'



    
    difficulty = request.session['difficulty']
    result = puzzle[difficulty][0]
    expressions = puzzle[difficulty][1]
    boxes = [tile for tile in expressions[0]]

    context = {
        'difficulty': difficulty,
        'num_tiles': num_tiles,
        'boxes': boxes,
        'result': result,
        'expressions': json.dumps(expressions)
    }

    return render(request, 'numbler.html', context)

def next_puzzle(request):

    if 'hints' not in request.session:
        request.session['hints'] = ['-1','-1','-1']

    if 'difficulty' not in request.session:
        request.session['difficulty'] = "unknown"
    
    current_difficulty = request.session['difficulty']

    # update the results
    if request.method == 'POST':
        hint_level = request.POST.get('hint_level')
        
        if current_difficulty == 'Easy':
            request.session['hints'][0]= hint_level
        elif current_difficulty == 'Medium':
            request.session['hints'][1]= hint_level
        elif current_difficulty == 'Hard':
            request.session['hints'][2]= hint_level


    # Update the difficulty level for the next puzzle
    if current_difficulty == 'Easy':
        request.session['difficulty'] = 'Medium'
    elif current_difficulty == 'Medium':
        request.session['difficulty'] = 'Hard'
    elif current_difficulty == 'Hard':
        request.session['difficulty'] = 'Completed'


    # If the puzzle completed
    if request.session['difficulty'] == 'Completed':
        
        # Get the current date and time
        now = datetime.datetime.now()

        # Get the start of tomorrow
        tomorrow = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        # Calculate the time difference
        time_difference = tomorrow - now

        # Convert the difference to hours and minutes
        total_seconds = time_difference.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        hints_given = request.session['hints']
        print (f'Hints given: {hints_given}')
        hints_message = []
        for i in range(len(hints_given)):
            if hints_given[i]=='-1':
                result = " "
            elif hints_given[i]=='0':
                result = "✔"
            elif hints_given[i]=='3':
                result = "✘"
            else:
                result = f'✔ ({hints_given[i]} hints)'
            hints_message.append(result)    
        
        result_message = f'NumGoose #1\n\nEasy: {hints_message[0]}\nMedium: {hints_message[2]}\nHard: {hints_message[2]}\n'
            
        next_game_message = f"Next puzzle in {hours} hours and {minutes} minutes"


        context = {
            'result_message':result_message,
            'next_game_message':next_game_message,
        }

        return render (request, 'completed.html', context)
        
    return numbler(request)
