import cv2
import os

def capture_images(outfolder = 'cam_calibrate/calib_img'):
    # Open the webcam
    cap = cv2.VideoCapture(0)  # 0 represents the default camera (you may need to change it if you have multiple cameras)
    index = 0 
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
-+++++

        # Display the frame
        cv2.imshow('Webcam', frame)
        # print('HEYO')
        # Check for the 'ESC' key to exit the loop
        k = cv2.waitKey(1)%256
        if k  == 27:
            break

        elif k ==  32:  # 32 is the ASCII code for the space key
            # Save the captured frame as an image
            image_filename = os.path.join(outfolder, str(index)+'.png')
            print(image_filename)
            cv2.imwrite(image_filename, frame)
            print(f"Image captured and saved as {image_filename}")
            
        index+=1 

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

# Run the function
capture_images()

