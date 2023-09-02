import requests
import random
import data

url = 'https://pokeapi.co/api/v2/'

possible_pokemon = data.every_pokemon
for i in range(len(possible_pokemon)):
    possible_pokemon[i]['dex_num'] = i+1

possible_pokemon = possible_pokemon[:151]
gameover = False

guess = 'gyarados'
gen = 1
type1 ='water'
type2 ='flying'
height = 65
weight = 2350

def getgen(dex_num):
    if dex_num <= 151: return 1
    elif dex_num >151 and dex_num<=251: return 2
    elif dex_num > 251 and dex_num<=386: return 3
    elif dex_num >386 and dex_num<=493: return 4
    elif dex_num >493 and dex_num<=649: return 5
    elif dex_num >649 and dex_num<=721: return 6
    elif dex_num>721 and dex_num<=809: return 7
    elif dex_num>809 and dex_num<=905: return 8
    else: return 9

def gen_bounds(num):
    match num:
        case 1: return (1, 151)
        case 2: return (152, 251)
        case 3: return (252, 386)
        case 4: return (387, 493)
        case 5: return (494, 649)
        case 6: return (650, 721)
        case 7: return (722, 809)
        case 8: return (810, 905)
        case 9: return (906, 1008)

def addtype2(p):
    try:
        t2 = p['types'][1]
    except:
        p['types'].append({'slot':2, 'type':{'name':'none'}})

while not gameover:
    print(f'choose {guess}')
    correct = input('right or wrong')
    if correct == 'yes':
        gameover = True
    gen_guess = input('generation: lower, higher, or correct')
    if gen_guess == 'lower':
        for pokemon in possible_pokemon:
            if pokemon['dex_num'] >= gen_bounds(gen)[0]:
                possible_pokemon.remove(pokemon)
    elif gen_guess == 'higher':
        for pokemon in possible_pokemon:
            if pokemon['dex_num'] <= gen_bounds(gen)[1]:
                possible_pokemon.remove(pokemon)
    else:
        for pokemon in possible_pokemon:
            if pokemon['dex_num'] <= gen_bounds(gen)[0] or pokemon['dex_num'] >= gen_bounds(gen)[1]:
                possible_pokemon.remove(pokemon)
    type1_guess = input('type 1: correct, wrong, or wrong spot')
    if type1_guess == 'correct':
        for pokemon in possible_pokemon:
            rsp = requests.get(pokemon['url']).json()
            if rsp['types'][0]['type']['name'] != type1:
                possible_pokemon.remove(pokemon)
    elif type1_guess == 'wrong':
        for pokemon in possible_pokemon:
            rsp = requests.get(pokemon['url']).json()
            if rsp['types'][0]['type']['name'] == type1:
                possible_pokemon.remove(pokemon)
    elif type1_guess == 'wrong spot':
        for pokemon in possible_pokemon:
            rsp = requests.get(pokemon['url']).json()
            addtype2(rsp)
            if rsp['types'][1]['type']['name'] != type1:
                possible_pokemon.remove(pokemon)
    type2_guess = input('type 2:')
    if type2_guess == 'correct':
        for pokemon in possible_pokemon:
            rsp = requests.get(pokemon['url']).json()
            addtype2(rsp)
            if rsp['types'][1]['type']['name'] != type2:
                possible_pokemon.remove(pokemon)
    elif type2_guess == 'wrong':
        for pokemon in possible_pokemon:
            rsp = requests.get(pokemon['url']).json()
            addtype2(rsp)
            if rsp['types'][1]['type']['name'] == type2:
                possible_pokemon.remove(pokemon)
    elif type2_guess == 'wrong spot':
        for pokemon in possible_pokemon:
            rsp = requests.get(pokemon['url']).json()
            if rsp['types'][0]['type']['name'] != type2:
                possible_pokemon.remove(pokemon)

    height_guess = input('height: higher, lower, or right')
    if height_guess == 'higher':
        for pokemon in possible_pokemon:
            rsp = requests.get(pokemon['url']).json()
            if rsp['height'] <= height:
                possible_pokemon.remove(pokemon)
    elif height_guess == 'lower':
        for pokemon in possible_pokemon:
            rsp = requests.get(pokemon['url']).json()
            if rsp['height'] >= height:
                possible_pokemon.remove(pokemon)
    elif height_guess == 'right':
        for pokemon in possible_pokemon:
            rsp = requests.get(pokemon['url']).json()
            if rsp['height'] != height:
                possible_pokemon.remove(pokemon)
    weight_guess = input('weight:')
    if weight_guess == 'higher':
        for pokemon in possible_pokemon:
            rsp = requests.get(pokemon['url']).json()
            if rsp['weight'] <= weight:
                possible_pokemon.remove(pokemon)
    elif weight_guess == 'lower':
        for pokemon in possible_pokemon:
            rsp = requests.get(pokemon['url']).json()
            if rsp['weight'] >= weight:
                possible_pokemon.remove(pokemon)
    elif weight_guess == 'right':
        for pokemon in possible_pokemon:
            rsp = requests.get(pokemon['url']).json()
            if rsp['weight'] != weight:
                possible_pokemon.remove(pokemon)
    
    new_guess = random.choice(possible_pokemon)
    rsp = requests.get(new_guess['url']).json()
    addtype2(rsp)
    guess = new_guess['name']
    gen = getgen(new_guess['dex_num'])
    type1 = rsp['types'][0]['type']['name']
    type2 = rsp['types'][1]['type']['name']
    height = rsp['height']
    weight = rsp['weight']