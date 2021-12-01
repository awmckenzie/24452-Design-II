import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2
from adafruit_servokit import ServoKit

import servo
import config

opposite = {7,6,3,2}

def main():
    try:
        cfg = config.config() # init configuration; all constants are stored in config.py

        ###########################################
        # servo initiation
        kit = ServoKit(channels=16)
        servos = []
        #servo_targets = [0, 0, 0, 0, 0, 0, 0, 0] # 0 to 180 degrees
        #depths = [0, 0, 0, 0, 0, 0, 0, 0] # 600 to 2000 mm
        
        servos = servo.init_servos(servos, cfg['actuators'])

        ###########################################
        # intel realsense initiation
        pipeline = rs.pipeline()

        rs_config = rs.config()
        rs_config.enable_stream(rs.stream.depth, cfg['x_res'], cfg['y_res'], rs.format.z16, cfg['fps'])

        frame_queue = rs.frame_queue(cfg['queue_size'], keep_frames=True)

        decimation_filter_depth = rs.decimation_filter(cfg['depth_decimation_level'])
        decimation_filter_cv = rs.decimation_filter(cfg['cv_decimation_level'])
        hole_filter = rs.hole_filling_filter()
        spatial_filter = rs.spatial_filter(0.5, 20, 5, 0)
        temporal_filter = rs.temporal_filter()
        depth2disparity = rs.disparity_transform()
        disparity2depth = rs.disparity_transform(False)

        pipeline.start(rs_config, frame_queue)

        #############################################

        # servos 7 6 5 4 = left of camera = right of depth map on screen
        # servos 3 2 1 0 = right of camera = left of depth map on screen
        # servos 7 6 opposite orientation
        # servos 5 4 normal orientation

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
            	# if any of the column's depths (> max dist) or (< min dist), change value to zero
                depth_filtered = np.where((depth_image_split[i] < cfg['max_dist']) & (depth_image_split[i] > cfg['min_dist']), depth_image_split[i], 0)
                
       			# if column has nonzero depth, take avg of col and return
                counts[i] = np.count_nonzero(depth_filtered)
                if counts[i] > 0:
                    depths[i] = np.mean(depth_filtered[depth_filtered != 0])

            ##### calculate servo angle
            for i in range(cfg['actuators']):
            	if counts[i] > cfg['min_count']:
                    servo_targets[i] = round(90 * (depths[i] - cfg['min_dist']) / (cfg['max_dist'] - cfg['min_dist']))
                if i in opposite:
                	servo_targets[i] = -servo_targets[i] + 90

            print(servo_targets)

            for i in range(cfg['actuators']):
                servos[i].move(servo_targets[i])
            
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', depth_colormap)
            cv2.waitKey(1)

    finally:
        pipeline.stop()
        print('hi')

if __name__ == '__main__':
    main()