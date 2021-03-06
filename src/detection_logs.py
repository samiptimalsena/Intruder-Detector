import streamlit as st
from glob import glob
import numpy as np
from PIL import Image
import config
import os

DETECTION_LOGS = config.DETECTION_LOGS

def show_images(slot1):

    image_path = glob(DETECTION_LOGS+"/*")
    if len(image_path) == 0:
        slot1.write("No Images")
    else:
        image_names = [path.split("/")[-1].split(".")[0] for path in image_path]
        cols = slot1.beta_columns(3)
        j = 0
        for i in range(len(image_path)):
            j = j % 3
            img = Image.open(image_path[i])
            cols[j].image(img, caption=image_names[i])
            j += 1
        