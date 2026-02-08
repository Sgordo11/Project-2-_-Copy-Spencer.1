#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 12:37:32 2021

@author: kendrick shepherd
"""

import sys

import Geometry_Operations as geom

# Determine the unknown bars next to this node
def UnknownBars(node):
    list_of_unknown_bars = []
    for bar in node.bars:
        if bar.is_computed == False:
            list_of_unknown_bars.append(bar)
    return list_of_unknown_bars

# Determine if a node if "viable" or not
def NodeIsViable(node):
    unknown = UnknownBars(node)
    if unknown == 1 or 2:
        return True
    else:
        return False


# Compute unknown force in bar due to sum of the
# forces in the x direction
def SumOfForcesInLocalX(node, unknown_bars):
    local_x_bar = unknown_bars[0]
    other_bar = unknown_bars[1]
    local_x_vector = geom.BarNodeToVector(node, local_x_bar)

    my_sum = 0
    x_forces = node.GetNetXForce()
    # get the x force created by Dr.Shepard
    y_forces = node.GetNetYForce()

    global_x_dir = [1, 0]
    global_y_dir = [0, 1]

    my_sum += x_forces * geom.CosineVectors(local_x_vector, global_x_dir)
    my_sum += y_forces * geom.CosineVectors(local_x_vector, global_y_dir)

    for bar in node.bars:
        if bar.is_computed == True:
            bar_force = bar.axial_load
            cosine_of_bars = geom.CosineBars(local_x_bar, bar)
            my_sum += bar_force * cosine_of_bars

    force_other = -my_sum / geom.CosineBars(local_x_bar, other_bar)

    other_bar.SetAxialLoad(force_other)

    other_bar.is_computed = True


# Compute unknown force in bar due to sum of the 
# forces in the y direction
def SumOfForcesInLocalY(node, unknown_bars):
    local_x_bar = unknown_bars[0]
    other_bar = unknown_bars[1]
    local_x_vector = geom.BarNodeToVector(node, local_x_bar)

    my_sum = 0
    x_forces = node.GetNetXforce()
    # get the x force created by Dr.Shepard
    y_forces = node.GetNetYforce()

    global_x_dir = [1, 0]
    global_y_dir = [0, 1]

    my_sum += x_forces * geom.SineVectors(local_x_vector, global_x_dir)
    my_sum += y_forces * geom.SineVectors(local_x_vector, global_y_dir)

    for bar in node.bars:
        if bar.is_computed == True:
            bar_force = bar.axial_load
            sin_of_bars = geom.SineBars(local_x_bar, bar)
            my_sum += bar_force * sin_of_bars

    force_other = -my_sum/geom.SineBars(other_bar, local_x_bar)

    other_bar.SetAxialLoad(force_other)

    other_bar.is_computed = True

    # how do i get my other unknown bar
    # given the other unknown bar how do i get the sine of the angle
    # the local x direction in the other unknown bar

# Check if any member has an unknown force ... if so, return true
# Nodes is a lost of all the nodes in my truss
def DoIHaveAnUnkownMember(nodes):

    for node in nodes:
        unknown_bars = UnknownBars(node)
        if len(unknown_bars) > 0:
            return True
    return False
            
    
# Perform the method of joints on the structure
def IterateUsingMethodOfJoints(nodes,bars):
    counter = 0
    while DoIHaveAnUnkownMember(nodes) == True:
        for node in nodes:
            if NodeIsViable(node) == True:
                unknown_bars = UnknownBars(node)
                if len(unknown_bars) == 2:
                    SumOfForcesInLocalY(node, unknown_bars)
                SumOfForcesInLocalX(node, unknown_bars)
        counter +=1
        if counter > len(nodes) + 1:
            sys.exit("Too many iterations")
    return bars