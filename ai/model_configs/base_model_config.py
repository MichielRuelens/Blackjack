from abc import abstractmethod, ABCMeta

import tensorflow as tf


class BaseModelConfig(metaclass=ABCMeta):

    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    def model_class(self):
        raise NotImplementedError

    @property
    def save_path(self) -> str:
        raise NotImplementedError

    def load_model(self) -> tf.keras.Model:
        model = self.model_class(self)
        model.load_weights(self.save_path)
        return model
