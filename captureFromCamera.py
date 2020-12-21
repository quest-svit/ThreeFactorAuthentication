import cv2
import os

def capture_and_save(path,filename):
  videoCaptureObject = cv2.VideoCapture(0)
  result = True
  while(result):
      ret,frame = videoCaptureObject.read()
      cv2.imwrite(os.path.join(path , filename),frame)
      result = False
  videoCaptureObject.release()
  cv2.destroyAllWindows()

if __name__ == "__main__":
  capture_and_save("./images","Camera.jpg")
