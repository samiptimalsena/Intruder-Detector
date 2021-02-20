import os

from config import REGISTERED_IMAGES,DETECTION_LOGS

if not os.path.exists(DETECTION_LOGS):
    os.makedirs(DETECTION_LOGS)