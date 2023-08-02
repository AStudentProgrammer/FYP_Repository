# import the opencv library
import cv2

from time import sleep,time
prev_time = 0


# define a video capture object
vid = cv2.VideoCapture(1)
count = 0


while(True):
    current_time = time()
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # Display the resulting frame
    cv2.imshow('frame', frame)
    filename = "img_" + str(count) + ".jpeg"
    
    if current_time - prev_time >= 10:
        cv2.imwrite(filename,frame)
        prev_time = time()        
        count = count + 1
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    #sleep(10)
        
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
