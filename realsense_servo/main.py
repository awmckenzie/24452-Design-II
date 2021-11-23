import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2
from adafruit_servokit import ServoKit

import servo
import config

def main():
    try:
        cfg = config.config() # init configuration
        ###########################################
        
        kit = ServoKit(channels=16)
        servos = []
        servo_targets = [0, 0, 0, 0, 0, 0, 0, 0] # 0 to 180 degrees
        depths = [0, 0, 0, 0, 0, 0, 0, 0] # 600 to 2000 mm
        
        servo.init_servos(servos, cfg['actuators'])
        ###########################################
        pipeline = rs.pipeline()

        rs_config = rs.config()
        rs_config.enable_stream(rs.stream.depth, cfg['x_res'], cfg['y_res'], rs.format.z16, cfg['fps'])

        frame_queue = rs.frame_queue(cfg['queue_size'], keep_frames=True)

        decimation_filter = rs.decimation_filter(cfg['decimation_level'])
        hole_filter = rs.hole_filling_filter()
        spatial_filter = rs.spatial_filter(0.5, 20, 5, 0)
        temporal_filter = rs.temporal_filter()
        depth2disparity = rs.disparity_transform()
        disparity2depth = rs.disparity_transform(False)

        pipeline.start(rs_config, frame_queue)
        #############################################

    finally:
        pipeline.stop()
        print('hi')

if __name__ == '__main__':
    main()