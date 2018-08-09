from keras.engine import Model
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Flatten, Dense, Input
from keras_vggface.vggface import VGGFace
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from keras import models
import cv2 as cv
import numpy as np
from keras import optimizers
import os
import time

from keras.engine import Model
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Flatten, Dense, Input
from keras_vggface.vggface import VGGFace
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from keras import models
import cv2 as cv
import numpy as np
from keras import optimizers
import os
import time

def new_img_convert(img, h = 10, w = 10):
    img = img[h:-h, w:-w]
    img = cv.resize(img, (180, 180), interpolation=cv.INTER_CUBIC)
    img = img.astype('float32')
    img = img / 255.
    return img

# Start measuring time
start = time.time()
label_id = []
label_names = []
img_data = []
index = 0
# Change the batchsize according to RAM amount
train_batchsize = 64
val_batchsize = 5
# Custom parameters
nb_class = 0
hidden_dim = 512
epochs_num = 20
for subdir, dirs, files in os.walk(os.path.join(os.getcwd(), 'filtered_dataset')):

    # Start indexing when something appears
    if not label_id:
        index = 0
    else:
        index +=1

    for file in files:
        im = cv.imread(os.path.join(subdir, file))
        img_data.append(new_img_convert(im))
        label_id.append(index)
        if ''.join(file.split('.')[0].split('_')[:-1]) not in label_names:
            label_names.append(''.join(file.split('.')[0].split('_')[:-1]))
            nb_class += 1

label = to_categorical(label_id)
print(np.shape(img_data), nb_class, np.shape(label), np.shape(label_names))


huh = models.load_model("my_model_trained_night")
print(label_names[np.argmax(huh.predict(np.expand_dims(img_data[0], axis=0)))])
print(label_names[np.argmax(huh.predict(np.expand_dims(img_data[5], axis=0)))])
print(label_names[np.argmax(huh.predict(np.expand_dims(img_data[10], axis=0)))])
print(label_names[np.argmax(huh.predict(np.expand_dims(img_data[55], axis=0)))])
print(label_names[np.argmax(huh.predict(np.expand_dims(img_data[100], axis=0)))])
print(label_names[np.argmax(huh.predict(np.expand_dims(img_data[110], axis=0)))])
print(label_names[np.argmax(huh.predict(np.expand_dims(img_data[150], axis=0)))])
