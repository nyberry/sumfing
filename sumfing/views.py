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

    puzzles = {'2024-08-14': {'Tiles': ['0', '2', '5', '6'], 'Easy': (14, ['20-6']), 'Medium': (31, ['6+25', '5+26', '26+5', '25+6']), 'Hard': (106, ['50*2+6', '20*5+6', '2*50+6', '5*20+6', '6+20*5', '6+2*50', '6+50*2', '6+5*20']), 'Extra': (140, ['20+5!', '5!+20'])}, '2024-08-15': {'Tiles': ['0', '4', '7', '8'], 'Easy': (3, ['7-4']), 'Medium': (52, ['7*8-4', '8*7-4']), 'Hard': (127, ['47+80', '40+87', '87+40', '80+47']), 'Extra': (848, ['0!+847', '847+0!'])}, '2024-08-16': {'Tiles': ['0', '1', '2', '5'], 'Easy': (19, ['20-1']), 'Medium': (42, ['52-10', '210/5']), 'Hard': (196, ['201-5']), 'Extra': (255, ['510/2'])}, '2024-08-17': {'Tiles': ['2', '6', '7', '8'], 'Easy': (1, ['7-6', '8-7']), 'Medium': (93, ['7+86', '87+6', '6+87', '86+7']), 'Hard': (113, ['86+27', '87+26', '26+87', '27+86']), 'Extra': (180, ['7!/28'])}, '2024-08-18': {'Tiles': ['1', '5', '6', '8'], 'Easy': (24, ['8+16', '18+6', '6+18', '16+8']), 'Medium': (82, ['6-5+81', '86+1-5', '81-5+6', '1-5+86', '15*6-8', '81+6-5', '6*15-8', '86-5+1', '1+86-5', '6+81-5']), 'Hard': (191, ['186+5', '5+186', '185+6', '6+185']), 'Extra': (491, ['81*6+5', '6*81+5', '5+6*81', '5+81*6'])}, '2024-08-19': {'Tiles': ['2', '3', '5', '8'], 'Easy': (19, ['38/2']), 'Medium': (88, ['3+85', '5+83', '83+5', '85+3']), 'Hard': (119, ['58*2+3', '2*58+3', '3+2*58', '3+58*2']), 'Extra': (150, ['25*3!', '3!*25'])}, '2024-08-20': {'Tiles': ['3', '5', '7', '9'], 'Easy': (4, ['7-3', '9-5']), 'Medium': (64, ['73-9']), 'Hard': (170, ['3*59-7', '59*3-7']), 'Extra': (236, ['3^5-7'])}, '2024-08-21': {'Tiles': ['1', '2', '4', '8'], 'Easy': (25, ['21+4', '1+24', '24+1', '4+21']), 'Medium': (27, ['28-1']), 'Hard': (191, ['8*24-1', '24*8-1']), 'Extra': (728, ['4*182', '182*4'])}, '2024-08-22': {'Tiles': ['0', '2', '4', '7'], 'Easy': (16, ['20-4']), 'Medium': (26, ['7*4-2', '4*7-2']), 'Hard': (112, ['40+72', '70+42', '72+40', '42+70']), 'Extra': (723, ['724-0!'])}, '2024-08-23': {'Tiles': ['3', '4', '8', '9'], 'Easy': (2, ['8/4']), 'Medium': (31, ['39-8']), 'Hard': (110, ['3*4+98', '4*3+98', '98+3*4', '98+4*3']), 'Extra': (164, ['39*4+8', '4*39+8', '984/3!', '8+39*4', '8+4*39'])}, '2024-08-24': {'Tiles': ['2', '3', '6', '9'], 'Easy': (14, ['23-9']), 'Medium': (61, ['63-2']), 'Hard': (129, ['6*23-9', '23*6-9']), 'Extra': (232, ['39*6-2', '6*39-2'])}, '2024-08-25': {'Tiles': ['1', '3', '4', '5'], 'Easy': (12, ['4*3', '3*4']), 'Medium': (49, ['53-4']), 'Hard': (148, ['145+3', '143+5', '3+145', '5+143']), 'Extra': (166, ['5^3+41', '41+5^3'])}, '2024-08-26': {'Tiles': ['0', '1', '5', '6'], 'Easy': (2, ['10/5']), 'Medium': (45, ['51-6']), 'Hard': (101, ['106-5']), 'Extra': (145, ['6!/5+1', '1+6!/5'])}, '2024-08-27': {'Tiles': ['1', '2', '3', '6'], 'Easy': (11, ['13-2']), 'Medium': (51, ['63-12']), 'Hard': (165, ['2+163', '163+2', '3+162', '162+3']), 'Extra': (588, ['6!-132'])}, '2024-08-28': {'Tiles': ['0', '5', '6', '9'], 'Easy': (3, ['9-6']), 'Medium': (47, ['56-9']), 'Hard': (119, ['69+50', '60+59', '59+60', '50+69']), 'Extra': (648, ['9!/560'])}, '2024-08-29': {'Tiles': ['0', '1', '5', '8'], 'Easy': (23, ['5+18', '15+8', '18+5', '8+15']), 'Medium': (75, ['80-5']), 'Hard': (113, ['105+8', '108+5', '8+105', '5+108']), 'Extra': (816, ['0!+815', '815+0!'])}, '2024-08-30': {'Tiles': ['2', '3', '5', '6'], 'Easy': (15, ['5*3', '3*5']), 'Medium': (90, ['5*36/2', '5/2*36', '36*5/2', '36/2*5']), 'Hard': (170, ['3*56+2', '56*3+2', '2+3*56', '2+56*3']), 'Extra': (141, ['6!/5-3'])}, '2024-08-31': {'Tiles': ['2', '3', '4', '7'], 'Easy': (6, ['4+2', '2+4', '2*3', '3*2']), 'Medium': (26, ['4*7-2', '7*4-2']), 'Hard': (171, ['7*24+3', '24*7+3', '3+24*7', '3+7*24']), 'Extra': (144, ['3!*24', '24*3!'])}, '2024-09-01': {'Tiles': ['0', '4', '7', '8'], 'Easy': (20, ['80/4']), 'Medium': (36, ['7*4+8', '4*7+8', '8+4*7', '8+7*4']), 'Hard': (120, ['840/7']), 'Extra': (873, ['874-0!'])}, '2024-09-02': {'Tiles': ['0', '7', '8', '9'], 'Easy': (17, ['8+9', '9+8']), 'Medium': (91, ['98-7']), 'Hard': (146, ['8*7+90', '7*8+90', '90+7*8', '90+8*7']), 'Extra': (878, ['879-0!'])}, '2024-09-03': {'Tiles': ['2', '3', '7', '9'], 'Easy': (12, ['3+9', '9+3']), 'Medium': (100, ['3+97', '93+7', '97+3', '7+93']), 'Hard': (170, ['23*7+9', '7*23+9', '9+23*7', '9+7*23']), 'Extra': (105, ['2^3+97', '97+2^3'])}, '2024-09-04': {'Tiles': ['1', '2', '4', '7'], 'Easy': (18, ['72/4']), 'Medium': (80, ['7*12-4', '12*7-4']), 'Hard': (135, ['142-7']), 'Extra': (577, ['4!^2+1', '1+4!^2'])}, '2024-09-05': {'Tiles': ['1', '3', '5', '7'], 'Easy': (21, ['3*7', '7*3']), 'Medium': (78, ['75+3', '3+75', '5+73', '73+5']), 'Hard': (168, ['173-5']), 'Extra': (251, ['371-5!'])}, '2024-09-06': {'Tiles': ['1', '3', '5', '9'], 'Easy': (22, ['31-9', '13+9', '9+13', '3+19', '19+3']), 'Medium': (28, ['9*3+1', '59-31', '3*9+1', '1+3*9', '1+9*3']), 'Hard': (156, ['159-3']), 'Extra': (278, ['91*3+5', '3*91+5', '5+3*91', '5+91*3'])}, '2024-09-07': {'Tiles': ['5', '6', '7', '8'], 'Easy': (11, ['6+5', '5+6']), 'Medium': (70, ['7-5+68', '67+8-5', '67-5+8', '68-5+7', '8+67-5', '68+7-5', '8-5+67', '7+68-5']), 'Hard': (125, ['57+68', '58+67', '68+57', '67+58']), 'Extra': (100, ['8*75/6', '6*7+58', '8/6*75', '7*6+58', '75/6*8', '75*8/6', '58+6*7', '58+7*6'])}, '2024-09-08': {'Tiles': ['1', '2', '5', '7'], 'Easy': (4, ['5-1']), 'Medium': (31, ['7-1+25', '27+5-1', '5+27-1', '27-1+5', '5-1+27', '25+7-1', '7+25-1', '25-1+7']), 'Hard': (103, ['15*7-2', '7*15-2']), 'Extra': (336, ['7!/15'])}, '2024-09-09': {'Tiles': ['0', '1', '2', '9'], 'Easy': (8, ['9-1']), 'Medium': (39, ['10+29', '20+19', '29+10', '19+20']), 'Hard': (111, ['2+109', '120-9', '9+102', '90+21', '102+9', '91+20', '21+90', '20+91', '109+2']), 'Extra': (513, ['2^9+1', '1+2^9'])}, '2024-09-10': {'Tiles': ['4', '5', '7', '8'], 'Easy': (20, ['4*5', '5*4']), 'Medium': (31, ['7*5-4', '5*7-4']), 'Hard': (107, ['5*4+87', '4*5+87', '8*4+75', '4*8+75', '75+4*8', '75+8*4', '87+4*5', '87+5*4']), 'Extra': (628, ['748-5!'])}, '2024-09-11': {'Tiles': ['2', '3', '4', '5'], 'Easy': (21, ['24-3', '25-4']), 'Medium': (47, ['2+45', '42+5', '5+42', '45+2']), 'Hard': (133, ['532/4']), 'Extra': (573, ['4!^2-3'])}, '2024-09-12': {'Tiles': ['0', '1', '8', '9'], 'Easy': (7, ['8-1']), 'Medium': (99, ['98+1', '1+98', '8+91', '91+8']), 'Hard': (182, ['190-8']), 'Extra': (892, ['0!+891', '891+0!'])}}
    
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
        request.session['hints'] = ['-1','-1','-1','-1']

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
    elif current_difficulty == 'Extra':
        request.session['hints'][3]= hint_level

    # Update the difficulty level for the next puzzle
    if current_difficulty == 'Easy':
        request.session['difficulty'] = 'Medium'
    elif current_difficulty == 'Medium':
        request.session['difficulty'] = 'Hard'
    elif current_difficulty == 'Hard':
        if request.session['hints'][0:2]==['0','0','0']:
            request.session['difficulty'] = 'Extra'
        else:
            request.session['difficulty'] = 'Completed'
    elif current_difficulty == 'Extra':
        request.session['difficulty'] = 'Completed'
    
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
            result = None
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
    
    if hints_message[3]:
        html_message = f'Sumfing #{game_no}\n\nEasy: {hints_message[0]}\nMedium: {hints_message[1]}\nHard: {hints_message[2]}\nExtra🤓: {hints_message[3]}'
        whatsapp_message = f'Sumfing #{game_no}\nEasy: {hints_message[0]}\nMedium: {hints_message[1]}\nHard: {hints_message[2]}\nExtra🤓: {hints_message[3]}\nPlay at sumfing.com'
    else:
        html_message = f'Sumfing #{game_no}\n\nEasy: {hints_message[0]}\nMedium: {hints_message[1]}\nHard: {hints_message[2]}\n'
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

