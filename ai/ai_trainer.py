from collections import defaultdict

import numpy as np
import tensorflow as tf

from ai.ai_env import BlackjackEnv
from ai.model_configs.mlp_config import MLPConfig
from ai.multi_layer_perceptron import MultiLayerPerceptron
from base.actions.action_service import ActionService


class DQN:
    def __init__(self, model_config: MLPConfig, gamma, max_experiences, min_experiences, batch_size, lr):
        self.num_actions = model_config.num_actions
        self.batch_size = batch_size
        self.optimizer = tf.optimizers.Adam(lr)
        self.gamma = gamma
        self.model = MultiLayerPerceptron(model_config)
        self.experience = defaultdict(list)
        self.max_experiences = max_experiences
        self.min_experiences = min_experiences

    def predict(self, state):
        inputs = {'state': np.atleast_2d(state)}
        return self.model(inputs)

    @tf.function
    def train(self, target_net):
        if len(self.experience['s']) < self.min_experiences:
            return 0
        ids = np.random.randint(low=0, high=len(self.experience['s']), size=self.batch_size)
        states = np.asarray([self.experience['s'][i] for i in ids])
        actions = np.asarray([self.experience['a'][i] for i in ids])
        rewards = np.asarray([self.experience['r'][i] for i in ids])
        states_next = np.asarray([self.experience['s2'][i] for i in ids])
        dones = np.asarray([self.experience['done'][i] for i in ids])
        value_next = np.max(target_net.predict(states_next), axis=1)
        actual_values = np.where(dones, rewards, rewards+self.gamma*value_next)

        with tf.GradientTape() as tape:
            selected_action_values = tf.math.reduce_sum(
                self.predict(states) * tf.one_hot(actions, self.num_actions), axis=1)
            loss = tf.math.reduce_sum(tf.square(actual_values - selected_action_values))
        variables = self.model.trainable_variables
        gradients = tape.gradient(loss, variables)
        self.optimizer.apply_gradients(zip(gradients, variables))

    def get_action(self, state, mask, epsilon):
        if np.random.random() < epsilon:
            valid_actions_indexes = [idx for idx, is_valid in enumerate(mask) if is_valid]
            return np.random.choice(valid_actions_indexes)
        else:
            predictions = self.predict(np.atleast_2d(state))
            proper_predictions = predictions * np.atleast_2d(mask)
            masked_predictions = np.atleast_2d(np.logical_not(mask) * (np.min(predictions) - 1))
            predictions = proper_predictions + masked_predictions
            return np.argmax(predictions[0])

    def add_experience(self, exp):
        if len(self.experience['s']) >= self.max_experiences:
            for key in self.experience.keys():
                self.experience[key].pop(0)
        for key, value in exp.items():
            self.experience[key].append(value)

    def copy_weights(self, train_net):
        variables1 = self.model.trainable_variables
        variables2 = train_net.model.trainable_variables
        for v1, v2 in zip(variables1, variables2):
            v1.assign(v2.numpy())


def play_game(env, train_net, target_net, epsilon, copy_step, print_exp_step):
    rewards = 0
    iteration = 0
    done = False
    state = env.reset()
    while not done:
        actions_mask = env.get_current_actions_mask()
        action = train_net.get_action(state, actions_mask, epsilon)
        prev_state = state
        state, reward, done, _ = env.step(action)
        rewards += reward
        if done:
            reward = -10
            env.reset()

        exp = {'s': prev_state, 'a': action, 'r': reward, 'm': actions_mask, 's2': state, 'done': done}
        train_net.add_experience(exp)
        train_net.train(target_net)
        iteration += 1
        if iteration % print_exp_step == 0:
            print("Experience replay:")
            for exp_action in train_net.experience['a']:
                print(ActionService().idx_to_action(exp_action))
        if iteration % copy_step == 0:
            target_net.copy_weights(train_net)
    return rewards


def main():
    cfg = MLPConfig()
    # ============ CONFIG PARAMETERS =============== #
    gamma = cfg.gamma
    copy_step = cfg.copy_step
    print_exp_step = cfg.print_exp_step
    max_experiences = cfg.max_experiences
    min_experiences = cfg.min_experiences
    batch_size = cfg.batch_size
    lr = cfg.lr
    number_iterations = cfg.number_iterations
    total_rewards = np.empty(number_iterations)
    epsilon = cfg.epsilon
    decay = cfg.decay
    min_epsilon = cfg.min_epsilon
    avg_rewards = cfg.avg_rewards
    # =============================================== #
    env = BlackjackEnv(cfg.num_actions, cfg.num_states)
    summary_writer = tf.summary.create_file_writer(cfg.log_dir)
    train_net = DQN(cfg, gamma, max_experiences, min_experiences, batch_size, lr)
    target_net = DQN(cfg, gamma, max_experiences, min_experiences, batch_size, lr)
    for n in range(number_iterations):
        epsilon = max(min_epsilon, epsilon * decay)
        total_reward = play_game(env, train_net, target_net, epsilon, copy_step, print_exp_step)
        total_rewards[n] = total_reward
        avg_rewards = total_rewards[max(0, n - 100):(n + 1)].mean()
        with summary_writer.as_default():
            tf.summary.scalar('episode reward', total_reward, step=n)
            tf.summary.scalar('running avg reward(100)', avg_rewards, step=n)
        if n % 100 == 0:
            print("episode:", n, "episode reward:", total_reward, "eps:", epsilon, "avg reward (last 100):", avg_rewards)
    print("avg reward for last 100 episodes:", avg_rewards)
    env.close()
    train_net.model.save_weights(cfg.save_path)


if __name__ == '__main__':
    main()
