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

    puzzles = {'2024-08-08': {'Tiles': ['4', '5', '6', '7'], 'Easy': (17, ['4*6-7', '6*4-7']), 'Medium': (21, ['56/4+7']), 'Hard': (99, ['7*5+64', '6*4+75', '4*6+75', '5*7+64'])}, '2024-08-09': {'Tiles': ['3', '6', '8', '9'], 'Easy': (10, ['6*3-8', '3*6-8', '6/3+8']), 'Medium': (40, ['96/3+8']), 'Hard': (113, ['9*3+86', '3*9+86'])}, '2024-08-10': {'Tiles': ['4', '5', '6', '9'], 'Easy': (19, ['4*6-5', '6*4-5']), 'Medium': (23, ['56/4+9']), 'Hard': (83, ['4*6+59', '6*4+59'])}, '2024-08-11': {'Tiles': ['3', '4', '7', '8'], 'Easy': (6, ['3+7-4', '7-4+3', '8*3/4', '7+3-4', '3-4+7', '3/4*8', '3*8/4', '8/4*3']), 'Medium': (23, ['48/3+7']), 'Hard': (116, ['4/3*87', '87*4/3', '87/3*4', '4*87/3'])}, '2024-08-12': {'Tiles': ['1', '3', '4', '5'], 'Easy': (16, ['5*3+1', '3*5+1']), 'Medium': (37, ['14*3-5', '3*14-5']), 'Hard': (61, ['5*13-4', '13*5-4'])}, '2024-08-13': {'Tiles': ['2', '6', '8', '9'], 'Easy': (20, ['2*6+8', '6*2+8']), 'Medium': (40, ['96/2-8']), 'Hard': (199, ['26*8-9', '8*26-9'])}, '2024-08-14': {'Tiles': ['1', '2', '4', '8'], 'Easy': (11, ['4+8-1', '8+4-1', '8-1+4', '4-1+8']), 'Medium': (40, ['4*12-8', '18*2+4', '12*4-8', '2*18+4']), 'Hard': (172, ['21*8+4', '8*21+4'])}, '2024-08-15': {'Tiles': ['2', '3', '6', '9'], 'Easy': (16, ['6*3-2', '3*6-2']), 'Medium': (30, ['96/3-2']), 'Hard': (84, ['2*39+6', '39*2+6'])}, '2024-08-16': {'Tiles': ['1', '2', '4', '8'], 'Easy': (11, ['4+8-1', '8+4-1', '8-1+4', '4-1+8']), 'Medium': (40, ['4*12-8', '18*2+4', '12*4-8', '2*18+4']), 'Hard': (90, ['41*2+8', '2*41+8'])}, '2024-08-17': {'Tiles': ['3', '4', '5', '8'], 'Easy': (10, ['8/4*5', '5/4*8', '5*8/4', '5-3+8', '8*5/4', '5+8-3', '8+5-3', '8-3+5']), 'Medium': (21, ['48/3+5']), 'Hard': (132, ['35*4-8', '4*35-8'])}, '2024-08-18': {'Tiles': ['4', '5', '6', '7'], 'Easy': (17, ['4*6-7', '6*4-7']), 'Medium': (21, ['56/4+7']), 'Hard': (99, ['7*5+64', '6*4+75', '4*6+75', '5*7+64'])}, '2024-08-19': {'Tiles': ['4', '7', '8', '9'], 'Easy': (19, ['7*4-9', '4*7-9']), 'Medium': (21, ['84/7+9']), 'Hard': (194, ['8*97/4', '97*8/4', '97/4*8', '8/4*97'])}, '2024-08-20': {'Tiles': ['1', '5', '6', '8'], 'Easy': (10, ['5-1+6', '5+6-1', '6+5-1', '6-1+5']), 'Medium': (25, ['81-56']), 'Hard': (99, ['8*6+51', '6*8+51'])}, '2024-08-21': {'Tiles': ['1', '3', '8', '9'], 'Easy': (14, ['9-3+8', '8-3+9', '8+9-3', '9+8-3']), 'Medium': (36, ['81/3+9']), 'Hard': (109, ['9*13-8', '13*9-8'])}, '2024-08-22': {'Tiles': ['1', '2', '6', '8'], 'Easy': (11, ['2*6-1', '6*2-1', '6/2+8']), 'Medium': (40, ['2*16+8', '16*2+8']), 'Hard': (90, ['8*12-6', '12*8-6'])}, '2024-08-23': {'Tiles': ['3', '6', '8', '9'], 'Easy': (16, ['6*8/3', '6/3*8', '8*6/3', '8/3*6']), 'Medium': (40, ['96/3+8']), 'Hard': (195, ['3*68-9', '68*3-9'])}, '2024-08-24': {'Tiles': ['1', '2', '5', '8'], 'Easy': (11, ['8-2+5', '8+5-2', '5+8-2', '5-2+8', '2*5+1', '2*8-5', '8*2-5', '5*2+1']), 'Medium': (22, ['15*2-8', '2*15-8']), 'Hard': (157, ['81*2-5', '2*81-5'])}, '2024-08-25': {'Tiles': ['1', '5', '6', '8'], 'Easy': (10, ['5-1+6', '5+6-1', '6+5-1', '6-1+5']), 'Medium': (25, ['81-56']), 'Hard': (103, ['6*18-5', '18*6-5'])}, '2024-08-26': {'Tiles': ['2', '6', '8', '9'], 'Easy': (20, ['2*6+8', '6*2+8']), 'Medium': (40, ['96/2-8']), 'Hard': (101, ['2*6+89', '6/2+98', '6*2+89'])}, '2024-08-27': {'Tiles': ['2', '4', '5', '8'], 'Easy': (18, ['5*4-2', '2*5+8', '4*5-2', '5*2+8']), 'Medium': (26, ['54-28']), 'Hard': (64, ['5*8+24', '8*5+24'])}, '2024-08-28': {'Tiles': ['1', '2', '8', '9'], 'Easy': (5, ['8/2+1']), 'Medium': (45, ['2*18+9', '18*2+9']), 'Hard': (164, ['9*18+2', '18*9+2'])}, '2024-08-29': {'Tiles': ['1', '2', '3', '6'], 'Easy': (20, ['6*3+2', '3*6+2']), 'Medium': (46, ['16*3-2', '3*16-2']), 'Hard': (76, ['13*6-2', '6*13-2'])}, '2024-08-30': {'Tiles': ['2', '3', '4', '6'], 'Easy': (20, ['6*3+2', '3*6+2']), 'Medium': (35, ['64/2+3']), 'Hard': (147, ['24*6+3', '6*24+3'])}, '2024-08-31': {'Tiles': ['3', '4', '5', '8'], 'Easy': (6, ['4-3+5', '3+8-5', '3-5+8', '8*3/4', '4+5-3', '8+3-5', '5-3+4', '3/4*8', '3*8/4', '8/4*3', '8-5+3', '5+4-3']), 'Medium': (21, ['48/3+5']), 'Hard': (97, ['3*4+85', '4*3+85'])}, '2024-09-01': {'Tiles': ['4', '5', '6', '7'], 'Easy': (17, ['4*6-7', '6*4-7']), 'Medium': (21, ['56/4+7']), 'Hard': (99, ['7*5+64', '6*4+75', '4*6+75', '5*7+64'])}, '2024-09-02': {'Tiles': ['1', '2', '4', '5'], 'Easy': (18, ['4*5-2', '5*4-2']), 'Medium': (33, ['54-21', '45-12']), 'Hard': (109, ['54*2+1', '21*5+4', '2*54+1', '5*21+4'])}, '2024-09-03': {'Tiles': ['3', '4', '7', '8'], 'Easy': (14, ['7/4*8', '7*8/4', '8*7/4', '8/4*7']), 'Medium': (23, ['48/3+7']), 'Hard': (145, ['4*38-7', '38*4-7'])}, '2024-09-04': {'Tiles': ['2', '5', '6', '9'], 'Easy': (13, ['6+9-2', '9*2-5', '6-2+9', '9+6-2', '9-2+6', '2*9-5']), 'Medium': (37, ['56/2+9']), 'Hard': (151, ['29*5+6', '5*29+6'])}, '2024-09-05': {'Tiles': ['4', '5', '6', '9'], 'Easy': (8, ['5+9-6', '9-6+5', '9-5+4', '4+9-5', '4-5+9', '9+4-5', '5-6+9', '9+5-6']), 'Medium': (23, ['56/4+9']), 'Hard': (124, ['6*5+94', '5*6+94'])}, '2024-09-06': {'Tiles': ['1', '2', '4', '6'], 'Easy': (13, ['2*6+1', '6*2+1']), 'Medium': (31, ['64/2-1']), 'Hard': (127, ['2*64-1', '64*2-1'])}}
    puzzle = puzzles.get(today_str)

    if puzzle == None:
        puzzle = puzzles['2024-08-08']

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

