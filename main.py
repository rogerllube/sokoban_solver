from pynput import keyboard
import os

pressed_key = []
player_pos = []
map_size = 0

def on_press(key):
    if key == keyboard.Key.esc:
        return False
    try:
        k = key.char
    except:
        k = key.name
    if k in["left", "right", "up", "down"]:
        pressed_key.append(k)
        return False

def print_map(game_map):
    symbol_dict = {
        "b": "📦",
        "w": "⬛",
        "g": "🔘",
        "p": "🧔",
        0: "⬜",
        "s": "☑️",
        "t": "🧔"
    }
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(0, len(game_map)):
        for j in range(0, len(game_map)):
            print(symbol_dict[game_map[i][j]], end="")
        print()

def fill_map(game_map, type):

    if type == "wall":
        character = "w"
    elif type == "goal":
        character = "g"
    elif type == "box":
        character = "b"
    elif type == "player":
        character = "p"

    while True:
        print_map(game_map)
        if type == "wall":
            position = input("Digite uma posiçao para posicionar uma parede no formato <x,y> ou digite qualquer coisa que nao seja um numero para ir ao proximo passo: ")
        elif type == "goal":
            position = input("Digite uma posiçao para posicionar um botao no formato <x,y> ou digite qualquer coisa que nao seja um numero para ir ao proximo passo: ")
        elif type == "box":
            position = input("Digite uma posiçao para posicionar uma caixa no formato <x,y> ou digite qualquer coisa que nao seja um numero para ir ao proximo passo: ")
        elif type == "player":
            position = input("Digite uma posiçao para posicionar um jogador no formato <x,y> ou digite qualquer coisa que nao seja um numero para ir ao proximo passo: ")

        if not position[0].isdigit():
            break
        position = position.split(",")
        if int(position[0]) < 0 or int(position[0]) >= map_size or int(position[1]) < 0 or int(position[1]) >= map_size:
            continue
        if game_map[int(position[0])][int(position[1])] == 0:
            game_map[int(position[0])][int(position[1])] = character
            if type == "player":
                player_pos.append(int(position[0]))
                player_pos.append(int(position[1]))
                return

def move_player(game_map, k):
    new_ppos = []
    global player_pos
    if k == "up":
        new_ppos.append(player_pos[0] - 1)
        new_ppos.append(player_pos[1])
    elif k == "down":
        new_ppos.append(player_pos[0] + 1)
        new_ppos.append(player_pos[1])
    elif k == "left":
        new_ppos.append(player_pos[0])
        new_ppos.append(player_pos[1] - 1)
    elif k == "right":
        new_ppos.append(player_pos[0])
        new_ppos.append(player_pos[1] + 1)

    if new_ppos[0] < 0 or new_ppos[0] >= map_size or new_ppos[1] < 0 or new_ppos[1] >= map_size:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_map(game_map)
        print("Movimento Invalido")
        return

    if game_map[new_ppos[0]][new_ppos[1]] == 0:
        game_map[new_ppos[0]][new_ppos[1]] = 'p'
        game_map[player_pos[0]][player_pos[1]] = 0 if game_map[player_pos[0]][player_pos[1]] == 'p' else 'g'
        player_pos = new_ppos

    elif game_map[new_ppos[0]][new_ppos[1]] == 'g':
        game_map[new_ppos[0]][new_ppos[1]] = 't'
        game_map[player_pos[0]][player_pos[1]] = 0 if game_map[player_pos[0]][player_pos[1]] == 'p' else 'g'
        player_pos = new_ppos

    if game_map[new_ppos[0]][new_ppos[1]] == 'b' or game_map[new_ppos[0]][new_ppos[1]] == 's':
        new_bpos = []
        if k == "up":
            new_bpos.append(new_ppos[0] - 1)
            new_bpos.append(new_ppos[1])
        elif k == "down":
            new_bpos.append(new_ppos[0] + 1)
            new_bpos.append(new_ppos[1])
        elif k == "left":
            new_bpos.append(new_ppos[0])
            new_bpos.append(new_ppos[1] - 1)
        elif k == "right":
            new_bpos.append(new_ppos[0])
            new_bpos.append(new_ppos[1] + 1)

        if new_bpos[0] < 0 or new_bpos[0] >= map_size or new_bpos[1] < 0 or new_bpos[1] >= map_size:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_map(game_map)
            print("Movimento Invalido")
            return
        if game_map[new_bpos[0]][new_bpos[1]] == 0:
            game_map[new_ppos[0]][new_ppos[1]] = 'p'
            game_map[player_pos[0]][player_pos[1]] = 0 if game_map[player_pos[0]][player_pos[1]] == 'p' else 'g'
            game_map[new_bpos[0]][new_bpos[1]] = 'b'
            player_pos = new_ppos
        elif game_map[new_bpos[0]][new_bpos[1]] == 'g':
            game_map[new_ppos[0]][new_ppos[1]] = 'p'
            game_map[player_pos[0]][player_pos[1]] = 0 if game_map[player_pos[0]][player_pos[1]] == 'p' else 'g'
            game_map[new_bpos[0]][new_bpos[1]] = 's'
            player_pos = new_ppos

def check_win(game_map):
    for l in game_map:
        if 'g' in l or 't' in l:
            return False
    return True

def evaluate_cell(game_map, size, x, y):
    match game_map[y][x]:
        case 'g' | 'p' | 't':
            min_dist = float('inf')
            for i in range(size):
                for j in range(size):
                    dist = abs(i - y) + abs(j - x)
                    if game_map[i][j] == "b" and dist < min_dist:
                        min_dist = dist
            return min_dist
        case _:
            return 0

def evaluate_board(game_map, size):
    sum = 0
    for i in range(size):
        for j in range(size):
            sum += evaluate_cell(game_map, size, j, i)
    return sum

def run_game(game_map):
    while True:
        with keyboard.Listener(
                on_press=on_press) as listener:
            listener.join()
        if(len(pressed_key) > 0):
            k = pressed_key.pop(0)
            move_player(game_map, k)
            print_map(game_map)
            print("Heuristica do Board: " + str(evaluate_board(game_map, map_size)))
            win_flag = check_win(game_map)
        if win_flag:
            print("Parabens, voce resolveu o problema")
            return


if __name__ == '__main__':

    map_size = int(input("Digite o tamanho do mapa:"))
    game_map = []

    for i in range(0, map_size):
        game_map.append([])
        for j in range(0, map_size):
            game_map[i].append(0)

    fill_map(game_map, "wall")
    print_map(game_map)
    fill_map(game_map, "goal")
    print_map(game_map)
    fill_map(game_map, "box")
    print_map(game_map)
    fill_map(game_map, "player")
    print_map(game_map)

    gamemode = input("Digite 1 para resolver o mapa ou digite 2 para soluçao automatica: ")

    if gamemode == "1":
        run_game(game_map)
    #elif gamemode == 2:
        #run_bot(game_map)