import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2
from adafruit_servokit import ServoKit
import ipdb

import servo
import config

def main():
    try:
        cfg = config.config() # init configuration; all constants are stored in config.py

        ###########################################
        kit = ServoKit(channels=16)
        servos = []
        #servo_targets = [0, 0, 0, 0, 0, 0, 0, 0] # 0 to 180 degrees
        #depths = [0, 0, 0, 0, 0, 0, 0, 0] # 600 to 2000 mm
        
        servos = servo.init_servos(servos, cfg['actuators'], cfg['servo_zero_offset'])

        ###########################################
        pipeline = rs.pipeline()
        rs_config = rs.config()
        rs_config.enable_stream(rs.stream.depth, cfg['x_res'], cfg['y_res'], rs.format.z16, cfg['fps'])
        frame_queue = rs.frame_queue(cfg['queue_size'], keep_frames=True)

        ### initialize post processing filters
        decimation_filter_depth = rs.decimation_filter(cfg['depth_decimation_level'])
        decimation_filter_cv = rs.decimation_filter(cfg['cv_decimation_level'])

        # fill holes based on best guesses from neighboring values
        hole_filter = rs.hole_filling_filter()

        # smooth edges
        spatial_filter = rs.spatial_filter(0.5, 20, 5, 0)

        # time averaging
        temporal_filter = rs.temporal_filter(0.4, 20, 3) 

        # transform into 1/D domain to decrease depth noise
        depth2disparity = rs.disparity_transform()

        # transform back to D domain
        disparity2depth = rs.disparity_transform(False)

        ### start the camera
        pipeline.start(rs_config, frame_queue)

        #############################################

        # servos 7 6 5 4 = left of camera = right of depth map on screen
        # servos 3 2 1 0 = right of camera = left of depth map on screen
        # servos 0, 1, 4, 5 are mirrored

        while(True):
            frame = frame_queue.wait_for_frame()
            depth_frame = frame.as_frameset().get_depth_frame()
            depth_frame_filtered = depth_frame

            depth_frame_filtered = decimation_filter_depth.process(depth_frame_filtered)
            depth_frame_filtered = depth2disparity.process(depth_frame_filtered)
            depth_frame_filtered = spatial_filter.process(depth_frame_filtered)
            depth_frame_filtered = temporal_filter.process(depth_frame_filtered)
            depth_frame_filtered = disparity2depth.process(depth_frame_filtered)
            #depth_frame_filtered = hole_filter.process(depth_frame_filtered)

            depth_image = np.asanyarray(depth_frame_filtered.get_data())

            depths = np.zeros(cfg['actuators'])
            servo_targets = np.zeros(cfg['actuators'])
            counts = np.zeros(cfg['actuators'])

            ##### split depth map into 8 cols
            depth_image_split = np.hsplit(depth_image, cfg['actuators'])

            for i in range(cfg['actuators']):
                counts[i] = np.count_nonzero((depth_image_split[i] > cfg['min_dist']) & (depth_image_split[i] < cfg['max_dist']))

                if counts[i] > cfg['min_count']:
                    depth_image_split[i] = np.where((depth_image_split[i] > cfg['max_dist']), 0, depth_image_split[i])
                    depth_image_split[i] = np.where((depth_image_split[i] < cfg['min_dist']), 0, depth_image_split[i])
                    depths[i] = np.mean(depth_image_split[i][depth_image_split[i] != 0])
                    
                else:
                    if np.var(depth_image_split[i] > 3):
                        depths[i] = cfg['max_dist']
                    else:
                        depths[i] = cfg['min_dist']
                
                servo_targets[i] = servos[i].min_angle + round((servos[i].max_angle - servos[i].min_angle) * (cfg['max_dist'] - depths[i]) / (cfg['max_dist'] - cfg['min_dist']))

                #ipdb.set_trace()
            print(depths)
            for i in range(cfg['actuators']):
                servos[i].move(servo_targets[i])
            
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', depth_colormap)
            cv2.waitKey(1) # delay 1ms

    finally:
        pipeline.stop()
        print('pipeline stop')

if __name__ == '__main__':
    main()
