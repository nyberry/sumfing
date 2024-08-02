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

    puzzles = {'2024-08-02': {'Tiles': ['1', '2', '8', '9'], 'Easy': (15, ['2*8-1', '8+9-2', '8-2+9', '8*2-1', '9+8-2', '9-2+8']), 'Medium': (48, ['98/2-1']), 'Hard': (255, ['2^8-1'])}, '2024-08-03': {'Tiles': ['3', '5', '6', '7'], 'Easy': (16, ['3*7-5', '7*3-5']), 'Medium': (44, ['65-3*7', '65-7*3']), 'Hard': (223, ['6^3+7', '7+6^3'])}, '2024-08-04': {'Tiles': ['2', '3', '4', '6'], 'Easy': (15, ['2*6+3', '3+2*6', '3+6*2', '6*2+3']), 'Medium': (50, ['62-3*4', '62-4*3']), 'Hard': (158, ['632/4'])}, '2024-08-05': {'Tiles': ['2', '3', '6', '9'], 'Easy': (10, ['3+9-2', '3-2+9', '9+3-2', '9-2+3']), 'Medium': (30, ['96/3-2']), 'Hard': (2352, ['392*6', '6*392'])}, '2024-08-06': {'Tiles': ['2', '3', '4', '6'], 'Easy': (20, ['2+3*6', '2+6*3', '3*6+2', '6*3+2']), 'Medium': (50, ['62-3*4', '62-4*3']), 'Hard': (552, ['23*4!', '4!*23'])}, '2024-08-07': {'Tiles': ['3', '4', '5', '7'], 'Easy': (16, ['3*7-5', '7*3-5']), 'Medium': (24, ['45-3*7', '45-7*3']), 'Hard': (6064, ['4^5+7!', '7!+4^5'])}, '2024-08-08': {'Tiles': ['1', '3', '6', '8'], 'Easy': (10, ['3+8-1', '3-1+8', '3*6-8', '6*3-8', '6/3+8', '8+3-1', '8+6/3', '8-1+3']), 'Medium': (22, ['38-16', '83-61']), 'Hard': (227, ['681/3'])}, '2024-08-09': {'Tiles': ['5', '7', '8', '9'], 'Easy': (10, ['7+8-5', '7-5+8', '8+7-5', '8+9-7', '8-5+7', '8-7+9', '9+8-7', '9-7+8']), 'Medium': (42, ['87-5*9', '87-9*5']), 'Hard': (9072, ['7!*9/5', '7!/5*9', '9*7!/5', '9/5*7!'])}, '2024-08-10': {'Tiles': ['2', '5', '6', '9'], 'Easy': (13, ['2*9-5', '6+9-2', '6-2+9', '9+6-2', '9-2+6', '9*2-5']), 'Medium': (36, ['65-29', '92-56']), 'Hard': (3588, ['52*69', '69*52'])}, '2024-08-11': {'Tiles': ['5', '6', '7', '9'], 'Easy': (10, ['6+9-5', '6-5+9', '7+9-6', '7-6+9', '9+6-5', '9+7-6', '9-5+6', '9-6+7']), 'Medium': (22, ['67-5*9', '67-9*5']), 'Hard': (835, ['7!/6-5'])}, '2024-08-12': {'Tiles': ['4', '6', '7', '9'], 'Easy': (12, ['7+9-4', '7-4+9', '9+7-4', '9-4+7']), 'Medium': (40, ['76-4*9', '76-9*4']), 'Hard': (676, ['4+7*96', '4+96*7', '7*96+4', '96*7+4'])}, '2024-08-13': {'Tiles': ['3', '4', '7', '8'], 'Easy': (6, ['3+7-4', '3-4+7', '3*8/4', '3/4*8', '7+3-4', '7-4+3', '8*3/4', '8/4*3']), 'Medium': (23, ['47-3*8', '47-8*3', '48/3+7', '7+48/3']), 'Hard': (99, ['3*4+87', '43+7*8', '43+8*7', '4*3+87', '7*8+43', '87+3*4', '87+4*3', '8*7+43'])}, '2024-08-14': {'Tiles': ['4', '5', '7', '9'], 'Easy': (10, ['5+9-4', '5-4+9', '9+5-4', '9-4+5']), 'Medium': (25, ['79-54']), 'Hard': (1076, ['5!*9-4', '9*5!-4'])}, '2024-08-15': {'Tiles': ['2', '4', '6', '8'], 'Easy': (5, ['8-6/2']), 'Medium': (39, ['86/2-4']), 'Hard': (4070, ['8^4-26'])}, '2024-08-16': {'Tiles': ['1', '4', '6', '9'], 'Easy': (11, ['6+9-4', '6-4+9', '9+6-4', '9-4+6']), 'Medium': (28, ['69-41']), 'Hard': (222, ['4!*9+6', '6+4!*9', '6+9*4!', '9*4!+6'])}, '2024-08-17': {'Tiles': ['1', '2', '7', '9'], 'Easy': (4, ['2+9-7', '2-7+9', '9+2-7', '9-7+2']), 'Medium': (42, ['71-29']), 'Hard': (3584, ['2^9*7', '7*2^9'])}, '2024-08-18': {'Tiles': ['1', '3', '6', '8'], 'Easy': (10, ['3+8-1', '3-1+8', '3*6-8', '6*3-8', '6/3+8', '8+3-1', '8+6/3', '8-1+3']), 'Medium': (22, ['38-16', '83-61']), 'Hard': (237, ['3*81-6', '81*3-6'])}, '2024-08-19': {'Tiles': ['2', '4', '8', '9'], 'Easy': (20, ['2*8+4', '4+2*8', '4+8*2', '8*2+4']), 'Medium': (45, ['49-8/2', '98/2-4']), 'Hard': (740, ['4+8*92', '4+92*8', '8*92+4', '92*8+4'])}, '2024-08-20': {'Tiles': ['1', '3', '5', '7'], 'Easy': (11, ['5+7-1', '5-1+7', '7+5-1', '7-1+5']), 'Medium': (30, ['51-3*7', '51-7*3']), 'Hard': (975, ['13*75', '75*13'])}, '2024-08-21': {'Tiles': ['4', '7', '8', '9'], 'Easy': (20, ['4*7-8', '7*4-8']), 'Medium': (21, ['84-7*9', '84-9*7', '84/7+9', '9+84/7']), 'Hard': (6732, ['748*9', '9*748'])}, '2024-08-22': {'Tiles': ['3', '4', '5', '8'], 'Easy': (6, ['3+8-5', '3-5+8', '3*8/4', '3/4*8', '4+5-3', '4-3+5', '5+4-3', '5-3+4', '8+3-5', '8-5+3', '8*3/4', '8/4*3']), 'Medium': (30, ['54-3*8', '54-8*3']), 'Hard': (6681, ['3^8+5!', '5!+3^8'])}, '2024-08-23': {'Tiles': ['1', '6', '7', '9'], 'Easy': (14, ['6+9-1', '6-1+9', '9+6-1', '9-1+6']), 'Medium': (49, ['91-6*7', '91-7*6']), 'Hard': (53, ['6*9-1', '9*6-1'])}, '2024-08-24': {'Tiles': ['3', '4', '6', '9'], 'Easy': (8, ['3+9-4', '3-4+9', '4*6/3', '4/3*6', '6*4/3', '6/3*4', '9+3-4', '9-4+3']), 'Medium': (26, ['69-43']), 'Hard': (4093, ['4^6-3'])}, '2024-08-25': {'Tiles': ['4', '5', '6', '9'], 'Easy': (19, ['4*6-5', '6*4-5']), 'Medium': (23, ['56/4+9', '9+56/4']), 'Hard': (93, ['4!+69', '69+4!'])}, '2024-08-26': {'Tiles': ['2', '3', '6', '8'], 'Easy': (13, ['2*8-3', '8*2-3']), 'Medium': (35, ['63-28']), 'Hard': (5172, ['3!*862', '862*3!'])}, '2024-08-27': {'Tiles': ['2', '4', '7', '8'], 'Easy': (20, ['2*8+4', '4+2*8', '4+8*2', '4*7-8', '7*4-8', '8*2+4']), 'Medium': (40, ['72-4*8', '72-8*4']), 'Hard': (311, ['287+4!', '4!+287'])}, '2024-08-28': {'Tiles': ['3', '4', '6', '8'], 'Easy': (20, ['3*4+8', '3*8-4', '4*3+8', '8+3*4', '8+4*3', '8*3-4']), 'Medium': (31, ['63-4*8', '63-8*4']), 'Hard': (4058, ['4^6-38'])}, '2024-08-29': {'Tiles': ['3', '6', '7', '8'], 'Easy': (17, ['3*8-7', '8*3-7']), 'Medium': (49, ['86-37']), 'Hard': (5876, ['7!+836', '836+7!'])}, '2024-08-30': {'Tiles': ['4', '5', '7', '9'], 'Easy': (10, ['5+9-4', '5-4+9', '9+5-4', '9-4+5']), 'Medium': (34, ['79-45']), 'Hard': (214, ['5!+94', '94+5!'])}, '2024-08-31': {'Tiles': ['3', '4', '5', '7'], 'Easy': (16, ['3*7-5', '7*3-5']), 'Medium': (24, ['45-3*7', '45-7*3']), 'Hard': (4995, ['7!-45'])}}

    puzzle = puzzles.get(today_str)

    if puzzle == None:
        puzzle = puzzles['2024-08-02']

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

