import tkinter as tk
from tkinter import ttk
import numpy as np
from tkinter import font

characters = {
    'Player02': {'mark': '２', 'color': '#0000ff', 'full_name': 'Player02', 'class': 'b'},
    'Player01': {'mark': '１', 'color': '#ff0000', 'full_name': 'Player01', 'class': 'a'}
}

PLAYER_1_NAME = 'Player01'
PLAYER_2_NAME = 'Player02'

next_board = None

current_player = characters[PLAYER_1_NAME]['mark']
current_color = characters[PLAYER_1_NAME]['color']

end_game_player = current_player

def game_over(winner):
    global B, b1, b2, b3
    for i in range(9):
        for j in range(9):
            B[i][j]['state'] = 'disabled'
            B[i][j]['cursor'] = 'arrow'

    try:
        winner_class = characters[winner]['class']
        if winner_class == 'a':
            b2['text'] = f'{characters[winner]["full_name"]}这老登赢了'
        else:
            b2['text'] = f'恭喜{characters[winner]["full_name"]}胜利！！'
    except:
        b2['text'] = '和棋'
        
    b2['state'] = 'disabled'
    b2['cursor'] = 'arrow'
    b3['state'] = 'disabled'
    b3['cursor'] = 'arrow'

    b1['state'] = 'normal'
    b1['cursor'] = 'hand2'

def check_winner():
    global B, b1, b2, b3
    mark = []
    for i in range(9):
        mark.append([])
        for j in range(9):
            if B[i][j]['text'] == characters[PLAYER_2_NAME]['mark']:
                mark[i].append(1)
            elif B[i][j]['text'] == characters[PLAYER_1_NAME]['mark']:
                mark[i].append(-1)
            else:
                mark[i].append(0)
    mark = np.array(mark)
    
    for i in range(9):
        if abs(sum(mark[i])) == 9:
            mark_small_board_as_used(i // 3, i % 3, current_player, current_color)
            game_over(PLAYER_2_NAME if sum(mark[i]) == 9 else PLAYER_1_NAME)
            return True
    for j in range(9):
        if abs(mark.sum(axis=0)[j]) == 9:
            mark_small_board_as_used(j // 3, j % 3, current_player, current_color)
            game_over(PLAYER_2_NAME if mark.sum(axis=0)[j] == 9 else PLAYER_1_NAME)
            return True
    if abs(mark.trace(1)) == 9:
        mark_small_board_as_used(0, 0, current_player, current_color)
        game_over(PLAYER_2_NAME if mark.trace(1) == 9 else PLAYER_1_NAME)
        return True
    if abs(mark.trace(-1)) == 9:
        mark_small_board_as_used(0, 2, current_player, current_color)
        game_over(PLAYER_2_NAME if mark.trace(-1) == 9 else PLAYER_1_NAME)
        return True
    
    if not (0 in mark):
        game_over('draw')
        return True
    return False

def mark_small_board_as_used(x, y, player_mark, player_color):
    global B, main_window, canvas, small_board_status

    small_board_status[x][y] = player_mark

    x1 = y * 3 * 70 + 2
    y1 = x * 3 * 70 + 2
    x2 = x1 + 3 * 70
    y2 = y1 + 3 * 70

    overlay_canvas = tk.Canvas(main_window, width=x2 - x1, height=y2 - y1, highlightthickness=0)
    overlay_canvas.place(x=x1, y=y1)

    overlay_canvas.create_rectangle(0, 0, x2 - x1, y2 - y1, fill='lightgrey', outline='black', width=2)

    overlay_canvas.create_text((x2 - x1) // 2, (y2 - y1) // 2, text=player_mark, font=large_font, fill=player_color)

    for i in range(x * 3, (x + 1) * 3):
        for j in range(y * 3, (y + 1) * 3):
            B[i][j]['state'] = 'disabled'

    check_global_winner()

small_board_status = [[None for _ in range(3)] for _ in range(3)]

def check_global_winner():
    global small_board_status

    for row in small_board_status:
        if len(set(row)) == 1 and row[0] is not None:
            game_over(PLAYER_2_NAME if row[0] == characters[PLAYER_2_NAME]['mark'] else PLAYER_1_NAME)
            return

    for col in range(3):
        column = [small_board_status[row][col] for row in range(3)]
        if len(set(column)) == 1 and column[0] is not None:
            game_over(PLAYER_2_NAME if column[0] == characters[PLAYER_2_NAME]['mark'] else PLAYER_1_NAME)
            return

    if len(set([small_board_status[i][i] for i in range(3)])) == 1 and small_board_status[0][0] is not None:
        game_over(PLAYER_2_NAME if small_board_status[0][0] == characters[PLAYER_2_NAME]['mark'] else PLAYER_1_NAME)
        return

    if len(set([small_board_status[i][2 - i] for i in range(3)])) == 1 and small_board_status[0][2] is not None:
        game_over(PLAYER_2_NAME if small_board_status[0][2] == characters[PLAYER_2_NAME]['mark'] else PLAYER_1_NAME)
        return

def check_small_board_winner(board_section):
    start_row, start_col = board_section[0] * 3, board_section[1] * 3
    marks = [B[i][j]['text'] for i in range(start_row, start_row + 3) for j in range(start_col, start_col + 3)]
    
    marks_2d = np.array(marks).reshape(3, 3)
    
    for row in marks_2d:
        if len(set(row)) == 1 and row[0] != '':
            return True
    
    for col in marks_2d.T:
        if len(set(col)) == 1 and col[0] != '':
            return True
    
    if len(set([marks_2d[i][i] for i in range(3)])) == 1 and marks_2d[0][0] != '':
        return True
    if len(set([marks_2d[i][2-i] for i in range(3)])) == 1 and marks_2d[0][2] != '':
        return True
    
    return False

def place(Bu, i, j):
    global current_player, current_color, end_game_player, next_board

    if Bu['state'] == 'disabled' or Bu.cget('bg') == 'lightgrey':
        return

    if b2['text'] in [f'恭喜{characters[PLAYER_1_NAME]["full_name"]}胜利！！', 
                      f'让{characters[PLAYER_2_NAME]["full_name"]}这老登赢了', 
                      '和棋']:
        return

    board_section = (i // 3, j // 3)

    if check_small_board_winner(board_section) and (next_board != board_section):
        return

    Bu['text'] = current_player
    Bu['font'] = button_font
    Bu['state'] = 'disabled'
    Bu['cursor'] = 'arrow'
    Bu['foreground'] = current_color
    Bu['disabledforeground'] = current_color

    if check_small_board_winner(board_section):
        mark_small_board_as_used(board_section[0], board_section[1], current_player, current_color)

    if check_winner():
        end_game_player = current_player
        return

    next_board = (i % 3, j % 3)

    if check_small_board_winner(next_board):
        next_board = None

    current_player = characters[PLAYER_2_NAME]['mark'] if current_player == characters[PLAYER_1_NAME]['mark'] else characters[PLAYER_1_NAME]['mark']
    current_color = characters[PLAYER_2_NAME]['color'] if current_color == characters[PLAYER_1_NAME]['color'] else characters[PLAYER_1_NAME]['color']

    update_board_colors()

def update_board_colors():
    global next_board
    has_open_board = False
    
    if next_board is not None:
        if check_small_board_winner(next_board) or is_small_board_full(next_board):
            next_board = None
    
    for i in range(9):
        for j in range(9):
            board_section = (i // 3, j // 3)
            if check_small_board_winner(board_section) or is_small_board_full(board_section):
                B[i][j].config(bg='lightgrey')
            elif next_board is None or board_section == next_board:
                B[i][j].config(bg='#F0F0F0')
                if not check_small_board_winner(board_section) and not is_small_board_full(board_section):
                    has_open_board = True
            else:
                B[i][j].config(bg='lightgrey')
    
    if not has_open_board:
        game_over('draw')

def is_small_board_full(board_section):
    x, y = board_section
    for i in range(x * 3, (x + 1) * 3):
        for j in range(y * 3, (y + 1) * 3):
            if B[i][j]['text'] == "":
                return False
    return True

def restart():
    global b1, b2, b3, B, current_player, current_color, next_board, small_board_status

    small_board_status = [[None for _ in range(3)] for _ in range(3)]

    for widget in main_window.winfo_children():
        if isinstance(widget, tk.Canvas) and widget != canvas:
            widget.destroy()

    for i in range(9):
        for j in range(9):
            B[i][j]['text'] = ''
            B[i][j]['state'] = 'disabled'
            B[i][j]['cursor'] = 'arrow'
            B[i][j].config(bg='#F0F0F0')

    b1['state'] = 'disabled'
    b1['cursor'] = 'arrow'
    b2['text'] = '开始'
    b2['state'] = 'normal'
    b2['cursor'] = 'hand2'
    b3['state'] = 'normal'
    b3['cursor'] = 'hand2'

    if b3['text'] == f'{characters[PLAYER_1_NAME]["full_name"]}先手':
        current_player = characters[PLAYER_1_NAME]['mark']
        current_color = characters[PLAYER_1_NAME]['color']
    else:
        current_player = characters[PLAYER_2_NAME]['mark']
        current_color = characters[PLAYER_2_NAME]['color']

    next_board = None

    update_board_colors()

def switch_first_hand():
    global b3, current_player, current_color
    if b3['text'] == f'{characters[PLAYER_1_NAME]["full_name"]}先手':
        b3['text'] = f'{characters[PLAYER_2_NAME]["full_name"]}先手'
        current_player = characters[PLAYER_2_NAME]['mark']
        current_color = characters[PLAYER_2_NAME]['color']
    else:
        b3['text'] = f'{characters[PLAYER_1_NAME]["full_name"]}先手'
        current_player = characters[PLAYER_1_NAME]['mark']
        current_color = characters[PLAYER_1_NAME]['color']

def play():
    global b1, b2, b3, B, current_player, current_color, next_board

    for i in range(9):
        for j in range(9):
            B[i][j]['state'] = 'normal'
            B[i][j]['cursor'] = 'hand2'
            update_board_colors()

    b1['state'] = 'normal'
    b1['cursor'] = 'hand2'
    b2['state'] = 'disabled'
    b2['cursor'] = 'arrow'
    b3['state'] = 'disabled'
    b3['cursor'] = 'arrow'
    
    if b3['text'] == f'{characters[PLAYER_1_NAME]["full_name"]}先手':
        current_player = characters[PLAYER_1_NAME]['mark']
        current_color = characters[PLAYER_1_NAME]['color']
    else:
        current_player = characters[PLAYER_2_NAME]['mark']
        current_color = characters[PLAYER_2_NAME]['color']
    
    next_board = None

def draw_board_borders(canvas):
    for i in range(3):
        for j in range(3):
            x1 = j * 3 * 70+2
            y1 = i * 3 * 70+2
            x2 = x1 + 210
            y2 = y1 + 210
            canvas.create_rectangle(x1, y1, x2, y2, outline='black', width=2)

main_window = tk.Tk()
main_window.title("终极井字棋")

button_font = font.Font(size=15, weight='bold')
large_font = font.Font(size=30, weight='bold')

canvas = tk.Canvas(main_window, width=630, height=630)
canvas.grid(row=0, column=0, rowspan=9, columnspan=9, sticky=tk.N + tk.S + tk.W + tk.E)
draw_board_borders(canvas)

B = []
for i in range(9):
    B.append([])
    for j in range(9):
        Bu = tk.Button(main_window, text="", width=4, height=2, font=button_font,
                       state='disabled',
                       cursor='arrow',
                       command=lambda i=i, j=j: place(B[i][j], i, j))
        Bu.grid(row=i, column=j, padx=0, pady=0)
        B[i].append(Bu)

b1 = tk.Button(main_window, text="重玩", command=restart, font=button_font)
b1.grid(row=9, column=0, columnspan=3, sticky=tk.W + tk.E)

b2 = tk.Button(main_window, text="开始", command=play, font=button_font)
b2.grid(row=9, column=3, columnspan=3, sticky=tk.W + tk.E)

b3 = tk.Button(main_window, text=f'{characters[PLAYER_1_NAME]["full_name"]}先手', command=switch_first_hand, font=button_font)
b3.grid(row=9, column=6, columnspan=3, sticky=tk.W + tk.E)

b1['state'] = 'disabled'
b1['cursor'] = 'arrow'
main_window.mainloop()