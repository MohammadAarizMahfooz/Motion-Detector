import cv2
import winsound

print("Welcome to Motion detector. choose any one of them\n1. Motion detection with webcam\n2. Motion detection with you mobile's camera(read README.md for more info.)")
inp = input()
url = "http://192.168.0.102:8080/video"
if "1" in inp:
    cam = cv2.VideoCapture(0)
elif "2" in inp:
    ip_add = input("Enter your IP address with Port\n")
    url = f"http://{ip_add}/video"
    cam = cv2.VideoCapture(url)
while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame1, contours, -1, (0, 0, 255), 2)
    for c in contours:
        if cv2.contourArea(c) < 3500:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)
        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('Motion detector', frame1)