#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Locates ball on platform and sends the
X and Y coordinates over Modbus to assigned
slave on ip: 192.168.2.17, port: 502.

Code by: Magnus Øye, Dated: 13.10-2018
Contact: magnus.oye@gmail.com
Website: https://github.com/magnusoy/Balancing-Platform
"""

# Importing packages
import cv2
from video_processing import ObjectDetection
from modbus_communication import ModbusClient
from joystick import Joystick

if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    cap.set(propId=3, value=640)
    cap.set(propId=4, value=480)

    client = ModbusClient()
    # js = Joystick()
    objectDetection = ObjectDetection(cap, watch=True)

    while client.isConnected():
        coordinates = objectDetection.getCoordinates()
        # joystick_coordinates = js.getEvents()
        client.sendInt(value=coordinates[0], address=12288)
        client.sendInt(value=coordinates[1], address=12290)
        # client.sendFloat(value=joystick_coordinates[0], address=12292)
        # client.sendFloat(value=joystick_coordinates[1], address=12294)

        # Break loop with ESC-key
        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            objectDetection.stop()
            break
