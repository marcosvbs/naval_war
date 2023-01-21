import classes

game_controller = classes.GameController()
player = classes.Player()
game_controller.place_ships_on_board()

def main():

    print('')
    print('Bem vindo ao jogo batalha naval!')
    print(f'O objetivo do jogo é afundar os {len(game_controller.ships)} navios escondidos no tabuleiro, usando no maximo {player.bombs} bombas.')

    while player.bombs != 0:

        player.board.show_cells()

        print(f'Você possui {player.bombs} bombas restantes.')

        ships_left = game_controller.check_ships_left()
        print(f'{ships_left} navios restantes.')
        print('')

        print('Onde gostaria de jogar uma bomba...')
        print('')

        target_cell_row = game_controller.get_target_cell_row()
        target_cell_column = game_controller.get_target_cell_column()

        player.drop_bomb(game_controller.board, target_cell_row, target_cell_column)
    
        player.bombs -= 1
        game_controller.check_sunk_ships(player.board)

        for i in range(20):
            print('')

        

        if game_controller.check_if_player_wins(player.board):
            print('')
            print('Parabéns, você ganhou!')
            return True

    print('')
    print('Que pena, você perdeu.')
    return False

main()