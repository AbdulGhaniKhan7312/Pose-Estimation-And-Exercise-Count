# Importing the libraries
import cv2
import numpy as np
import mediapipe as mp
import math
import time
import pyttsx3

def calc_angle(a,b,c): # 3D points
    ''' Arguments:
        a,b,c -- Values (x,y,z, visibility) of the three points a, b and c which will be used to calculate the
                vectors ab and bc where 'b' will be 'elbow', 'a' will be shoulder and 'c' will be wrist.
        
        Returns:
        theta : Angle in degress between the lines joined by coordinates (a,b) and (b,c)
    '''
    a = np.array([a.x, a.y])#, a.z])    # Reduce 3D point to 2D
    b = np.array([b.x, b.y])#, b.z])    # Reduce 3D point to 2D
    c = np.array([c.x, c.y])#, c.z])    # Reduce 3D point to 2D

    ab = np.subtract(a, b)
    bc = np.subtract(b, c)
    
    theta = np.arccos(np.dot(ab, bc) / np.multiply(np.linalg.norm(ab), np.linalg.norm(bc)))     # A.B = |A||B|cos(x) where x is the angle b/w A and B
    theta = 180 - 180 * theta / 3.14    # Convert radians to degrees
    
    return np.round(theta, 2)                              

def draw_rounded_rect(img, rect_start, rect_end, corner_width, box_color):

    x1, y1 = rect_start
    x2, y2 = rect_end
    w = corner_width

    # draw filled rectangles
    cv2.rectangle(img, (x1 + w, y1), (x2 - w, y1 + w), box_color, -1)
    cv2.rectangle(img, (x1 + w, y2 - w), (x2 - w, y2), box_color, -1)
    cv2.rectangle(img, (x1, y1 + w), (x1 + w, y2 - w), box_color, -1)
    cv2.rectangle(img, (x2 - w, y1 + w), (x2, y2 - w), box_color, -1)
    cv2.rectangle(img, (x1 + w, y1 + w), (x2 - w, y2 - w), box_color, -1)


    # draw filled ellipses
    cv2.ellipse(img, (x1 + w, y1 + w), (w, w),
                angle = 0, startAngle = -90, endAngle = -180, color = box_color, thickness = -1)

    cv2.ellipse(img, (x2 - w, y1 + w), (w, w),
                angle = 0, startAngle = 0, endAngle = -90, color = box_color, thickness = -1)

    cv2.ellipse(img, (x1 + w, y2 - w), (w, w),
                angle = 0, startAngle = 90, endAngle = 180, color = box_color, thickness = -1)

    cv2.ellipse(img, (x2 - w, y2 - w), (w, w),
                angle = 0, startAngle = 0, endAngle = 90, color = box_color, thickness = -1)

    return img

def draw_text(
    img,
    msg,
    width = 8,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    pos=(0, 0),
    font_scale=1,
    font_thickness=2,
    text_color=(0, 255, 0),
    text_color_bg=(0, 0, 0),
    box_offset=(20, 10),
):

    offset = box_offset
    x, y = pos
    text_size, _ = cv2.getTextSize(msg, font, font_scale, font_thickness)
    text_w, text_h = text_size
    rec_start = tuple(p - o for p, o in zip(pos, offset))
    rec_end = tuple(m + n - o for m, n, o in zip((x + text_w, y + text_h), offset, (25, 0)))
    
    img = draw_rounded_rect(img, rec_start, rec_end, width, text_color_bg)

    cv2.putText(
        img,
        msg,
        (int(rec_start[0] + 6), int(y + text_h + font_scale - 1)), 
        font,
        font_scale,
        text_color,
        font_thickness,
        cv2.LINE_AA,
    )
    
    return text_size

def draw_points(image, p1, p2, p3, frame_width, frame_height, color1, color2):
    
    cv2.line(image, tuple(np.multiply([p1.x, p1.y], [frame_width,frame_height]).astype(int)), tuple(np.multiply([p2.x, p2.y], [frame_width,frame_height]).astype(int)), color1,3)
    cv2.line(image, tuple(np.multiply([p3.x, p3.y], [frame_width,frame_height]).astype(int)), tuple(np.multiply([p2.x, p2.y], [frame_width,frame_height]).astype(int)), color1,3)
    cv2.circle(image, tuple(np.multiply([p1.x, p1.y], [frame_width,frame_height]).astype(int)), 5, color2, cv2.FILLED)
    cv2.circle(image, tuple(np.multiply([p1.x, p1.y], [frame_width,frame_height]).astype(int)), 10, color2, 1)
    cv2.circle(image, tuple(np.multiply([p2.x, p2.y], [frame_width,frame_height]).astype(int)), 5, color2, cv2.FILLED)
    cv2.circle(image, tuple(np.multiply([p2.x, p2.y], [frame_width,frame_height]).astype(int)), 10, color2, 1)
    cv2.circle(image, tuple(np.multiply([p3.x, p3.y], [frame_width,frame_height]).astype(int)), 5, color2, cv2.FILLED)
    cv2.circle(image, tuple(np.multiply([p3.x, p3.y], [frame_width,frame_height]).astype(int)), 10, color2, 1)
    
    return image

def draw_2points(image, p1, p2, frame_width, frame_height, color1, color2):
    
    cv2.line(image, tuple(np.multiply([p1.x, p1.y], [frame_width,frame_height]).astype(int)), tuple(np.multiply([p2.x, p2.y], [frame_width,frame_height]).astype(int)), color1,3)
    cv2.circle(image, tuple(np.multiply([p1.x, p1.y], [frame_width,frame_height]).astype(int)), 5, color2, cv2.FILLED)
    cv2.circle(image, tuple(np.multiply([p1.x, p1.y], [frame_width,frame_height]).astype(int)), 10, color2, 1)
    cv2.circle(image, tuple(np.multiply([p2.x, p2.y], [frame_width,frame_height]).astype(int)), 5, color2, cv2.FILLED)
    cv2.circle(image, tuple(np.multiply([p2.x, p2.y], [frame_width,frame_height]).astype(int)), 10, color2, 1)

    return image


def infer():
    
    mp_drawing = mp.solutions.drawing_utils     # Connecting Keypoints Visuals
    mp_pose = mp.solutions.pose                 # Keypoint detection model
    
    engine = pyttsx3.init()   # text to speech initialise
    
    left_flag = None     # Flag which stores hand position(Either UP or DOWN)
    left_count = 0       # Storage for count of bicep curls
    right_flag = None
    right_count = 0

    incorrect_l = 0
    incorrect_r = 0
    
    reps = 3
    sets = 2
    
    l_complete = False
    r_complete = False
    complete = False
    
    RED = (0,0,255)
    YELLOW = (255,255,0)
    WHITE = (255,255,255)
    BLUE = (255,0,0)
    BLACK = (0,0,0)
    
    
    offset_thresh = 0
    hip_thresh = [170,180]
    knee_thresh = [170,180]
    elbow_thresh = [40,160]
    wrist_thresh = 0
    nose_thresh = 0
    shoulder_thresh = 20
    
#     disp_feedback_1 = 'KEEP WRIST STRAIGHT'
    disp_feedback_2 = 'Keep arm straight'
#     disp_feedback_3 = 'Keep straight'

    cap = cv2.VideoCapture(0)
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) # Landmark detection model instance
    
        # Initialize OpenCV window with a specific name
    cv2.namedWindow("MediaPipe feed", cv2.WINDOW_NORMAL)

    # Resize the window to the desired size (1000 x 1000)
    cv2.resizeWindow("MediaPipe feed", 1280, 720)
#     pTime = 0

    while cap.isOpened():
        _, frame = cap.read()

        # BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)      # Convert BGR frame to RGB
        image.flags.writeable = False
        
        frame_height, frame_width, _ = image.shape
        
        # Make Detections
        results = pose.process(image)                       # Get landmarks of the object in frame from the model

        # Back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)      # Convert RGB back to BGR

        try:
            # Extract Landmarks
            landmarks = results.pose_landmarks.landmark
            
            nose = landmarks[mp_pose.PoseLandmark.NOSE]
            
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
            left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
            left_foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
            
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
            right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
            right_foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]

            # Render Shoulder, Elbow and Wrist only
            
            image = draw_points(image,left_shoulder,left_elbow,left_wrist,frame_width,frame_height,RED,WHITE)
            image = draw_points(image,right_shoulder,right_elbow,right_wrist,frame_width,frame_height,RED,WHITE)

            # Calculate angles between x-axis and y-axis
            
            left_elbow_angle = int(calc_angle(left_shoulder, left_elbow, left_wrist))     
            right_elbow_angle = int(calc_angle(right_shoulder, right_elbow, right_wrist))
            
            left_shoulder_angle = int(calc_angle(left_hip,left_shoulder,left_elbow))
            right_shoulder_angle = int(calc_angle(right_hip,right_shoulder,right_elbow))
            
            left_hip_angle = int(calc_angle(left_shoulder,left_hip,left_knee))
            right_hip_angle = int(calc_angle(right_shoulder,right_hip,right_knee))
            
            # Feedback
                
            if left_shoulder_angle > shoulder_thresh: 
                draw_text(
                    image, 
                    disp_feedback_2, 
                    pos=(30, frame_height-30),
                    text_color=WHITE,
                    font_scale=0.7,
                    text_color_bg= RED,
                )

            else: # Count left
                image = draw_points(image,left_shoulder,left_elbow,left_wrist,frame_width,frame_height,BLUE,WHITE)
                if left_elbow_angle > elbow_thresh[1]:
                    left_flag = 'down'
                if left_elbow_angle < elbow_thresh[0] and left_flag=='down':
                    if left_count == reps:
                        l_complete = True
                    else:
                        left_count += 1
                        incorrect_l = 0
                        left_flag = 'up'
                        
            if right_shoulder_angle > shoulder_thresh: 
                draw_text(
                    image, 
                    disp_feedback_2, 
                    pos=(30, frame_height-80),
                    text_color=WHITE,
                    font_scale=0.7,
                    text_color_bg= RED,
                )
                    
            else: # Count right 
                image = draw_points(image,right_shoulder,right_elbow,right_wrist,frame_width,frame_height,BLUE,WHITE)
                if right_elbow_angle > elbow_thresh[1]:
                    right_flag = 'down'
                if right_elbow_angle < elbow_thresh[0] and right_flag=='down':
                    if right_count == reps:
                        r_complete = True
                    else:
                        right_count += 1
                        incorrect_r = 0
                        right_flag = 'up'         
            
        except:
            pass
        
        draw_text(
            image, 
            "Left : " + str(left_count) + "/" + str(reps), 
            pos=(30, 30),
            text_color=WHITE,
            font_scale=0.7,
            text_color_bg= BLUE,
        )  

        draw_text(
            image, 
            "Right : " + str(right_count) + "/" + str(reps), 
            pos=(30, 80),
            text_color=WHITE,
            font_scale=0.7,
            text_color_bg= BLUE,
        )
        
        cv2.imshow('MediaPipe feed', image)

        k = cv2.waitKey(10) & 0xff  # Esc for quiting the app
            
        if l_complete == True and r_complete == True:
            complete = True
            engine.say('Welldone')
            engine.runAndWait()
            cap.release()
            cv2.destroyAllWindows()
            return complete
        
        elif k==27:
            break
            
        elif k==ord('r'):       # Reset the counter on pressing 'r' on the Keyboard
            left_count = 0
            right_count = 0
            incorrect_l = 0
            incorrect_r = 0
        
#         else:
#             return False
            
    cap.release()
    cv2.destroyAllWindows()
    

if __name__=='__main__':
    
    # User Inputs
    
    engine = pyttsx3.init()   # text to speech initialise
    engine.say('Your dumbbell curl exercise is about to start, remember to maintain a good posture and keep your arms straight')
    engine.runAndWait()
    
    # Start Exercise and return status (Complete / Incomplete)
    
    complete = infer()
    print('Completed : ', complete)