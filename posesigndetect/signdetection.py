from enum import IntEnum

import numpy as np
import cv2
import math

"""
Sign Detection Logic:

We're checking for the 8 signs, using the following logic:

1. Get keypoint coords (x, y) form the Pose Estimation model
2. Compute relative distance and direction of specific join from neck for each sign
3. Check if the joint is right or left of the neck and above or below the neck, and find the angle between the joint and the neck (angle found from relative distance - tan inverse function)
4. Depending on results from step-3 , the sign which corresponds to the image is found
"""

class MPIIPartMapping():
    """
    Mappings of body part names to model keypoint indices.
    """

    HEAD = 9
    NECK = 8

    LEFT_SHOULDER = 12
    RIGHT_SHOULDER = 13

    LEFT_ELBOW = 11
    RIGHT_ELBOW = 14

    LEFT_WRIST = 10
    RIGHT_WRIST = 15

    TORSO = 7
    PELVIS = 6

    LEFT_HIP = 2
    RIGHT_HIP = 3

    LEFT_KNEE = 1
    RIGHT_KNEE = 4

    LEFT_FOOT = 0
    RIGHT_FOOT = 5

class RelativeDirection(IntEnum):
    """
    Enum of basic directions from point A to point B. SAME indicates overlap.
    """

    ABOVE = 1
    BELOW = 2
    LEFT = 3
    RIGHT = 4
    SAME = 5

class Signs(IntEnum):
    """
    Enum of Signs.
    """

    UNK = -1
    N = 0
    Y = 1
    stationary = 2
    return_sign = 3
    go_left = 4
    go_right = 5
    investigate = 6
    proceed = 7

def relative_part_direction(point_1, point_2):
    """
    Compute Relative Direction of one 2D point from another.

    Args:
        point_1 (`np.ndarray` of shape [2]): Coordinates of Point 1.
        point_2 (`np.ndarray` of shape [2]): Coordinates of Point 2.

    Returns:
        Relative distance between point_1 and point_2.
        `RelativeDirection`: Relative Direction of Point 1 from Point 2, as a member of
            `RelativeDirection` enum.
    """

    diff_vector = point_2 - point_1
    relative_dist = [diff_vector[0], diff_vector[1]]
    direction = [None, None]

    if (diff_vector[0] < 0):
        direction[0] = RelativeDirection.RIGHT
    elif (diff_vector[0] > 0):
        direction[0] = RelativeDirection.LEFT
    else:
        direction[0] = RelativeDirection.SAME

    if (diff_vector[1] < 0):
        direction[1] = RelativeDirection.BELOW
    elif (diff_vector[1] > 0):
        direction[1] = RelativeDirection.ABOVE
    else:
        direction[1] = RelativeDirection.SAME

    return relative_dist, direction

def sign_detector(keypoints):
    """
    Detect the Sign a person, represented by keypoints, is holding using the logic describe at top
    of module.

    Args:
        keypoints (`np.ndarray` of shape [16, 2]): MPII Keypoint coordinates.

    Returns:
        `Signs`: Detected sign as a member of `Signs` enum.
    """

    # Ensure it's MPII Keypoints
    assert (len(keypoints.shape) == 2)
    assert (keypoints.shape[0] == 16 and keypoints.shape[1] == 2)

    left_wrist_loc = keypoints[MPIIPartMapping.LEFT_WRIST]
    right_wrist_loc = keypoints[MPIIPartMapping.RIGHT_WRIST]
    neck_loc = keypoints[MPIIPartMapping.NECK]

    left_relative_dist, left_wrist_neck_dir = relative_part_direction(left_wrist_loc, neck_loc)
    right_relative_dist, right_wrist_neck_dir = relative_part_direction(right_wrist_loc, neck_loc)
    
    y_sign = (
        (left_wrist_neck_dir[0] == RelativeDirection.LEFT and
        left_wrist_neck_dir[1] == RelativeDirection.ABOVE and
        right_wrist_neck_dir[0] == RelativeDirection.RIGHT and
        right_wrist_neck_dir[1] == RelativeDirection.ABOVE and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > 30 and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < 60 and
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > 120 and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < 150)
        or 
        (left_wrist_neck_dir[0] == RelativeDirection.RIGHT and
        left_wrist_neck_dir[1] == RelativeDirection.ABOVE and
        right_wrist_neck_dir[0] == RelativeDirection.LEFT and
        right_wrist_neck_dir[1] == RelativeDirection.ABOVE and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > 30 and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < 60 and
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > 120 and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < 150)
    )

    n_sign = (
        (left_wrist_neck_dir[0] == RelativeDirection.LEFT and
        left_wrist_neck_dir[1] == RelativeDirection.ABOVE and
        right_wrist_neck_dir[0] == RelativeDirection.RIGHT and
        right_wrist_neck_dir[1] == RelativeDirection.BELOW and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > 30 and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < 60 and
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > -150 and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < -120)
        or 
        (left_wrist_neck_dir[0] == RelativeDirection.RIGHT and
        left_wrist_neck_dir[1] == RelativeDirection.BELOW and
        right_wrist_neck_dir[0] == RelativeDirection.LEFT and
        right_wrist_neck_dir[1] == RelativeDirection.ABOVE and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > 30 and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < 60 and
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > -150 and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < -120)
    )
    
    return_sign = (
        (left_wrist_neck_dir[0] == RelativeDirection.LEFT and 
        left_wrist_neck_dir[1] == RelativeDirection.ABOVE and 
        right_wrist_neck_dir[0] == RelativeDirection.RIGHT and 
        right_wrist_neck_dir[1] == RelativeDirection.BELOW and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > 60 and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < 100 and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > -120 and
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < -60)
        or 
        (left_wrist_neck_dir[0] == RelativeDirection.RIGHT and 
        left_wrist_neck_dir[1] == RelativeDirection.ABOVE and 
        right_wrist_neck_dir[0] == RelativeDirection.LEFT and 
        right_wrist_neck_dir[1] == RelativeDirection.BELOW and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > 60 and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < 100 and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > -120 and
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < -60)
    )

    stationary_sign = (
        ((((np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > -190 and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < -160) or 
        ((np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > 160 and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < 190)) and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > -20 and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < 25)
        or 
        ((((np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > -190 and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < -160) or 
        ((np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > 160 and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < 190)) and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > -20 and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < 25)
    )

    investigate_sign = (
        (left_wrist_neck_dir[0] == RelativeDirection.LEFT and 
        left_wrist_neck_dir[1] == RelativeDirection.BELOW and 
        right_wrist_neck_dir[0] == RelativeDirection.RIGHT and 
        right_wrist_neck_dir[1] == RelativeDirection.BELOW and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > -55 and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < -35 and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > -155 and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < -120)
        or 
        (left_wrist_neck_dir[0] == RelativeDirection.RIGHT and 
        left_wrist_neck_dir[1] == RelativeDirection.BELOW and 
        right_wrist_neck_dir[0] == RelativeDirection.LEFT and 
        right_wrist_neck_dir[1] == RelativeDirection.BELOW and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > -55 and 
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < -35 and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > -155 and 
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < -120)
    )

    proceed_further = (
        (left_wrist_neck_dir[0] == RelativeDirection.LEFT and
        left_wrist_neck_dir[1] == RelativeDirection.ABOVE and
        right_wrist_neck_dir[0] == RelativeDirection.RIGHT and
        right_wrist_neck_dir[1] == RelativeDirection.ABOVE and
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > 60 and
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < 100 and
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > 90 and
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < 130)
        or 
        (left_wrist_neck_dir[0] == RelativeDirection.LEFT and
        left_wrist_neck_dir[1] == RelativeDirection.ABOVE and
        right_wrist_neck_dir[0] == RelativeDirection.RIGHT and
        right_wrist_neck_dir[1] == RelativeDirection.ABOVE and
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > 60 and
        (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < 100 and
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > 90 and
        (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < 130)
    )

    go_left = (
        ((left_wrist_neck_dir[0] == RelativeDirection.LEFT and 
        left_wrist_neck_dir[1] == RelativeDirection.SAME and 
        right_wrist_neck_dir[0] == RelativeDirection.RIGHT and 
        right_wrist_neck_dir[1] == RelativeDirection.BELOW) or 
        ((np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > -25 and
         (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < 25 and
         (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > -150 and
         (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < -100))
        or 
        ((left_wrist_neck_dir[0] == RelativeDirection.LEFT and 
         left_wrist_neck_dir[1] == RelativeDirection.SAME and 
        right_wrist_neck_dir[0] == RelativeDirection.RIGHT and 
        right_wrist_neck_dir[1] == RelativeDirection.BELOW) or 
        ((np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > -25 and 
         (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < 25 and 
         (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > -150 and 
         (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < -100))
    )

    go_right = (
        ((right_wrist_neck_dir[0] == RelativeDirection.RIGHT and 
        right_wrist_neck_dir[1] == RelativeDirection.SAME and 
        left_wrist_neck_dir[0] == RelativeDirection.LEFT and 
        left_wrist_neck_dir[1] == RelativeDirection.BELOW) or
        ((((np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > 150 and
         (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < 190) or
         ((np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > -190 and
         (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < -150)) and
         (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > -100 and
         (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < -50))
        or 
        ((right_wrist_neck_dir[0] == RelativeDirection.RIGHT and 
        right_wrist_neck_dir[1] == RelativeDirection.SAME and 
        left_wrist_neck_dir[0] == RelativeDirection.LEFT and 
        left_wrist_neck_dir[1] == RelativeDirection.BELOW) or 
        ((np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) > -100 and 
         (np.arctan2(right_relative_dist[1], right_relative_dist[0])*180/np.pi) < -55 and 
         (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) > -190 and 
         (np.arctan2(left_relative_dist[1], left_relative_dist[0])*180/np.pi) < -150))
    )

    if y_sign : 
        return Signs.Y
    if n_sign : 
        return Signs.N
    if stationary_sign : 
        return Signs.stationary
    if return_sign : 
        return Signs.return_sign
    if investigate_sign : 
        return Signs.investigate
    if proceed_further : 
        return Signs.proceed
    if go_left : 
        return Signs.go_left
    if go_right : 
        return Signs.go_right

    return Signs.UNK

"""
==========
Drawing functionality
==========
"""

signs_display = {
    Signs.Y : {"text" : "Help needed", "color" : [0, 255, 0]}, 
    Signs.N : {"text" : "Help not needed", "color" : [0, 0, 255]}, 
    Signs.stationary : {"text" : "Remain stationary", "color" : [253, 255, 24]}, 
    Signs.return_sign : {"text" : "Return to shore", "color" : [254, 249, 27]}, 
    Signs.proceed : {"text" : "Proceed further out to sea", "color" : [234, 99, 3]}, 
    Signs.investigate : {"text" : "Investigate submerged object", "color" : [253, 255, 24]}, 
    Signs.go_left : {"text" : "Go left", "color" : [118, 90, 168]}, 
    Signs.go_right : {"text" : "Go right", "color" : [253, 255, 24]}, 
    Signs.UNK : {"text": "", "color": [0, 0, 0]}
}

def draw_sign(image, sign, font=cv2.FONT_HERSHEY_PLAIN, fontsize=1.2, thickness=2):
    sign_position = (5, image.shape[0] // 2)
    cv2.putText(image, signs_display[sign]["text"], sign_position, font, fontsize, signs_display[sign]["color"], thickness=thickness)
