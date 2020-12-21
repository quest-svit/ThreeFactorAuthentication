import cv2
import sys
import os
from PIL import Image


def detect_faces(gray,faceCascade):
  # Detect faces in the image
  faces = faceCascade.detectMultiScale(
      gray,
      scaleFactor=1.1,
      minNeighbors=5,
      minSize=(30, 30),
      flags = cv2.CASCADE_SCALE_IMAGE)
  return faces

def draw_rectangle(faces,image):
  # Draw a rectangle around the faces
  for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
  
def extract_faces(faces,image):
  padding=2
  extracted_imgs = []
  for r in faces:
      x = r[0]+padding
      y = r[1]+padding
      w = r[2]-(padding*2)
      h = r[3]-(padding*2)
      roi = image[y:y+h, x:x+w]
      extracted_imgs.append(roi)
  return extracted_imgs

def display_and_Save_faces(extracted_imgs,lastNumber):
  # Display and Save the extracted images
  for i in range(len(extracted_imgs)):
      img = extracted_imgs[i]
      filename = "image" + str(i+lastNumber) + ".png"
      path="./images"
      cv2.imwrite(os.path.join(path , filename),img)
  print("Images Saved Successfully")

def read_image(imagePath):
  # Get user supplied values
  cascPath = './static/haarcascade_frontalface_default.xml'

  # Create the haar cascade
  faceCascade = cv2.CascadeClassifier(cascPath)

  # Read the image
  image = cv2.imread(imagePath)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  return gray,faceCascade,image

# Start of Program
if __name__ == "__main__":

  lastNumber=1
  gray,faceCascade,image=read_image('./images/Camera.jpg')
  faces=detect_faces(gray,faceCascade)
  draw_rectangle(faces,image)
  extracted_imgs=extract_faces(faces,image)
  display_and_Save_faces(extracted_imgs,lastNumber)

