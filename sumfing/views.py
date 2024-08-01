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

    puzzles = {'2024-08-01': {'Tiles': ['6', '1', '3', '3'], 'Easy': (8, ['6+3-1', '6-1+3', '3+6-1', '3-1+6', '3*3-1']), 'Medium': (51, ['16*3+3', '3+16*3', '3+3*16', '3*16+3']), 'Hard': (130, ['136-3!'])}, '2024-08-02': {'Tiles': ['2', '1', '2', '7'], 'Easy': (16, ['2+2*7', '2+7*2', '2*7+2', '7*2+2']), 'Medium': (55, ['27*2+1', '2*27+1', '1+27*2', '1+2*27']), 'Hard': (588, ['12*7^2', '7^2*12'])}, '2024-08-03': {'Tiles': ['4', '8', '9', '7'], 'Easy': (18, ['8*9/4', '8/4*9', '9*8/4', '9/4*8']), 'Medium': (46, ['48+7-9', '48-9+7', '47+8-9', '47-9+8', '8+47-9', '8-9+47', '7+48-9', '7-9+48']), 'Hard': (556, ['7!/9-4'])}, '2024-08-04': {'Tiles': ['8', '2', '6', '1'], 'Easy': (17, ['8*2+1', '2*8+1', '1+8*2', '1+2*8']), 'Medium': (35, ['68/2+1', '1+68/2']), 'Hard': (464, ['6!-2^8'])}, '2024-08-05': {'Tiles': ['4', '5', '3', '5'], 'Easy': (11, ['5*3-4', '3*5-4']), 'Medium': (36, ['5+35-4', '5-4+35', '35+5-4', '35-4+5']), 'Hard': (234, ['354-5!'])}, '2024-08-06': {'Tiles': ['2', '4', '1', '5'], 'Easy': (18, ['4*5-2', '5*4-2']), 'Medium': (79, ['21*4-5', '4*21-5']), 'Hard': (292, ['412-5!'])}, '2024-08-07': {'Tiles': ['9', '2', '2', '5'], 'Easy': (6, ['9+2-5', '9-5+2', '2+9-5', '2-5+9', '2/2+5', '5+2/2']), 'Medium': (60, ['2/2+59', '59+2/2']), 'Hard': (392, ['2^9-5!'])}, '2024-08-08': {'Tiles': ['2', '2', '3', '4'], 'Easy': (11, ['2*4+3', '3+2*4', '3+4*2', '4*2+3']), 'Medium': (35, ['2/2+34', '34+2/2']), 'Hard': (208, ['232-4!'])}, '2024-08-09': {'Tiles': ['3', '4', '3', '2'], 'Easy': (15, ['3+4*3', '3+3*4', '3*4+3', '4*3+3']), 'Medium': (65, ['34*2-3', '3*23-4', '23*3-4', '2*34-3']), 'Hard': (573, ['4!^2-3'])}, '2024-08-10': {'Tiles': ['3', '2', '1', '6'], 'Easy': (20, ['3*6+2', '2+3*6', '2+6*3', '6*3+2']), 'Medium': (56, ['31*2-6', '2*31-6']), 'Hard': (90, ['6!/2^3'])}}

    puzzle = puzzles.get(today_str)

    if puzzle == None:
        puzzle = puzzles['2024-08-01']

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
            result =f'💡'
        elif hints_given[i]=='2':
            result =f'💡💡'
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
    whatsapp_message = f'Sumfing #{game_no}\nEasy: {hints_message[0]}\nMedium: {hints_message[1]}\nHard: {hints_message[2]}\n{time_taken_message}Play at sumfing.com'

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

