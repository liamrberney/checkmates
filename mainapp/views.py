from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .forms import UserRegisterForm
from django.http import JsonResponse

import sqlite3
import os
import hashlib
import traceback
import json
import requests
import math

from .forms import NameForm
from .models import Greeting


# use this function to execute arbtrary sql commands
# returns the result as an array of tuples
def sql_exec(query):
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    data = cur.fetchall()
    con.close()
    return data

# this function generates an md5 hash of a string
# returns a string


def checkMatch(user1, user2):
    query = "SELECT "+user1+" FROM friends WHERE "+user1+" = " + \
        "'"+user2+"'"
    # print(str(sql_exec(query)))
    # print(bool(sql_exec(query)))
    return (bool(sql_exec(query)))


def hash(string):
    return str(hashlib.md5(string.encode()).digest()).replace("'", "")

# insert values into table
# values is an array


def sql_insert(table_name, values):
    query = "insert into "+table_name+" values("
    for i in range(len(values)):
        if type(values[i]) == str:
            query += "'"+values[i]+"'"
        else:
            query += values[i]
        if i != len(values)-1:
            query += ","
    query += ")"
    print("query", query)
    sql_exec(query)

# this function replaces value of specific column where row=id with another column value
# use for updating bios, location, etc
# presumes primary key-value exists and that it is the first column


def update_table_vals(table_name, rowid, value, table_column):
    query = "UPDATE "+table_name+" SET "+table_column + " = '"+value + \
        "' WHERE "+sql_get_column_names(table_name)[0]+" ='"+rowid+"';"
    sql_exec(query)


def get_id(table_name, user_or_game):
    query = "SELECT rowid FROM "+table_name+" WHERE " + \
        sql_get_column_names(table_name)[1]+" = '"+user_or_game+"';"
    data = sql_exec(query)
    return str(data[0][0])
    # print(data)

# this function adds user matches to the "friends" table
# if user is not on the table, the database appends a new column


def swipe_queue(username):
    sql_file = open("sort.sql")
    queue = sql_file.read()
    queue = queue.replace("~", username)
    data = sql_exec(queue)
    # print(data)
    return data


# this function adds user matches to the "open games" table
# if user is not on the table, the database appends a new column
def add_open(username, match_username):
    try:
        sql_file = open("new_games.sql")
        query = sql_file.read().split(';')
        for q in query:
            q = q.replace("?", match_username)
            q = q.replace("~", username)
            sql_exec(q)
    except:
        print(traceback.format_exc())

# this function adds user matches to the "friends" table
# if user is not on the table, the database appends a new column


def add_match(username, match_username):
    try:
        sql_file = open("new_friend.sql")
        query = sql_file.read().split(';')
        for q in query:
            q = q.replace("?", match_username)
            q = q.replace("~", username)
            sql_exec(q)
    except:
        print(traceback.format_exc())


def add_swipe(username, match_username):
    try:
        sql_file = open("new_swipe.sql")
        query = sql_file.read().split(';')
        for q in query:
            q = q.replace("?", match_username)
            q = q.replace("~", username)
            sql_exec(q)
    except:
        print(traceback.format_exc())

# this function adds user matches to the "history" table
# if user is not on the table, the database appends a new column


def add_history(user1, user2, user1Score, user2Score):
    try:
        sql_file = open("new_history.sql")
        query = sql_file.read().split(';')
        for q in query:
            q = q.replace("?", user2)
            q = q.replace("%", user1Score)
            q = q.replace("&", user2Score)
            q = q.replace("~", user1)
            sql_exec(q)
    except:
        print(traceback.format_exc())


# this function gets matchlist for user


def get_match(username):
    query = "SELECT "+username+" FROM friends WHERE friends."+username+" IS NOT NULL"
    data = sql_exec(query)
    return str(data[0])


def get_history(username):
    query = "SELECT "+username+" FROM history WHERE history."+username+" IS NOT NULL"
    data = sql_exec(query)
    return data


def sql_get_column_names(table_name):
    query = "pragma table_info("+table_name+")"
    data = sql_exec(query)
    names = []
    for d in data:
        names.append(d[1])
    return names


def sql_table2html(table_name):
    query = "select * from "+table_name
    data = sql_exec(query)
    html = "<p><b>"+table_name+"</b></p>"
    html += "<p>"
    names = sql_get_column_names(table_name)
    for n in names:
        html += n+" "
    html += "</p>"
    for d in data:
        html += "<p>"+str(d)+"</p>"
    return html


def index(request):
    return render(request, "index.html")


def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})


def handle_uploaded_file(f):
    #print("handling file")
    with open('media/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def home(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            ELO = 1200
            handle_uploaded_file(request.FILES["profile_picture"])
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            name = first_name + " " + last_name
            fs = FileSystemStorage()
            uploaded_file_url = fs.url((request.FILES["profile_picture"]).name)
            pwhash = password  # hash(password)
            sql_insert("users (username, name, pwhash, img_url, lat, lon, bios, phone,email)", [
                       username, name, pwhash, uploaded_file_url, "NONE", "NONE", "", phone, email])
            query = "ALTER TABLE friends ADD COLUMN "+username+";"
            sql_exec(query)
            query = "ALTER TABLE history ADD COLUMN "+username+";"
            sql_exec(query)
            query = "ALTER TABLE games ADD COLUMN "+username+";"
            sql_exec(query)
            query = "ALTER TABLE swipe ADD COLUMN "+username+";"
            sql_exec(query)
            #query = "SELECT IIF ((SELECT COUNT(*) AS CNTREC FROM pragma_table_info('friends') WHERE name='"+username+"') > 0, 1, 0);"
            # data=sql_exec(query)
            #print(data[0][0] != 0)
            return redirect('main')
        else:
            print("Invalid form")
    else:
        form = UserRegisterForm()
    return render(request, 'checkmates/register.html', {'form': form})


@csrf_exempt
def register(request):
    print("register")
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        password = request.POST.get("password")
        passwordCon = request.POST.get("passwordCon")
        imagename = request.POST.get("image")
        file = request.FILES["image"]
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        pwhash = password  # hash(password)
        sql_insert("users", [username, name, pwhash, uploaded_file_url])
    return HttpResponseRedirect("/")


@csrf_exempt
def login(request):
    # print('login123')
    if request.method == "POST":
        username = str(request.POST.get("loginemail"))
        pw = str(request.POST.get("loginPassword"))
        query1 = "insert into login_attempts values('"+username+"','"+pw+"')"
        sql_exec(query1)
        pwhash = pw  # hash(pw)
        query2 = "select * from users where username='"+username+"' and "
        query2 += "pwhash='"+pwhash+"'"
        data = sql_exec(query2)
        if len(data) == 0:
            # ("invalid username or password")
            return HttpResponseRedirect("/?invalid_login=true")
        else:
            return HttpResponseRedirect("/main/")
    return HttpResponse("login")


def dbdump(request):
    print('dbdump')
    tables = ["login_attempts", "users", "friends",
              "variants", "auth_user", "history", "games", "swipe"]
    html = ""
    for t in tables:
        html += sql_table2html(t)

    return HttpResponse(html)

# don't look at this


@csrf_exempt
def saveprofile(request):
    if(request.user.username == ""):
        return HttpResponseRedirect("/register/")
    print("saving profile edits...")
    # if request.method == "POST":
    user = str(request.user)
    imageurl = json.load(request)['imageurl']
    #print("imageurl: " + imageurl)

    # print(findProfilePic(user))
    phonenumber = str(request.GET.get("phonenumber"))
    bio = str(request.GET.get("bio"))
    name = str(request.GET.get("fullname"))
    email = str(request.GET.get("email"))
    # liked_user = str(request.GET.get("username"))
    #print(name + bio + email + phonenumber)
    update_table_vals("users", get_id(
        "users", str(request.user)), name, "name")
    update_table_vals("users", get_id(
        "users", str(request.user)), bio, "bios")
    update_table_vals("users", get_id(
        "users", str(request.user)), phonenumber, "phone")
    update_table_vals("users", get_id(
        "users", str(request.user)), email, "email")
    update_table_vals("users", get_id(
        "users", str(request.user)), imageurl, "img_url")
    userelo = findELO(user)
    userimg = findProfilePic(user)
    return HttpResponseRedirect("/editprofile/")


def getfeed(request):
    res = swipe_queue(str(request.user))
    data = json.dumps({"array": res})
    return HttpResponse(data)


def like(request):
    # if request.method == "POST":
    user = str(request.user)
    liked_user = str(request.GET.get("username"))
    # print(liked_user)
    add_swipe(user, liked_user)
    add_match(user, liked_user)
    #print (checkMatch(user, liked_user) and checkMatch(liked_user, user))
    if (checkMatch(user, liked_user) and checkMatch(liked_user, user)):
        add_open(user, liked_user)
        add_open(liked_user, user)
    return HttpResponse(user+" liked "+liked_user)


def dislike(request):
    print("dislike")
    # if request.method == "POST":
    user = str(request.user)
    liked_user = str(request.GET.get("username"))
    add_swipe(user, liked_user)
    return HttpResponse(user+" disliked "+liked_user)


def main(request):
    print('main')
    if(request.user.username == ""):
        return HttpResponseRedirect("/register/")
    if request.method == "POST":
        location = str(request.POST.get("lat-long"))
        coordinates = location.split(",")
        update_table_vals("users", get_id(
            "users", str(request.user)), coordinates[0], "lat")
        update_table_vals("users", get_id(
            "users", str(request.user)), coordinates[1], "lon")
        print(coordinates[0], coordinates[1])
        return HttpResponseRedirect("/main/")
    return render(request, 'checkmates/main.html', context={"user": request.user})


def profile(request):
    print('profile')
    return render(request, 'checkmates/profile.html')


def findProfilePic(username):
    query = "select img_url from users where username='" + username + "'"
    print(query)
    data = sql_exec(query)
    return str(data[0][0])


def findELO(username):
    query = "select ELO from users where username='" + username + "'"
    print(query)
    data = sql_exec(query)
    return str(data[0][0])


def findNumGames(username):
    query = "select total from users where username='" + username + "'"
    print(query)
    data = sql_exec(query)
    return str(data[0][0])


def setNone(table, user, userOpp):
    query = "UPDATE games SET " + user + " = NULL WHERE "+user+" ='"+userOpp+"';"
    sql_exec(query)


def editprofile(request):
    print('editprofile')
    username = request.user.username
    if(request.user.username == ""):
        return HttpResponseRedirect("/register/")
    if request.method == 'POST' and 'lichess' in request.POST:
        #from ChessAPI import getLichessELO

        ELO = getLichessELO(request.POST['LUsername'], username)
        if(ELO != None):
            #print('Hey I made it with ELO' + str(ELO))
            updateELO(username, ELO)

    if request.method == 'POST' and 'chesscom' in request.POST:
        #from ChessAPI import getLichessELO

        ELO = getChessDotComELO(request.POST['CUsername'], username)
        if(ELO != None):
            updateELO(username, ELO)
    if request.method == 'POST' and 'chesscomPic' in request.POST:
        #from ChessAPI import getLichessELO

        img = getChessDotComPic(request.POST['CUsername'])
        UpdateProfPic(username, img)

    userELO = findELO(username)
    if(userELO == 'None'):
        userELO = 1200
    img = findProfilePic(username)
    email = findEmail(username)
    phone = findPhone(username)
    bio = findBio(username)
    fullname = findName(username)
    print("This is the bio we are editing: " + bio)
    return render(request, 'checkmates/editprofile.html', context={"pic": img, "name": fullname, "user": request.user, "bio": bio, "ELO": userELO, "phone": phone, "email": email})


def findPhone(username):
    query = "select phone from users where username='" + username + "'"
    print(query)
    data = sql_exec(query)
    return str(data[0][0])


def findBio(username):
    query = "select bios from users where username='" + username + "'"
    print(query)
    data = sql_exec(query)
    return str(data[0][0])


def findEmail(username):
    query = "select email from users where username='" + username + "'"
    print(query)
    data = sql_exec(query)
    return str(data[0][0])


def findName(username):
    query = "select name from users where username='" + username + "'"
    print(query)
    data = sql_exec(query)
    return str(data[0][0])


def matchhistory(request):
    if(request.user.username == ""):
        return HttpResponseRedirect("/register/")
    print('matchhistory')
    data = get_history(str(request.user))
    print(data)
    info = []
    for i in data:
        for j in i:
            component = (j.split(","))
            result = component[0]
            username = component[1]
            img_url = findProfilePic(username)
            temp = [username, img_url, result]
            info.append(temp)
    info = info[::-1]

    # ["w","aa","l"]
    return render(request, 'checkmates/matchhistory.html', context={"history": info})


def getGameStatus(currUser, oppUser):
    query = "SELECT "+currUser+" FROM history WHERE "+currUser+" == 'W,"+oppUser+",L';"
    data = sql_exec(query)

    query = "SELECT "+currUser+" FROM history WHERE "+currUser+" == 'L,"+oppUser+",W';"
    data2 = sql_exec(query)

    query = "SELECT "+currUser+" FROM history WHERE "+currUser+" == 'D,"+oppUser+",D';"
    data3 = sql_exec(query)
    return (data == None & data2 == None & data3 == None)


def get_games(username):
    query = "SELECT "+username+" FROM games WHERE games."+username+" IS NOT NULL"
    data = sql_exec(query)
    print(data)
    if(data == []):
        return
    return data[0]


def opengames(request):
    if(request.user.username == ""):
        return HttpResponseRedirect("/register/")
    print('opengames')
    info = (get_games(str(request.user)))
    games = []
    if(info != None):
        for i in info:
            temp = []
            uName = i
            img = findProfilePic(uName)
            email = findEmail(uName)
            phone = findPhone(uName)
            temp = [str(uName), str(img), str(email), str(phone)]
            games.append(temp)

    print(games)
    # games = [['AA', '/media/A.jpg', "AA@gmail.com", "123-456-7899", True],
    #          ["BB", '/media/B.png', "BB@gmail.com", "987-654-3211", False]]
    if request.method == 'POST' and "WonButton" in request.POST:
        print("Wonbutton")
        add_history(str(request.user), str(
            request.POST['opponentUsername']), "W", "L")
        calculateELO(str(request.user), str(
            request.POST['opponentUsername']), 1)
        setNone("games", str(request.user), str(
            request.POST['opponentUsername']))
        return HttpResponseRedirect("/opengames/")
    elif request.method == 'POST' and "DrewButton" in request.POST:
        print("Drawbutton")
        add_history(str(request.user), str(
            request.POST['opponentUsername']), "D", "D")
        calculateELO(str(request.user), str(
            request.POST['opponentUsername']), 0.5)
        setNone("games", str(request.user), str(
            request.POST['opponentUsername']))
        return HttpResponseRedirect("/opengames/")
    elif request.method == 'POST' and "LostButton" in request.POST:
        print("Lostbutton")
        add_history(str(request.user), str(
            request.POST['opponentUsername']), "L", "W")
        calculateELO(str(request.user), str(
            request.POST['opponentUsername']), 0)
        setNone("games", str(request.user), str(
            request.POST['opponentUsername']))
        return HttpResponseRedirect("/opengames/")
    # if request.method == 'POST':
    #     print("is a post")
    #     games = [["AA", '/media/A.jpg', "AA@gmail.com", "123-456-7899", getGameStatus(str(request.user), str(request.POST['opponentUsername']))],
    #              ["BB", '/media/B.png', "BB@gmail.com", "987-654-3211", getGameStatus(str(request.user), str(request.POST['opponentUsername']))]]
    #     print(getGameStatus(str(request.user), str(
    #         request.POST['opponentUsername'])))
    return render(request, 'checkmates/opengames.html', context={"games": games})


def gamepreferences(request):
    if(request.user.username == ""):
        return HttpResponseRedirect("/register/")
    if request.method == "POST":
        #print("Abort me")
        TimePreferences = request.POST.get("TimePreferences", None)
        ChessVariant = request.POST.get("ChessVariant", None)

        time = "None"
        if (TimePreferences == "Blitz"):
            time = "5"
        elif (TimePreferences == "Classical"):
            time = "30"
        elif (TimePreferences == "Rapid"):
            time = "15"
        elif (TimePreferences == "Unlimited"):
            time = "None"

        print("time: " + time)
        update_table_vals("users", get_id(
            "users", str(request.user)), ChessVariant, "variant")
        update_table_vals("users", get_id(
            "users", str(request.user)), time, "time_control")
        print(TimePreferences)
        print(ChessVariant)
        # if display_type in ["locationbox", "displaybox"]:

    query = "select variant from users where username= '" + \
        str(request.user) + "'"
    variant = sql_exec(query)[0][0]

    query = "select time_control from users where username= '" + \
        str(request.user) + "'"
    timecontrolint = sql_exec(query)[0][0]

    timecontrol = "Unlimited"
    if (timecontrolint == None):
        timecontrol = "Unlimited"
    elif (timecontrolint == 5):
        timecontrol = "Blitz"
    elif (timecontrolint == 30):
        timecontrol = "Classical"
    elif (timecontrolint == 15):
        timecontrol = "Rapid"

    return render(request, 'checkmates/gamepreferences.html', context={"ChessVariant": variant, "TimePreferences": timecontrol})


def event(request):
    context = {}
    fname = request.POST.get('fname', None)
    context['fname'] = fname
    return render(request, 'checkmates/event.html', context)


def info(request):
    return render(request, 'checkmates/info.html')


def TOS(request):
    print('TOS')
    return render(request, 'checkmates/tos.html')


def privacy(request):
    print('Privacy')
    return render(request, 'checkmates/privacy.html')


def cookies(request):
    print('Cookies')
    return render(request, 'checkmates/cookies.html')


# Takes in a username and outputs a tuple (ELO Type, Max ELO)


def getLichessELO(username, checkmatesName):
    # default ELO
    ELO = 1200
    url = 'https://lichess.org/api/user/' + username
    response = requests.get(url)
    status = response.status_code
    if(status != 200):
        print('Error ' + str(status))
        return
    data = response.text
    parse_json = json.loads(data)

    # Takes ratings into account only if they have a game played
    blitz = 0
    bullet = 0
    correspondence = 0
    classical = 0

    if(parse_json['perfs']['blitz']['games'] > 0):
        blitz = parse_json['perfs']['blitz']['rating']

    if(parse_json['perfs']['bullet']['games'] > 0):
        bullet = parse_json['perfs']['bullet']['rating']

    if(parse_json['perfs']['correspondence']['games'] > 0):
        correspondence = parse_json['perfs']['correspondence']['rating']

    if(parse_json['perfs']['classical']['games'] > 0):
        classical = parse_json['perfs']['classical']['rating']

    dict = {blitz: 'blitz',
            bullet: 'bullet',
            correspondence: 'correspondence',
            classical: 'classical'}

    ELO = max(blitz, bullet, correspondence, classical)
    eloType = dict[ELO]

    updateNumGames(checkmatesName, parse_json['perfs'][eloType]['games'])

    return ELO


# Takes in a username and outputs a tuple (ELO Type, Max ELO)
def getChessDotComELO(username, checkmatesName):
    # default ELO
    ELO = 1200
    url = 'https://api.chess.com/pub/player/' + username + '/stats/'

    response = requests.get(url)
    status = response.status_code
    if(status != 200):
        print('Error ' + str(status))
        return

    data = response.text
    parse_json = json.loads(data)

    # Takes the FIDE rating if it exists over everything else
    fide = parse_json['fide']
    if(fide > 0):
        return ('fide', fide)

    # only take ratings into account if they have won a game
    daily = 0
    rapid = 0
    bullet = 0
    blitz = 0
    if(parse_json['chess_daily']['record']['win'] > 0):
        daily = parse_json['chess_daily']['last']['rating']
    if(parse_json['chess_rapid']['record']['win'] > 0):
        rapid = parse_json['chess_rapid']['last']['rating']
    if(parse_json['chess_bullet']['record']['win'] > 0):
        bullet = parse_json['chess_bullet']['last']['rating']
    if(parse_json['chess_blitz']['record']['win'] > 0):
        blitz = parse_json['chess_blitz']['last']['rating']

    print(daily, rapid, bullet, blitz, fide)
    dict = {
        daily: 'chess_daily',
        rapid: 'chess_rapid',
        bullet: 'chess_bullet',
        blitz: 'chess_blitz'
    }

    ELO = max(daily, rapid, bullet, blitz)
    eloType = dict[ELO]
    updateNumGames(checkmatesName, parse_json[eloType]['record']
                   ['win'] + parse_json[eloType]['record']['loss']
                   + parse_json[eloType]['record']['draw'])

    return ELO


def getChessDotComPic(username):
    url = 'https://api.chess.com/pub/player/' + username

    response = requests.get(url)
    status = response.status_code
    if(status != 200):
        print('Error ' + status)
        return

    data = response.text
    parse_json = json.loads(data)

    return parse_json['avatar']


# username is checkmates username
def updateELO(username, ELO):
    rowid = get_id('users', username)

    update_table_vals('users', rowid, str(ELO), 'ELO')

# username is checkmates username


def UpdateProfPic(username, imgLink):
    rowid = get_id('users', username)
    update_table_vals('users', str(rowid), str(imgLink), 'img_url')


def updateNumGames(username, total):
    rowid = get_id('users', username)
    update_table_vals('users', str(rowid), str(total), 'total')


# result == 1 | user1 wins
# result == 0 | user2 wins
# result == .5 | draw
# calulates and updates ELO based on results of game
def calculateELO(username1, username2, result):
    if(result != 0 and result != .5 and result != 1):
        print("INALID RESULT: " + result)
        return
    numGames1 = int(findNumGames(username1))
    numGames2 = int(findNumGames(username2))

    ELO1 = int(math.floor(float(findELO(username1))))
    ELO2 = int(math.floor(float(findELO(username2))))

    if(numGames1 <= 30):
        K1 = 40
    elif (ELO1 >= 2400):
        K1 = 10
    else:
        K1 = 20

    if(numGames2 <= 30):
        K2 = 40
    elif (ELO2 >= 2400):
        K2 = 10
    else:
        K2 = 20

    prob1 = probOfWin(ELO1, ELO2)
    #prob2 = probOfWin(ELO2, ELO1)

    newELO1 = int(math.floor(ELO1 + K1 * (result - prob1)))

    result = 1 - result

    #newELO2 = ELO2 + K2 * (result - prob2)

    updateELO(username1, newELO1)
    #updateELO(username2, newELO2)

    return


def probOfWin(ELO1, ELO2):
    return 1.0 * 1.0 / (1 + 1.0 * pow(10, 1.0 * (ELO1 - ELO2) / 400))
