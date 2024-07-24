from django.shortcuts import render
import json
import datetime

def numbler(request):

    puzzles = {'2024-07-24': {'Tiles': ['4', '1', '9', '2'], 'Easy': (44, ['9+2*4', '2+9*4']), 'Medium': (105, ['9-4*21']), 'Hard': (174, ['91-4*2'])}, '2024-07-25': {'Tiles': ['2', '2', '3', '5'], 'Easy': (12, ['2+2*3', '2*5+2', '5*2+2']), 'Medium': (58, ['2*3+52', '3*2+52']), 'Hard': (442, ['5!+322'])}, '2024-07-26': {'Tiles': ['2', '6', '8', '1'], 'Easy': (49, ['6*8+1', '8*6+1']), 'Medium': (120, ['21-6*8', '2+18*6', '8+12*6', '12+8*6', '18+2*6']), 'Hard': (840, ['8-1!/6'])}, '2024-07-27': {'Tiles': ['1', '7', '4', '1'], 'Easy': (35, ['1+4*7', '4+1*7']), 'Medium': (33, ['7-4*11']), 'Hard': (724, ['7-1!+4'])}, '2024-07-28': {'Tiles': ['4', '2', '2', '3'], 'Easy': (11, ['4*2+3', '2*4+3']), 'Medium': (35, ['2/2+34']), 'Hard': (103, ['3^4+22'])}, '2024-07-29': {'Tiles': ['1', '2', '9', '2'], 'Easy': (20, ['1+9*2', '2*9+2', '9+1*2', '9*2+2']), 'Medium': (47, ['92/2+1']), 'Hard': (176, ['9-1*22'])}, '2024-07-30': {'Tiles': ['1', '2', '2', '1'], 'Easy': (5, ['2*2+1']), 'Medium': (44, ['1+21*2', '1+1*22', '21+1*2', '2+2*11']), 'Hard': (145, ['12^2+1'])}, '2024-07-31': {'Tiles': ['5', '9', '6', '3'], 'Easy': (75, ['9+6*5', '6+9*5']), 'Medium': (77, ['6*3+59', '3*6+59']), 'Hard': (971, ['3!+965'])}, '2024-08-01': {'Tiles': ['4', '2', '2', '2'], 'Easy': (3, ['4+2/2', '2+4/2', '2/2+2']), 'Medium': (7, ['22/2-4']), 'Hard': (120, ['2/2+4!'])}, '2024-08-02': {'Tiles': ['7', '3', '4', '2'], 'Easy': (40, ['7+3*4', '3+7*4']), 'Medium': (78, ['37*2+4', '2*37+4']), 'Hard': (579, ['4!^2+3'])}}
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
