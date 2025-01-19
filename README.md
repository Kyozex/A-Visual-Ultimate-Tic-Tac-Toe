# A-Visual-Ultimate-Tic-Tac-Toe
An easy-to-use visual Ultimate Tic-Tac-Toe game with customizable player names and colors / 一款易于使用的可视化终极井字游戏，具有可自定义的玩家名称和代表色

对py文件进入编辑界面后，需要修改的地方包括：

    characters = {

        'Player02': {'mark': '２', 'color': '#0000ff', 'full_name': 'Player02', 'class': 'b'},
    
        'Player01': {'mark': '１', 'color': '#ff0000', 'full_name': 'Player01', 'class': 'a'}
    
    }

请将“Player01/02”换成你需要的玩家名称，“mark”是在棋盘上的玩家标记，“color”是玩家代表色（请尽量选择深色！），“full_name”与玩家名称保持一致，“class”决定该玩家获胜的胜利宣言（其中“a”类型=“Player这老登赢了”，“b”类型=“恭喜Player胜利！！”）

另外让

    PLAYER_1_NAME = 'Player01'

    PLAYER_2_NAME = 'Player02'

中的“Player01/02”与上文保持一致^^
