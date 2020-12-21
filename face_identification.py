import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import pathlib
import matplotlib.pyplot as plt

def load_dataset():

  data_dir = pathlib.Path("./images/faces")

  return data_dir

def train_test_split(data_dir):

  train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

  val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)
  
  return train_ds,val_ds


def create_compile_model(img_height, img_width,num_classes):
  model = Sequential([
    layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
  ])

  model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
  return model


def train_model(model,train_ds,val_ds):
  epochs=10
  history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
  )
  return model

def save_model(model):
  # Save the entire model as a SavedModel.
  model.save('saved_model/faces_model') 
  print("Model Saved successfully")

def load_unknown_image(filename,img_height,img_width):
  unknown_flower_path =  pathlib.Path(filename)

  img = keras.preprocessing.image.load_img(
      unknown_flower_path, target_size=(img_height, img_width)
  )
  img_array = keras.preprocessing.image.img_to_array(img)
  img_array = tf.expand_dims(img_array, 0) # Create a batch

  return img_array

def predict(img_array,class_names):
  new_model = tf.keras.models.load_model('saved_model/faces_model')
  predictions = new_model.predict(img_array)
  score = tf.nn.softmax(predictions[0])
  return class_names[np.argmax(score)],100 * np.max(score)

#Program starts here
if __name__ == "__main__":

  batch_size = 32
  img_height = 180
  img_width = 180
  class_names=['ankit', 'chitrang', 'harshit', 'jignesh', 'mitul', 'nishil', 'tanmay', 'urmish']

  if not os.path.isdir('saved_model/faces_model'):

    data_dir=load_dataset()
    train_ds,val_ds = train_test_split(data_dir)

    class_names = train_ds.class_names
    print(class_names)

    AUTOTUNE = tf.data.experimental.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    num_classes = 8
    model = create_compile_model(img_height, img_width,num_classes)
    trained_model=train_model(model,train_ds,val_ds)
    save_model(trained_model)


  img_array=load_unknown_image("./images/image66.png",img_height,img_width)
  flower_type,confidence=predict(img_array,class_names)
  print("Detected Face "+flower_type+ " with confidence of " + str(confidence))
