from run.game_runner import GameRunner

if __name__ == '__main__':
    game_runner = GameRunner()
    game_id, game = game_runner.start_game()
    while not game.is_finished():
        game.print()
        game.play_single_step(verbose=False)
    print("GAME FINISHED")
    game.print()
    if game.player_won():
        print("Player won with score of {}".format(game.player.score))
