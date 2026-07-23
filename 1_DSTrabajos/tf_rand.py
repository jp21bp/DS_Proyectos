#### Este archivo tiene una variedad de diferentes conceptos
    # de TF avanzadp

import tensorflow as tf
import keras as K

#### Callback personalizado
class DetectOverfit(tf.keras.callbacks.Callback):
    def __init__(self, threshold: float = 0.7):
        super(DetectOverfit, self).__init__()
        self.threshold = threshold

    def on_epoch_end(self, epoch, logs = None):
        ratio = logs['val_loss']/logs['loss']
        print(f'Epoch {epoch} : va/train loss ratio:{ratio:.2f}')
        if ratio > self.threshold:
            self.model.stop_training = True
        return super().on_epoch_end(epoch, logs)

custom_callback = DetectOverfit(0.8)
dir(custom_callback)


#### Funcion de perdidad personalizada
### Huber loss
    # L = 0.5*a^2 if abs(a) < threshold else threshold*(abs(a)-0.5*threshold)
## Usando wrapper style
    # 'threshold' = hyperparam
    # Cualquier loss fcn espera un funcion que llame a 
            # 'y_true' y 'y_pred' como parametros

def my_huber_w_threshold(threshold):
    def my_huber(y_true, y_pred):
        error = y_true - y_pred
        is_small = tf.abs(error) <= threshold
        small_error = tf.square(error) / 2
        big_error = threshold * (tf.abs(error) - (0.5 * threshold))
        return tf.where(is_small, small_error, big_error)
    return my_huber
model.compile(optimizer='sgd', loss=my_huber_w_threshold(1.25))
## Usando class style
class MyHuberLoss(tf.keras.losses.Loss):
    def __init__(self, name : str = 'huber_loss', threshold : float = 1.0):
        super().__init__(name)
        self.threshold = threshold

    def call(self, y_true, y_pred):
        error = y_true - y_pred
        is_small = tf.abs(error) <= self.threshold
        small_error = tf.square(error) / 2
        big_error = self.threshold * (tf.abs(error) - (0.5 * self.threshold))
        return tf.where(is_small, small_error, big_error)
model.compile(optimizer='sgd', loss=my_huber_w_threshold(1.25))


### Contrastive Loss
    # L = Y * D^2 + (1-Y)*max(margin-D,0)
    # margin = loss hyperparameter
## Wrapper style
def con_loss_w_margin(margin):
    def cont_loss(y_true, y_pred):
        square_pred = K.square(y_pred)
        margin_square = K.square(K.maximum(margin-y_pred, 0))
        return K.mean(y_true*square_pred + (1-y_true)*margin_square)
    return cont_loss

## Class style
class ContLoss(tf.keras.losses.Loss):
    margin = 0  # No necesario, solo si quieres inicializar localmente
    def __init__(self, name = 'cont_loss', margin = margin):
        super().__init__(name)
        self.margin = margin

    def call(self, y_true, y_pred):
        square_pred = K.square(y_pred)
        margin_square = K.square(K.maximum(self.margin-y_pred, 0))
        return K.mean(y_true*square_pred + (1-y_true)*margin_square)


           
