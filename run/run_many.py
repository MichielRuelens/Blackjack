from collections import defaultdict

from numpy import mean

from run.game_runner import GameRunner


def get_winner(g):
    player_0 = g.players[0]
    player_1 = g.players[1]
    if player_0.score > player_1.score:
        return player_0, player_0.score - player_1.score
    return player_1, player_0.score - player_1.score


if __name__ == '__main__':
    game_runner = GameRunner()

    num_broken = 0
    num_games = 100
    scores = []
    game_id, game = game_runner.start_game()
    for i in range(num_games):
        print("Playing game {}".format(i + 1))
        while not game.is_finished():
            game.play_single_step()
        if game.player.broken:
            num_broken += 1
        else:
            scores.append(game.player.score)
        game.reset_game(keep_players=True)
    print(f"Break Percent: {int((num_broken*100)/num_games)}%")
    print(f"Average score: {mean(scores)}")
