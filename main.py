# import cv2
# import numpy as np
# import tempfile
# import streamlit as st
#
#
# harcascade = "model/haarcascade_russian_plate_number.xml"
#
# cap = cv2.VideoCapture(0)
#
# cap.set(3, 640) # width
# cap.set(4, 480) #height
#
# min_area = 500
# count = 0
#
# # cap = cv2.VideoCapture(0)
# st.title("ANPR")
#
# frame_placeholder = st.empty()
# stop_button_pressed = st.button("Stop")
#
# while cap.isOpened() and not stop_button_pressed:
#     # ret, frame = cap.read()
#
#     success, img = cap.read()
#
#     plate_cascade = cv2.CascadeClassifier(harcascade)
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#     plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)
#     for (x, y, w, h) in plates:
#         area = w * h
#
#         if area > min_area:
#             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
#
#             img_roi = img[y: y + h, x:x + w]
#             # cv2.imshow("ROI", img_roi)
#
#     # cv2.imshow("Result", img)
#
#     if not success:
#         st.write("the video captured is end.")
#         break
#
#     frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     frame_placeholder.image(frame, channels="RGB")
#
#     if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
#         break
#
# cap.release()
# cv2.destroyWindow()




import cv2
import numpy as np
import streamlit as st

# Load the cascade for number plate detection
harcascade = "model/haarcascade_russian_plate_number.xml"
plate_cascade = cv2.CascadeClassifier(harcascade)

def funVideo():
    # Open the video capture
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # width
    cap.set(4, 480)  # height

    min_area = 500
    count = 0

    # Streamlit setup
    st.title("ANPR")

    col1, col2, col3 = st.columns(3)
    with col1:
        frame_placeholder1 = st.empty()
    with col2:
        frame_placeholder2 = st.empty()
    with col3:
        process_button_pressed = st.button("process")
        stop_button_pressed = st.button("Stop")

    text_placeholder = st.empty()


    while cap.isOpened() and not stop_button_pressed:
        success, img = cap.read()

        if not success:
            st.write("The video capture has ended.")
            break

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (x, y, w, h) in plates:
            area = w * h
            if area > min_area:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

                img_roi = img[y: y + h, x:x + w]
                frame_placeholder2.image(img_roi, channels="RGB", caption="Frame with Detected Number Plates")
                text_placeholder.text(process_button_pressed)
                if process_button_pressed:
                    text_placeholder.text("Progressing....")
                    cv2.imwrite("plates/si_" + str(count) + ".jpg", img_roi)
                    cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
                    cv2.imshow("Results", img)
                    text_placeholder.text("The number plate is : ")
                    cv2.waitKey(500)
                    count += 1
                    process_button_pressed = not process_button_pressed


        # Display the original frame
        frame1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame_placeholder1.image(frame1, channels="RGB", caption="Original Frame")

        # Display the frame with detected number plates
        # frame2 = cv2.cvtColor(img_roi, cv2.COLOR_BGR2RGB)
        # frame_placeholder2.image(img_roi, channels="RGB", caption="Frame with Detected Number Plates")


        if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
            break

    cap.release()
    cv2.destroyAllWindows()
funVideo()