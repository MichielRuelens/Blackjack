from typing import Dict, Any, TYPE_CHECKING

import tensorflow as tf

if TYPE_CHECKING:
    from ai.model_configs.mlp_config import MLPConfig


class MultiLayerPerceptron(tf.keras.Model):

    def __init__(self, config: 'MLPConfig'):
        super(MultiLayerPerceptron, self).__init__()
        self.input_layer = tf.keras.layers.InputLayer(input_shape=(config.num_states,))
        self.hidden_layers = []
        for i in config.hidden_units:
            self.hidden_layers.append(tf.keras.layers.Dense(i, activation='tanh', kernel_initializer='RandomNormal'))
        self.output_layer = tf.keras.layers.Dense(
            config.num_actions, activation='linear', kernel_initializer='RandomNormal')

    @tf.function
    def call(self, inputs: Dict[str, Any]):
        state = inputs['state']
        z = self.input_layer(state)
        for layer in self.hidden_layers:
            z = layer(z)
        output = self.output_layer(z)
        return output
