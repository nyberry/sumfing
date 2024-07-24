from django.shortcuts import render
import json
import datetime

def numbler(request):

    puzzles = {'2024-07-23': {'Tiles': ['4', '9', '4', '1'], 'Easy': (17, ['4*4+1']), 'Medium': (97, ['4+94-1', '4-1+94', '94+4-1', '94-1+4']), 'Hard': (121, ['9-4!+1'])}, '2024-07-24': {'Tiles': ['2', '5', '4', '2'], 'Easy': (14, ['2+5*2', '2*5+4', '5+2*2', '5*2+4']), 'Medium': (68, ['22-5*4']), 'Hard': (288, ['4!^2/2'])}, '2024-07-25': {'Tiles': ['2', '2', '3', '5'], 'Easy': (11, ['2*3+5', '3*2+5']), 'Medium': (101, ['2*52-3', '52*2-3']), 'Hard': (242, ['5!*2+2'])}, '2024-07-26': {'Tiles': ['8', '2', '3', '5'], 'Easy': (20, ['8*5/2', '8/2*5', '5*8/2', '5/2*8']), 'Medium': (97, ['3*5+82', '5*3+82']), 'Hard': (963, ['5!*8+3'])}, '2024-07-27': {'Tiles': ['2', '5', '1', '4'], 'Easy': (18, ['5+4*2', '5*4-2', '4+5*2', '4*5-2']), 'Medium': (94, ['51-4*2']), 'Hard': (529, ['4!-1^2'])}, '2024-07-28': {'Tiles': ['9', '2', '2', '6'], 'Easy': (42, ['9-2*6']), 'Medium': (41, ['2*6+29', '6*2+29']), 'Hard': (82, ['6!/9+2'])}, '2024-07-29': {'Tiles': ['2', '2', '8', '1'], 'Easy': (17, ['2*8+1', '8*2+1']), 'Medium': (120, ['2+8*12', '8+2*12']), 'Hard': (52, ['8^2-12'])}, '2024-07-30': {'Tiles': ['8', '2', '2', '5'], 'Easy': (9, ['8/2+5', '2*2+5', '2/2+8']), 'Medium': (88, ['52-8*2']), 'Hard': (944, ['5!-2*8'])}, '2024-07-31': {'Tiles': ['8', '3', '5', '6'], 'Easy': (46, ['8*5+6', '5*8+6']), 'Medium': (60, ['3+65-8', '3-8+65', '5+63-8', '5-8+63', '63+5-8', '63-8+5', '65+3-8', '65-8+3', '6/3+58']), 'Hard': (147, ['6!/5+3'])}, '2024-08-01': {'Tiles': ['6', '3', '9', '5'], 'Easy': (84, ['9+5*6', '5+9*6']), 'Medium': (97, ['6/3+95']), 'Hard': (333, ['5!-9*3'])}}
    # Get today's date to fetch the puzzle of the day
    today = datetime.date.today().strftime('%Y-%m-%d')
    puzzle = puzzles.get(today, puzzles['2024-07-23'])  # Fallback to a default puzzle if today's puzzle is not found

    num_tiles = puzzle['Tiles']

    # Initialize session variable for difficulty if not set
    if 'difficulty' not in request.session:
        request.session['difficulty'] = 'Easy'
    
    difficulty = request.session['difficulty']
    boxes = [0, 1, 2, 3, 4] if difficulty == 'Easy' else [0, 1, 2, 3, 4, 5]
    result = puzzle[difficulty][0]
    expressions = puzzle[difficulty][1]

    context = {
        'difficulty': difficulty,
        'num_tiles': num_tiles,
        'boxes': boxes,
        'result': result,
        'expressions': json.dumps(expressions)
    }

    return render(request, 'numbler.html', context)

def next_puzzle(request):
    # Update the difficulty level for the next puzzle
    if 'difficulty' in request.session:
        current_difficulty = request.session['difficulty']
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

            message = f"Next puzzle in {hours} hours and {minutes} minutes"
            return render (request, 'completed.html', {'message':message})
        
    return numbler(request)
