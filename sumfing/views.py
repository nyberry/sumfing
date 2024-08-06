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

    puzzles = {'2024-08-06': {'Tiles': ['1', '4', '6', '8'], 'Easy': (11, ['4-1+8', '8-1+4', '8+4-1', '4+8-1']), 'Medium': (27, ['68-41']), 'Hard': (76, ['14*6-8', '6*14-8'])}, '2024-08-07': {'Tiles': ['1', '7', '8', '9'], 'Easy': (3, ['9-7+1', '9+1-7', '1+9-7', '1-7+9']), 'Medium': (21, ['91/7+8']), 'Hard': (135, ['18*7+9', '7*18+9'])}, '2024-08-08': {'Tiles': ['3', '4', '7', '8'], 'Easy': (13, ['3*7-8', '7*3-8']), 'Medium': (30, ['78/3+4']), 'Hard': (133, ['3*47-8', '47*3-8'])}, '2024-08-09': {'Tiles': ['2', '3', '4', '6'], 'Easy': (20, ['6*3+2', '3*6+2']), 'Medium': (35, ['64/2+3']), 'Hard': (254, ['4*63+2', '63*4+2'])}, '2024-08-10': {'Tiles': ['1', '2', '4', '5'], 'Easy': (18, ['5*4-2', '4*5-2']), 'Medium': (34, ['2*15+4', '15*2+4']), 'Hard': (107, ['2*54-1', '54*2-1'])}, '2024-08-11': {'Tiles': ['2', '3', '5', '9'], 'Easy': (17, ['3*5+2', '5*3+2']), 'Medium': (36, ['59-23']), 'Hard': (228, ['25*9+3', '9*25+3'])}, '2024-08-12': {'Tiles': ['2', '4', '6', '8'], 'Easy': (11, ['6/2+8']), 'Medium': (47, ['86/2+4']), 'Hard': (322, ['4*82-6', '82*4-6'])}, '2024-08-13': {'Tiles': ['1', '3', '6', '7'], 'Easy': (15, ['3*7-6', '7*3-6']), 'Medium': (46, ['63-17']), 'Hard': (440, ['63*7-1', '7*63-1'])}, '2024-08-14': {'Tiles': ['1', '5', '8', '9'], 'Easy': (16, ['9+8-1', '9-1+8', '8+9-1', '8-1+9']), 'Medium': (22, ['81-59']), 'Hard': (463, ['5*91+8', '91*5+8'])}, '2024-08-15': {'Tiles': ['1', '4', '5', '7'], 'Easy': (10, ['4-1+7', '7+4-1', '4+7-1', '7-1+4']), 'Medium': (26, ['71-45']), 'Hard': (63, ['17*4-5', '14*5-7', '5*14-7', '4*17-5'])}, '2024-08-16': {'Tiles': ['2', '3', '6', '7'], 'Easy': (15, ['3*7-6', '7*3-6', '2*6+3', '6*2+3']), 'Medium': (47, ['73-26']), 'Hard': (159, ['27*6-3', '6*27-3'])}, '2024-08-17': {'Tiles': ['6', '7', '8', '9'], 'Easy': (4, ['6+7-9', '7+6-9', '6-9+7', '7-9+6']), 'Medium': (31, ['98-67']), 'Hard': (459, ['78*6-9', '6*78-9'])}, '2024-08-18': {'Tiles': ['2', '5', '7', '9'], 'Easy': (1, ['2*5-9', '5*2-9']), 'Medium': (46, ['75-29']), 'Hard': (107, ['5*2+97', '2*5+97'])}, '2024-08-19': {'Tiles': ['3', '5', '7', '8'], 'Easy': (9, ['5+7-3', '7-3+5', '7+5-3', '5-3+7']), 'Medium': (34, ['87-53']), 'Hard': (163, ['57*3-8', '3*57-8'])}, '2024-08-20': {'Tiles': ['3', '4', '6', '9'], 'Easy': (11, ['6+9-4', '9-4+6', '6/3+9', '6-4+9', '9+6-4']), 'Medium': (29, ['93-64']), 'Hard': (300, ['34*9-6', '9*34-6'])}, '2024-08-21': {'Tiles': ['3', '4', '5', '8'], 'Easy': (6, ['8-5+3', '3/4*8', '4+5-3', '8+3-5', '3-5+8', '8*3/4', '8/4*3', '3+8-5', '4-3+5', '5+4-3', '5-3+4', '3*8/4']), 'Medium': (21, ['48/3+5']), 'Hard': (237, ['5*48-3', '48*5-3'])}, '2024-08-22': {'Tiles': ['2', '3', '7', '8'], 'Easy': (17, ['3*8-7', '7*2+3', '2*7+3', '8*3-7']), 'Medium': (42, ['78/2+3']), 'Hard': (138, ['73*2-8', '2*73-8'])}, '2024-08-23': {'Tiles': ['1', '4', '5', '7'], 'Easy': (10, ['4-1+7', '7+4-1', '4+7-1', '7-1+4']), 'Medium': (43, ['57-14']), 'Hard': (229, ['4*57+1', '57*4+1'])}, '2024-08-24': {'Tiles': ['3', '4', '7', '9'], 'Easy': (20, ['3*9-7', '9*3-7']), 'Medium': (24, ['73-49']), 'Hard': (139, ['37*4-9', '4*37-9'])}, '2024-08-25': {'Tiles': ['2', '3', '6', '9'], 'Easy': (20, ['6*3+2', '3*6+2']), 'Medium': (46, ['69-23']), 'Hard': (184, ['6*92/3', '92/3*6', '6/3*92', '92*6/3'])}, '2024-08-26': {'Tiles': ['1', '4', '6', '8'], 'Easy': (11, ['4-1+8', '8-1+4', '8+4-1', '4+8-1']), 'Medium': (27, ['68-41']), 'Hard': (484, ['61*8-4', '8*61-4'])}, '2024-08-27': {'Tiles': ['2', '6', '7', '8'], 'Easy': (11, ['6+7-2', '6-2+7', '8/2+7', '6/2+8', '7-2+6', '7+6-2']), 'Medium': (25, ['87-62']), 'Hard': (129, ['68*2-7', '2*68-7'])}, '2024-08-28': {'Tiles': ['4', '5', '6', '8'], 'Easy': (16, ['4*6-8', '6*4-8']), 'Medium': (21, ['85-64']), 'Hard': (328, ['64*5+8', '5*64+8'])}, '2024-08-29': {'Tiles': ['1', '4', '7', '8'], 'Easy': (20, ['7*4-8', '4*7-8']), 'Medium': (23, ['71-48']), 'Hard': (375, ['47*8-1', '8*47-1'])}, '2024-08-30': {'Tiles': ['2', '4', '8', '9'], 'Easy': (20, ['2*8+4', '8*2+4']), 'Medium': (45, ['98/2-4']), 'Hard': (114, ['9*8+42', '8*9+42'])}, '2024-08-31': {'Tiles': ['5', '6', '7', '8'], 'Easy': (4, ['7-8+5', '7+5-8', '5+7-8', '6-7+5', '5-8+7', '5-7+6', '6+5-7', '5+6-7']), 'Medium': (31, ['87-56']), 'Hard': (355, ['58*6+7', '6*58+7'])}, '2024-09-01': {'Tiles': ['3', '5', '6', '9'], 'Easy': (10, ['6+9-5', '5/3*6', '6/3*5', '5*6/3', '6*5/3', '9-5+6', '9+6-5', '6-5+9']), 'Medium': (28, ['93-65']), 'Hard': (107, ['9*6+53', '6*9+53'])}, '2024-09-02': {'Tiles': ['2', '4', '7', '9'], 'Easy': (12, ['7-4+9', '9-4+7', '9+7-4', '7+9-4']), 'Medium': (46, ['74/2+9']), 'Hard': (199, ['7*29-4', '29*7-4'])}, '2024-09-03': {'Tiles': ['2', '4', '8', '9'], 'Easy': (14, ['2*9-4', '9*2-4']), 'Medium': (45, ['98/2-4']), 'Hard': (200, ['2*98+4', '98*2+4'])}, '2024-09-04': {'Tiles': ['4', '5', '8', '9'], 'Easy': (18, ['9/4*8', '9*8/4', '8*9/4', '8/4*9']), 'Medium': (35, ['89-54']), 'Hard': (249, ['5*48+9', '48*5+9'])}}
    puzzle = puzzles.get(today_str)

    if puzzle == None:
        puzzle = puzzles['2024-08-06']

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

