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

    puzzles = {'2024-08-12': {'Tiles': ['3', '5', '6', '8'], 'Easy': (24, ['8*3', '3*8']), 'Medium': (55, ['63-8', '58-3']), 'Hard': (223, ['38*6-5', '6*38-5'])}, '2024-08-13': {'Tiles': ['2', '3', '4', '9'], 'Easy': (15, ['24-9']), 'Medium': (71, ['94-23']), 'Hard': (104, ['3*4+92', '4*3+92', '92+3*4', '92+4*3'])}, '2024-08-14': {'Tiles': ['1', '5', '6', '8'], 'Easy': (7, ['6+1', '8-1', '1+6']), 'Medium': (83, ['65+18', '18+65', '68+15', '15+68']), 'Hard': (111, ['6*5+81', '5*6+81', '81+5*6', '81+6*5'])}, '2024-08-15': {'Tiles': ['1', '6', '7', '9'], 'Easy': (2, ['9-7']), 'Medium': (92, ['97+1-6', '1-6+97', '91+7-6', '91-6+7', '7+91-6', '7-6+91', '1+97-6', '97-6+1']), 'Hard': (147, ['17*9-6', '9*17-6'])}, '2024-08-16': {'Tiles': ['2', '4', '5', '8'], 'Easy': (23, ['28-5']), 'Medium': (35, ['5/4*28', '54/2+8', '28/4*5', '28*5/4', '5*28/4', '8+54/2']), 'Hard': (102, ['4*5+82', '5*4+82', '82+4*5', '82+5*4'])}, '2024-08-17': {'Tiles': ['1', '5', '8', '9'], 'Easy': (11, ['19-8']), 'Medium': (41, ['5*8+1', '8*5+1', '59-18', '1+5*8', '1+8*5']), 'Hard': (489, ['5*98-1', '98*5-1'])}, '2024-08-18': {'Tiles': ['2', '4', '5', '6'], 'Easy': (14, ['56/4']), 'Medium': (72, ['5*6+42', '6*5+42', '42+5*6', '42+6*5']), 'Hard': (204, ['5*42-6', '42*5-6'])}, '2024-08-19': {'Tiles': ['5', '6', '7', '8'], 'Easy': (15, ['7+8', '8+7']), 'Medium': (52, ['58-6']), 'Hard': (108, ['6*5+78', '5*6+78', '78+5*6', '78+6*5'])}, '2024-08-20': {'Tiles': ['1', '4', '6', '8'], 'Easy': (22, ['18+4', '4+18', '14+8', '8+14']), 'Medium': (57, ['61-4']), 'Hard': (271, ['68*4-1', '4*68-1'])}, '2024-08-21': {'Tiles': ['1', '4', '5', '6'], 'Easy': (9, ['5+4', '4+5']), 'Medium': (25, ['4*6+1', '6*4+1', '1+4*6', '1+6*4']), 'Hard': (251, ['41*6+5', '6*41+5', '5+41*6', '5+6*41'])}, '2024-08-22': {'Tiles': ['1', '4', '6', '8'], 'Easy': (7, ['6+1', '8-1', '1+6']), 'Medium': (33, ['41-8']), 'Hard': (106, ['14*8-6', '8*14-6'])}, '2024-08-23': {'Tiles': ['1', '2', '3', '6'], 'Easy': (19, ['6+13', '3+16', '16+3', '13+6']), 'Medium': (68, ['136/2']), 'Hard': (193, ['32*6+1', '6*32+1', '1+32*6', '1+6*32'])}, '2024-08-24': {'Tiles': ['1', '4', '6', '7'], 'Easy': (12, ['16-4']), 'Medium': (72, ['76-4']), 'Hard': (283, ['6*47+1', '47*6+1', '1+47*6', '1+6*47'])}, '2024-08-25': {'Tiles': ['2', '4', '7', '9'], 'Easy': (18, ['9*2', '2*9']), 'Medium': (31, ['27+4', '24+7', '4+27', '7+24']), 'Hard': (117, ['27*4+9', '4*27+9', '9+27*4', '9+4*27'])}, '2024-08-26': {'Tiles': ['3', '5', '7', '8'], 'Easy': (19, ['57/3']), 'Medium': (55, ['58-3']), 'Hard': (152, ['57/3*8', '8*57/3', '57*8/3', '8/3*57'])}, '2024-08-27': {'Tiles': ['1', '5', '8', '9'], 'Easy': (24, ['15+9', '5+19', '19+5', '9+15']), 'Medium': (76, ['81-5', '85-9']), 'Hard': (467, ['51*9+8', '9*51+8', '8+51*9', '8+9*51'])}, '2024-08-28': {'Tiles': ['1', '2', '4', '9'], 'Easy': (6, ['4+2', '2+4']), 'Medium': (32, ['41-9']), 'Hard': (366, ['91*4+2', '4*91+2', '2+4*91', '2+91*4'])}, '2024-08-29': {'Tiles': ['3', '5', '6', '7'], 'Easy': (8, ['3+5', '5+3']), 'Medium': (79, ['76+3', '3+76', '6+73', '73+6']), 'Hard': (231, ['75*3+6', '3*75+6', '6+3*75', '6+75*3'])}, '2024-08-30': {'Tiles': ['1', '4', '6', '8'], 'Easy': (24, ['6*4', '4*6']), 'Medium': (78, ['84-6']), 'Hard': (236, ['61*4-8', '4*61-8'])}, '2024-08-31': {'Tiles': ['2', '4', '6', '7'], 'Easy': (13, ['6+7', '7+6']), 'Medium': (91, ['24+67', '64+27', '67+24', '27+64']), 'Hard': (222, ['6*74/2', '74/2*6', '74*6/2', '6/2*74'])}, '2024-09-01': {'Tiles': ['1', '2', '4', '8'], 'Easy': (23, ['24-1']), 'Medium': (69, ['41+28', '28+41', '48+21', '21+48']), 'Hard': (164, ['41/2*8', '21*8-4', '41*8/2', '8*21-4', '8/2*41', '8*41/2'])}, '2024-09-02': {'Tiles': ['2', '4', '6', '7'], 'Easy': (8, ['4*2', '6+2', '2+6', '2*4']), 'Medium': (100, ['76+24', '74+26', '26+74', '24+76']), 'Hard': (428, ['6*72-4', '72*6-4'])}, '2024-09-03': {'Tiles': ['2', '5', '7', '9'], 'Easy': (4, ['9-5']), 'Medium': (74, ['79-5']), 'Hard': (125, ['59*2+7', '2*59+7', '7+2*59', '7+59*2'])}, '2024-09-04': {'Tiles': ['1', '3', '4', '6'], 'Easy': (18, ['6*3', '3*6']), 'Medium': (51, ['64-13']), 'Hard': (187, ['61*3+4', '3*61+4', '4+3*61', '4+61*3'])}, '2024-09-05': {'Tiles': ['4', '5', '7', '9'], 'Easy': (12, ['7+5', '5+7']), 'Medium': (38, ['45-7', '47-9']), 'Hard': (243, ['4*59+7', '59*4+7', '7+4*59', '7+59*4'])}, '2024-09-06': {'Tiles': ['1', '4', '6', '8'], 'Easy': (3, ['4-1']), 'Medium': (65, ['1+64', '4+61', '61+4', '64+1']), 'Hard': (289, ['48*6+1', '6*48+1', '1+48*6', '1+6*48'])}, '2024-09-07': {'Tiles': ['1', '3', '8', '9'], 'Easy': (5, ['8-3']), 'Medium': (43, ['8*3+19', '3*8+19', '19+3*8', '19+8*3']), 'Hard': (293, ['3*98-1', '98*3-1'])}, '2024-09-08': {'Tiles': ['1', '2', '5', '8'], 'Easy': (13, ['5+8', '8+5']), 'Medium': (36, ['18*2', '2*18']), 'Hard': (171, ['85*2+1', '2*85+1', '1+2*85', '1+85*2'])}, '2024-09-09': {'Tiles': ['2', '5', '6', '8'], 'Easy': (21, ['26-5']), 'Medium': (29, ['58/2']), 'Hard': (203, ['8*26-5', '26*8-5'])}, '2024-09-10': {'Tiles': ['1', '3', '7', '8'], 'Easy': (20, ['17+3', '13+7', '7+13', '3+17']), 'Medium': (26, ['78/3']), 'Hard': (123, ['7*18-3', '18*7-3'])}}  
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

