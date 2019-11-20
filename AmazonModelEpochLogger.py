from gensim.models.callbacks import CallbackAny2Vec
from gensim.models import Word2Vec

historic_loss = list()
epochs_list = list()

class EpochLogger(CallbackAny2Vec):
    '''Callback to print loss after each epoch.'''

    def __init__(self):
        self.epoch = 0
        self.prev_loss = 0

    def on_epoch_end(self, model: Word2Vec):
        loss = model.get_latest_training_loss() - self.prev_loss

        historic_loss.append(loss)
        epochs_list.append(self.epoch)

        print('Loss after epoch {}: {}'.format(self.epoch, loss))
        self.prev_loss += loss
        self.epoch += 1