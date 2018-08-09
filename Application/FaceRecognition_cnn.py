from keras.engine import Model
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Flatten, Dense, Input
from keras_vggface.vggface import VGGFace
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from FaceRecognition_imagepreprocessing import face_recording, take_image

import numpy as np
from keras import optimizers
import time, datetime

class Cnn_model:

    # Initial parameters
    label_id = []
    img_data = []
    index = 0
    # Custom parameters
    nb_class = 0
    hidden_dim = 512
    epochs_num = 2

    def initialize_networkmodel(self):

        ###### Define model ######
        vgg_model = VGGFace(include_top=False, weights='vggface', input_shape=(180, 180, 3))
        last_layer = vgg_model.get_layer('pool5').output
        # Add layers
        x = Flatten(name='flatten')(last_layer)
        x = Dense(self.hidden_dim, activation='relu', name='fc6')(x)
        x = Dense(self.hidden_dim, activation='relu', name='fc7')(x)
        out = Dense(self.nb_class, activation='softmax', name='fc8')(x)
        self.custom_vgg_model = Model(vgg_model.input, out)
        # Turn some layers as not trainable | Last three dense layers are trainable
        layer_count = 0
        for layer in self.custom_vgg_model.layers:
            layer_count = layer_count + 1
        for l in range(layer_count - 3):
            self.custom_vgg_model.layers[l].trainable = False

        ###### Finalize the model ######
        sgd = optimizers.SGD(lr=5e-3, decay=1e-6, momentum=0.9, nesterov=True)
        self.custom_vgg_model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

    def add_person(self, **kwargs):
        gui = kwargs.get('gui', False)
        data = face_recording(gui = gui, cnn=True)

        # If first face is to be added
        if not self.label_id:
            curr_id=0
        else:
            curr_id = max(self.label_id)+1
        self.label_id.extend([curr_id]*len(data))
        self.img_data.extend(data)
        self.nb_class+=1

        print("Added face with label = {}.".format(curr_id))


    def data_processing(self):
        self.label_id = to_categorical(self.label_id)
        X_train, X_test, y_train, y_test = train_test_split(
            np.array(self.img_data), self.label_id, test_size=0.1)
        train_datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest')
        validation_datagen = ImageDataGenerator()

        # Batchsize parameters
        self.train_batchsize = int(round(len(X_train)/10))
        self.val_batchsize = self.train_batchsize

        self.train_generator = train_datagen.flow(
            X_train,
            y_train,
            shuffle=True,
            batch_size=self.train_batchsize)

        self.validation_generator = validation_datagen.flow(
            X_test,
            y_test,
            batch_size=self.val_batchsize)


    def train_cnn(self):
        # Train the model
        self.history = self.custom_vgg_model.fit_generator(
            self.train_generator,
            steps_per_epoch=self.train_generator.n / self.train_generator.batch_size,
            epochs=self.epochs_num,
            validation_data=self.validation_generator,
            validation_steps=self.validation_generator.n / self.validation_generator.batch_size,
            verbose=1)

        self.custom_vgg_model.save('trained_model_{}'.format(
            datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')))

    def recognize_face(self, gui=False):
        try:
            assert self.custom_vgg_model
        except:
            raise AttributeError()
        image = take_image(gui=gui, cnn=True)
        print(np.argmax(self.custom_vgg_model.predict(np.expand_dims(image, axis=0))))

    def accuracy_statistics(self):
        ##### Show results #####
        acc = self.history.history['acc']
        val_acc = self.history.history['val_acc']
        loss = self.history.history['loss']
        val_loss = self.history.history['val_loss']
        epochs = range(len(acc))

        # summarize history for accuracy
        plt.subplot(121)
        plt.plot(epochs, acc)
        plt.plot(epochs, val_acc)
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        # summarize history for loss
        plt.subplot(122)
        plt.plot(epochs,loss)
        plt.plot(epochs,val_loss)
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

if __name__ == "__main__":
    nnmodel = Cnn_model()
    nnmodel.add_person()
    time.sleep(1)
    nnmodel.add_person()
    nnmodel.data_processing()
    nnmodel.initialize_networkmodel()
    nnmodel.train_cnn()
    nnmodel.accuracy_statistics()
    nnmodel.recognize_face()
