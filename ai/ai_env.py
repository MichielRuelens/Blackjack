import logging
from typing import Optional

import numpy as np
from gym import Env, spaces

from ai.controlled_game import ControlledGame
from base.actions.action import Action
from base.actions.action_service import ActionService
from base.constants import Constants
from base.enums.game_phase import GamePhase


class BlackjackEnv(Env):
    """
    An implementation of the OpenAI environment class for the Blackjack game.
    """

    def __init__(self, num_actions, state_size):
        self.__version__ = "0.1.0"
        logging.info("Blackjack - Version {}".format(self.__version__))

        # Game variables
        self.game = None  # type: Optional[ControlledGame]
        self.curr_step = -1

        # Define what the agent can do, each action in the game has a unique index
        self.action_space = spaces.Discrete(num_actions)

        # Not sure yet what to do with the observation space
        self.observation_space = spaces.Discrete(state_size)

        # Store what the agent tried
        self.curr_episode = -1
        self.action_episode_memory = []

    def step(self, action_idx: int):
        """
        The agent takes a step in the environment.
        Parameters
        ----------
        action_idx : int
        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        if self.game.is_finished():
            raise RuntimeError("Episode is done, please reset the game.")
        action = ActionService().idx_to_action(action_idx)  # type: Action
        self.curr_step += 1
        self._take_action(action, action_idx)
        reward = action.get_reward()
        # If the game is over and the last player who played a card is the winner, add a winning bonus to the reward
        # Note that at this point the 'current player' is not the player who took the last action,
        # since _take_action() already swapped the current player.
        if self.game.is_finished():
            reward += Constants.rewards.get(self.game.player.score)
        observation = self._get_state()
        return observation, reward, self.game.is_finished(), {}

    def get_current_actions_mask(self):
        return self.game.get_current_actions_mask()

    def _take_action(self, action: Action, action_idx: int):
        self.action_episode_memory[self.curr_episode].append(action_idx)
        self.game.play_action(action)
        if self.game.board.phase == GamePhase.END_TURN_PHASE:
            self.game.switch_player_turns()

    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.
        Returns
        -------
        observation (object): the initial observation of the space.
        """
        self.curr_step = -1
        self.curr_episode += 1
        self.action_episode_memory.append([])
        if self.game is None:
            self.game = ControlledGame()
        self.game.reset_game(initialize=True)
        return self._get_state()

    def _get_state(self) -> np.array:
        return np.array(self.game.get_state().create_numeral_representation(self.game.current_player), dtype=np.float32)

    def render(self, mode='human'):
        pass
