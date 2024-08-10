from django.shortcuts import render
from django.shortcuts import redirect
import json
import datetime
import time
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def index(request):

    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")

    puzzles = {'2024-08-09': {'Tiles': ['1', '2', '4', '9'], 'Easy': (5, ['1+4', '9-4', '4+1']), 'Medium': (33, ['24+9', '9+24', '29+4', '4+29', '42-9']), 'Hard': (188, ['2*94', '94*2'])}, '2024-08-10': {'Tiles': ['2', '4', '6', '7'], 'Easy': (14, ['2*7', '7*2']), 'Medium': (23, ['46/2', '27-4']), 'Hard': (84, ['6*7+42', '7*6+42', '2*4+76', '4*2+76', '42+7*6', '42+6*7', '76+2*4', '76+4*2'])}, '2024-08-11': {'Tiles': ['2', '3', '4', '7'], 'Easy': (6, ['2+4', '3*2', '4+2', '2*3']), 'Medium': (30, ['3+27', '7+23', '23+7', '27+3']), 'Hard': (141, ['47*3', '3*47'])}, '2024-08-12': {'Tiles': ['2', '6', '7', '8'], 'Easy': (3, ['6/2']), 'Medium': (34, ['6+28', '28+6', '68/2', '26+8', '8+26']), 'Hard': (180, ['2*87+6', '87*2+6'])}, '2024-08-13': {'Tiles': ['3', '5', '6', '7'], 'Easy': (10, ['3+7', '7+3']), 'Medium': (31, ['36-5', '37-6']), 'Hard': (179, ['5*37-6', '37*5-6'])}, '2024-08-14': {'Tiles': ['2', '4', '7', '9'], 'Easy': (14, ['2*7', '7*2']), 'Medium': (26, ['4*7-2', '7*4-2']), 'Hard': (59, ['7*9-4', '9*7-4'])}, '2024-08-15': {'Tiles': ['1', '2', '6', '9'], 'Easy': (3, ['6/2', '1+2', '2+1', '9-6']), 'Medium': (43, ['62-19']), 'Hard': (114, ['19*6', '6*19'])}, '2024-08-16': {'Tiles': ['1', '5', '8', '9'], 'Easy': (11, ['19-8']), 'Medium': (44, ['5*9-1', '9*5-1']), 'Hard': (131, ['5*8+91', '8*5+91'])}, '2024-08-17': {'Tiles': ['2', '4', '5', '7'], 'Easy': (19, ['24-5']), 'Medium': (48, ['52-4']), 'Hard': (115, ['2*54+7', '54*2+7'])}, '2024-08-18': {'Tiles': ['4', '7', '8', '9'], 'Easy': (5, ['9-4']), 'Medium': (39, ['48-9', '47-8']), 'Hard': (76, ['9*8+4', '8*9+4'])}}
    puzzle = puzzles.get(today_str)

    if puzzle == None:
        puzzle = puzzles['2024-08-09']

    date_of_first_puzzle = datetime.datetime.strptime("2024-07-25", "%Y-%m-%d").date()
    days_since_start = (today - date_of_first_puzzle).days

    # check if user has ever visited before:
    if 'date_str' in request.session:

        # if user has already visited today, redirect to game play page:
        if request.session['date_str']==today_str:
            return redirect('sumfing') 
            
    # this is user's first visit today, so reset the session data
    current_time=time.time()
    request.session['difficulty']='Easy'
    request.session['puzzle']=puzzle
    request.session['date_str']=today_str
    request.session['game_no']=days_since_start
    request.session['start_time']=current_time
    return redirect('sumfing')


@csrf_protect
def sumfing(request):

    # redirect if the user has come here by entering route in browser, without starting a session
    if 'date_str' not in request.session:
        return redirect ('index')
    
    # get the session data, redirect if a problem
    try:
        puzzle = request.session['puzzle']
        num_tiles = puzzle['Tiles']
        difficulty = request.session['difficulty']
    except:
        return redirect ('index')

    # redirect if the game is finished
    if difficulty == "Completed":
        return redirect('completed')

    # render the puzzle page
    result = puzzle[difficulty][0]
    expressions = puzzle[difficulty][1]
    boxes = [tile for tile in expressions[0]]
    context = {
        'difficulty': difficulty.lower(),
        'num_tiles': num_tiles,
        'boxes': boxes,
        'result': result,
        'expressions': json.dumps(expressions)
    }
    return render(request, 'sumfing.html', context)


@csrf_protect
def next_puzzle(request):

    # redirect if not here by form button
    if request.method != 'POST':
        return redirect('index')
    
    # OK to move to next puzzle
    if 'hints' not in request.session:
        request.session['hints'] = ['-1','-1','-1']

    if 'difficulty' not in request.session:
        request.session['difficulty'] = "unknown"
    
    current_difficulty = request.session['difficulty']

    # keep track of how many hints were given
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
        current_time = time.time()
        if 'start_time' in request.session:
            time_taken = int(current_time- request.session['start_time'])
            request.session['time_taken'] = time_taken

    # If the puzzle completed
    if request.session['difficulty'] == 'Completed':
        return redirect('completed')
                
    return sumfing(request)


def completed(request):

    # redirect if the user came here by browswer line
    if 'difficulty' not in request.session:
        return redirect('index')
    
    if request.session['difficulty'] != "Completed":
        return redirect('index')

    # Make a message about how many hints have been given
    hints_given = request.session['hints']
    hints_message = []
    for i in range(len(hints_given)):
        if hints_given[i]=='-1':
            result = "?"
        elif hints_given[i]=='0':
            result = "✅"
        elif hints_given[i]=='1':
            result =f'💡✅'
        elif hints_given[i]=='2':
            result =f'💡💡✅'
        elif hints_given[i]=='3':
            result = "❌"
        hints_message.append(result)    
    
    game_no = request.session['game_no']
    if 'time_taken' in request.session:
        time_taken = request.session['time_taken']
        time_taken_message = f'🕒 {time_taken} seconds\n'
    else:
        time_taken_message = ''
    html_message = f'Sumfing #{game_no}\n\nEasy: {hints_message[0]}\nMedium: {hints_message[1]}\nHard: {hints_message[2]}\n\n{time_taken_message}'
    whatsapp_message = f'Sumfing #{game_no}\nEasy: {hints_message[0]}\nMedium: {hints_message[1]}\nHard: {hints_message[2]}\nPlay at sumfing.com'

    # Make next game message:
    # 1. Get the current date and time
    now = datetime.datetime.now()
    # 2. Get the start of tomorrow
    tomorrow = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    # 3. Calculate the time difference
    time_difference = tomorrow - now
    # 4. Convert the difference to hours and minutes
    total_seconds = time_difference.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    # 5. Form the message string
    next_game_message = f'Sumfing else in\n{hours} hours and {minutes} minutes'

    context = {
        'html_message':html_message,
        'whatsapp_message':whatsapp_message,
        'next_game_message':next_game_message,
    }

    return render (request, 'completed.html', context)

