from django.shortcuts import render
import json
import datetime

def numbler(request):

    puzzles = {'2024-07-25': {'Tiles': ['5', '5', '2', '3'], 'Easy': (13, ['5*2+3', '5*3-2', '2*5+3', '3+5*2', '3+2*5', '3*5-2']), 'Medium': (38, ['5+35-2', '5-2+35', '35+5-2', '35-2+5']), 'Hard': (133, ['253-5!'])}, '2024-07-26': {'Tiles': ['1', '4', '2', '3'], 'Easy': (10, ['4+2*3', '4+3*2', '4*3-2', '2*3+4', '3*4-2', '3*2+4']), 'Medium': (66, ['4+2*31', '4+31*2', '2*31+4', '31*2+4']), 'Hard': (648, ['3!^4/2'])}}  # Get today's date to fetch the puzzle of the day
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    print("hello", today, date_str)
    puzzle = puzzles.get(date_str)
    if puzzle == None:
        puzzle = puzzles['2024-07-24']

    num_tiles = puzzle['Tiles']

    # Initialize session variable for difficulty if not set
    if 'difficulty' not in request.session:
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
        
        next_game_message = f"Next puzzle in {hours} hours and {minutes} minutes"

        context = {
            'next_game_message':next_game_message,
            'easy_result': hints_message[0],
            'medium_result': hints_message[1],
            'hard_result': hints_message[2]
        }

        return render (request, 'completed.html', context)
        
    return numbler(request)
