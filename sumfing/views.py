from django.shortcuts import render
from django.shortcuts import redirect
import json
import datetime

def welcome(request):

    puzzles = {'2024-07-25': {'Tiles': ['2', '2', '6', '5'], 'Easy': (14, ['6*2+2', '2+6*2', '2*6+2', '2+2*6']), 'Medium': (20, ['52/2-6']), 'Hard': (688, ['6!-2^5'])}, '2024-07-26': {'Tiles': ['3', '3', '2', '4'], 'Easy': (10, ['3*2+4', '3*4-2', '2*3+4', '4+3*2', '4+2*3', '4*3-2']), 'Medium': (95, ['23*4+3', '4*23+3','3+23*4', '3+4*23']), 'Hard': (228, ['234-3!'])}, '2024-07-27': {'Tiles': ['4', '1', '3', '5'], 'Easy': (16, ['1+3*5', '1+5*3', '3*5+1', '5*3+1','4*3+1','4*1+3','3+1*4','1+3*4','5-1*4','4*5-1']), 'Medium': (37, ['14*3-5', '3*14-5']), 'Hard': (219, ['3^5-4!'])}, '2024-07-28': {'Tiles': ['1', '9', '8', '4'], 'Easy': (16, ['9+8-1', '9-1+8', '8+9-1', '8-1+9']), 'Medium': (56, ['9+48-1', '9-1+48', '8+49-1', '8-1+49', '49+8-1', '49-1+8', '48+9-1', '48-1+9']), 'Hard': (183, ['8*4!-9', '4!*8-9'])}, '2024-07-29': {'Tiles': ['1', '4', '6', '1'], 'Easy': (9, ['4+6-1', '4-1+6', '6+4-1', '6-1+4']), 'Medium': (83, ['14*6-1', '6*14-1']), 'Hard': (92, ['116-4!'])}}
    
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    
    puzzle = puzzles.get(date_str)
    print(puzzle)

    if puzzle == None:
        puzzle = puzzles['2024-07-25']

    request.session['difficulty']='Easy'
    request.session['puzzle']=puzzle
    request.session['date_str']=date_str

    return redirect('sumfing')


def sumfing(request):
    
    puzzle = request.session['puzzle']
    num_tiles = puzzle['Tiles']

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

    return render(request, 'sumfing.html', context)


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
                result = "?"
            elif hints_given[i]=='0':
                result = "✅"
            elif hints_given[i]=='1':
                result =f'💡'
            elif hints_given[i]=='2':
                result =f'💡💡'
            elif hints_given[i]=='3':
                result = "❌"
            hints_message.append(result)    
        
        date_str = request.session['date_str']
        html_message = f'sum🎓fing {date_str}\n\nEasy: {hints_message[0]}\nMedium: {hints_message[1]}\nHard: {hints_message[2]}\n\n'
        whatsapp_message = f'sum🎓fing {date_str}\nEasy: {hints_message[0]}\nMedium: {hints_message[1]}\nHard: {hints_message[2]}\nsumfing.com'
           
        next_game_message = f"sum🎓fing else in {hours} hours and {minutes} minutes"


        context = {
            'html_message':html_message,
            'whatsapp_message':whatsapp_message,
            'next_game_message':next_game_message,
        }

        return render (request, 'completed.html', context)
        
    return sumfing(request)
