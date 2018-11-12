#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visualization of the ball and the
moving platform.

Code by: Magnus Øye, Dated: 06.10-2018
Contact: magnus.oye@gmail.com
Website: https://github.com/magnusoy/Balancing-Platform
"""

# Importing packages
from vpython import *
from modbus_communication import ModbusClient
from numpy import sqrt, sin, cos


def translate(x, lowerIn, upperIn, lowerOut, upperOut):
    """Map in value range to another range"""
    y = (x - lowerIn) / (upperIn - lowerIn) * (upperOut - lowerOut) + lowerOut
    return y


# Constants
L = 45  # Length of one side
Z0 = 9.0  # Start lifting height
A = 4.0  # Center offset
r = 9.0  # Radius'

# Variables
pitch, roll = 0.0, 0.0
x_pos, y_pos = 0, 0

# Creating visualization scene
scene.title = "Balancing Platform Visualization"
scene.x = 0
scene.y = 0
scene.width = 1920
scene.height = 1080
scene.range = 30
scene.center = vector(1, 0, 0)
scene.background = vector(0, 0, 0)

# Creating objects
set_ball = sphere(pos=vector(0, 1.2, 0), radius=0.5, color=color.red)
ball = sphere(pos=vector(0, 1.2, 0), radius=0.5, color=color.blue)
platform = box(length=50, height=1.0, width=50, color=color.orange)
floor = box(pos=vector(0, -8.75, 0), size=vector(100, 1, 100), color=color.cyan)
leg_1 = cylinder(pos=vector(20, -Z0, 20), axis=vector(0, 8.75, 0), radius=1, color=color.green)
leg_2 = cylinder(pos=vector(-20, -Z0, 20), axis=vector(0, 8.75, 0), radius=1, color=color.green)
leg_3 = cylinder(pos=vector(0, -Z0, -20), axis=vector(0, 8.75, 0), radius=1, color=color.green)
platform.pos = vector(0, 0, 0)

# Create modbus client
client = ModbusClient()

# Running visualization
while client.isConnected():
    # Refresh rate
    rate(5)

    # Read modbus addresses for data
    response = client.read()
    x_pos = response[9]
    y_pos = response[11]
    pitch = response[13]
    roll = response[15]
    set_x_pos = response[17]
    set_y_pos = response[19]

    # Convert to radians
    pitch = translate(pitch, 0, 100, -8, 8)
    roll = translate(roll, 0, 100, -8, 8)
    pitch = pitch * pi / 180
    roll = roll * pi / 180

    # Map in values to range that fits platform
    x_pos = translate(x_pos, 15, 84, -25, 25)
    y_pos = translate(y_pos, 1, 98, -25, 25)

    # Calculate leg heights from transformation position matrix
    y1 = ((sqrt(3) * L) / 6) * sin(pitch) * cos(roll) + ((L / 2) * sin(roll)) + Z0
    y2 = ((sqrt(3) * L) / 6) * sin(pitch) * cos(roll) - ((L / 2) * sin(roll)) + Z0
    y3 = -((sqrt(3) * L) / 3) * sin(pitch) * cos(roll) + Z0

    # Assign data to visualization objects
    platform.up = vector(sin(roll), 1, sin(-pitch))
    leg_1.axis = vector(0, y2, 0)
    leg_2.axis = vector(0, y1, 0)
    leg_3.axis = vector(0, y3, 0)

    # Update ball position
    if x_pos == -25 and y_pos == -25:
        ball.visible = False
    else:
        ball.visible = True
        ball.pos = vector(x_pos, 1 + x_pos*sin(-roll) + y_pos*sin(pitch), y_pos)
