import requests
import json
import tweepy


user = 'TatumanChess'

# Takes in a username and outputs a tuple (ELO Type, Max ELO)


def getLichessELO(username):
    # default ELO
    ELO = 1000
    url = 'https://lichess.org/api/user/' + username
    response = requests.get(url)
    status = response.status_code
    if(status != 200):
        print('Error ' + status)
        return
    data = response.text
    parse_json = json.loads(data)

    # Takes ratings into account only if they have a game played
    blitz, bullet, correspondence, classical = 0

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
    return (eloType, ELO)

# Takes in a username and outputs a tuple (ELO Type, Max ELO)


def getChessDotComELO(username):
    # default ELO
    ELO = 1000
    url = 'https://api.chess.com/pub/player/' + username + '/stats/'

    response = requests.get(url)
    status = response.status_code
    if(status != 200):
        print('Error ' + status)
        return

    data = response.text
    parse_json = json.loads(data)

    # Takes the FIDE rating if it exists over everything else
    fide = parse_json['fide']
    if(fide > 0):
        return ('fide', fide)

    # only take ratings into account if they have won a game
    daily, rapid, bullet, blitz = 0
    if(parse_json['chess_daily']['record']['win'] > 0):
        daily = parse_json['chess_daily']['last']['rating']
    if(parse_json['chess_rapid']['record']['win'] > 0):
        rapid = parse_json['chess_rapid']['last']['rating']
    if(parse_json['chess_bullet']['record']['win'] > 0):
        bullet = parse_json['chess_bullet']['last']['rating']
    if(parse_json['chess_daily']['record']['win'] > 0):
        blitz = parse_json['chess_blitz']['last']['rating']

    print(daily, rapid, bullet, blitz, fide)
    dict = {
        daily: 'daily',
        rapid: 'rapid',
        bullet: 'bullet',
        blitz: 'blitz'
    }

    ELO = max(daily, rapid, bullet, blitz)
    ELOType = dict[ELO]

    return (ELOType, ELO)


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
    update_table_vals('users', rowid, ELO, 'ELO')

# username is checkmates username
def UpdateProfPic(username, imgLink):
    rowid = get_id('users', username)
    update_table_vals('users', rowid, imgLink, 'img_url')


def main():
    print('Starting')


if __name__ == '__main__':
    main()
