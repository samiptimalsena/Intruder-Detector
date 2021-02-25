import streamlit as st
import video_capture
import os
from detection_logs import show_images
import config

DETECTION_LOGS = config.DETECTION_LOGS
INPUT_IMAGES = config.REGISTERED_IMAGES
if not os.path.exists(DETECTION_LOGS):
    os.makedirs(DETECTION_LOGS)


#hiding hamburger button
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

#Page title
st.title("ABC Management Office")
st.write("   ")
st.write("   ")
st.write("   ")
st.write("   ")

#Video window
FRAME_WINDOW = st.image(list())

with st.sidebar:
    st.title("Intruder Recognition")
    option = st.selectbox("Choose an option", ("Start Webcam", "Add New User"))
    admin_panel = st.button('🛡️ Admin Panel')

slot = st.empty()
slot2 = st.empty()

if admin_panel:
    show_images(slot)
    slot2.write(" ")

elif option == "Start Webcam":
    video_capture.startcam(FRAME_WINDOW)

elif option == "Add New User":
    user = slot.text_input("New user name")
    slot2.text("**Show your face in different angles for 5 seconds**")
    if not user:
        slot2.warning("Please enter user name")
        st.stop()

    if os.path.exists(INPUT_IMAGES+"/"+user.lower()):
        slot2.warning("User already exist")
        st.stop()

    os.makedirs(INPUT_IMAGES+"/"+user.lower())

    video_capture.collect_data(FRAME_WINDOW, user)
    slot2.write("Thanks for the patience 😀 !! You can now go to the start webcam")

    


