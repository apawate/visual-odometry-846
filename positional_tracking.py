
"""
    This sample shows how to track the position of the ZED camera 
    and displays it in a OpenGL window.
"""

import sys
import pillow
from PIL import Image
import ogl_viewer.tracking_viewer as gl
import pyzed.sl as sl
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time


def Tracking(p0, p1):
    image = PIL.Image.open("Screen_Shot_2022-02-06_at_8.24.27_PM.png")
    blank_image = np.array(image)
    p1*=500
    p0*=500
    p0=round(p0)
    p1=round(p1)

    cv2.circle(blank_image, (p0+600, p1+600),4, (0, 0, 0), 2)
    plt.imshow(blank_image)
    cv2.namedWindow("Display", cv2.WINDOW_AUTOSIZE)

    # using cv2.imshow() to display the image
    cv2.imshow('Display', blank_image)
    cv2.waitKey(1)







if __name__ == "__main__":

    init_params = sl.InitParameters(camera_resolution=sl.RESOLUTION.HD720,
                                 coordinate_units=sl.UNIT.METER,
                                 coordinate_system=sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP)
                                 
    # If applicable, use the SVO given as parameter
    # Otherwise use ZED live stream
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        print("Using SVO file: {0}".format(filepath))
        init_params.set_from_svo_file(filepath)

    zed = sl.Camera()
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    tracking_params = sl.PositionalTrackingParameters()
    zed.enable_positional_tracking(tracking_params)

    runtime = sl.RuntimeParameters()
    camera_pose = sl.Pose()

    camera_info = zed.get_camera_information()
    # Create OpenGL viewer
    viewer = gl.GLViewer()
    viewer.init(camera_info.camera_model)

    py_translation = sl.Translation()
    pose_data = sl.Transform()

    text_translation = ""
    text_rotation = ""
    frame = 0
    p0 = (0, 0)

    rotationLast = 0
    translationLast = 0
    text_rotationLast = 0
    pose_dataLast = 0
    numFrames = 0

    rotationLimit = 180
    translationLimit = 5

    while viewer.is_available():
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            tracking_state = zed.get_position(camera_pose)
            if tracking_state == sl.POSITIONAL_TRACKING_STATE.OK:


                rotation = camera_pose.get_rotation_vector()

                translation = camera_pose.get_translation(py_translation)
                text_rotation = str((round(rotation[0], 2), round(rotation[1], 2), round(rotation[2], 2)))
                text_translation = str((round(translation.get()[0], 2), round(translation.get()[1], 2), round(translation.get()[2], 2)))
                pose_data = camera_pose.pose_data(sl.Transform())

                Tracking(round(translation.get()[0], 2),round(translation.get()[2], 2))
                viewer.updateData(pose_data, text_translation, text_rotation, tracking_state)

                numFrames = numFrames + 1
                #print(round((((round(translation.get()[0], 2)**2)+(round(translation.get()[2], 2)**2))**0.5)*39.66010468,2))
                #(round((((round(translation.get()[0], 2) ** 2) + (round(translation.get()[2], 2) ** 2)) ** 0.5) * 39.66010468, 2))
                #print(round((((abs((round(translation.get()[0], 2)))**2)+(abs(4+(round(translation.get()[2], 2)))**2))**.5)*39.66010468,2))
                print(round((((abs((round(translation.get()[0], 2)))**2)+(abs((round(translation.get()[2], 2)))**2))**.5)*39.66010468,2))



    viewer.exit()
    zed.close()




