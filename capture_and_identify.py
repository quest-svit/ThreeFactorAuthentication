import captureFromCamera as cap
import face_detect_and_extract as det
import face_identification as iden

def captureAndIdentify():
  cap.capture_and_save("./images","Camera.jpg")
  lastNumber=1
  gray,faceCascade,image=det.read_image('./images/Camera.jpg')
  faces=det.detect_faces(gray,faceCascade)
  det.draw_rectangle(faces,image)
  extracted_imgs=det.extract_faces(faces,image)
  det.display_and_Save_faces(extracted_imgs,lastNumber)

  batch_size = 32
  img_height = 180
  img_width = 180
  class_names=['ankit', 'chitrang', 'harshit', 'jignesh', 'mitul', 'nishil', 'tanmay', 'urmish']

  img_array=iden.load_unknown_image("./images/image1.png",img_height,img_width)
  flower_type,confidence=iden.predict(img_array,class_names)
  return flower_type,confidence

#Program starts here
if __name__ == "__main__":

  Person,confidence=captureAndIdentify()
  
  print("Detected Face "+Person+ " with confidence of " + str(confidence))
