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
        #servo_targets = [0, 0, 0, 0, 0, 0, 0, 0] # 0 to 180 degrees
        #depths = [0, 0, 0, 0, 0, 0, 0, 0] # 600 to 2000 mm
        
        servos = servo.init_servos(servos, cfg['actuators'])
        ###########################################
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

        i_iter = int(cfg['y_res']/cfg['depth_decimation_level'])
        j_iter = int(cfg['x_res']/cfg['depth_decimation_level'])
        #############################################

        while(True):
            frame = frame_queue.wait_for_frame()
            depth_frame = frame.as_frameset().get_depth_frame()
            depth_frame_filtered = depth_frame
            #depth_frame_cv = depth_frame

            depth_frame_filtered = decimation_filter_depth.process(depth_frame_filtered)
            depth_frame_filtered = depth2disparity.process(depth_frame_filtered)
            depth_frame_filtered = spatial_filter.process(depth_frame_filtered)
            depth_frame_filtered = temporal_filter.process(depth_frame_filtered)
            depth_frame_filtered = disparity2depth.process(depth_frame_filtered)
            #depth_frame_filtered = hole_filter.process(depth_frame_filtered)

            #depth_frame_cv = decimation_filter_cv.process(depth_frame_cv)

            depth_image = np.asanyarray(depth_frame_filtered.get_data())
            #depth_image_cv = np.asanyarray(depth_frame_cv.get_data())

            depths = np.zeros(cfg['actuators'])
            servo_targets = np.zeros(cfg['actuators'])
            counts = np.zeros(cfg['actuators'])

            # depth_filtered = depth_image > cfg['min_dist'] and depth_image < cfg['max_dist']
            depth_image_split = np.hsplit(depth_image, cfg['actuators'])
            for i in range(cfg['actuators']):
                depth_filtered = np.where((depth_image_split[i] < cfg['max_dist']) & (depth_image_split[i] > cfg['min_dist']), depth_image_split[i], 0)
                counts[i] = np.count_nonzero(depth_filtered)
                if counts[i] > 0:
                    depths[i] = np.mean(depth_filtered[depth_filtered != 0])
            # for i in range(i_iter):
            #     for j in range(j_iter):
            #         if depth_image[i,j] < cfg['max_dist'] and depth_image[i,j] > cfg['min_dist']:
            #             div = int(j_iter/cfg['actuators'])
            #             ind = j//div
            #             depths[ind] += depth_image[i,j]
            #             counts[ind] += 1



            for i in range(cfg['actuators']):
                if counts[i] > cfg['min_count']:
                    servo_targets[i] = round(90 * (depths[i] - cfg['min_dist']) / (cfg['max_dist'] - cfg['min_dist']))
            print(servo_targets)

            for i in range(cfg['actuators']):
                servos[i].move(servo_targets[i])
            
            #depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_cv, alpha=0.03), cv2.COLORMAP_JET)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', depth_colormap)
            cv2.waitKey(1)

    finally:
        pipeline.stop()
        print('hi')

if __name__ == '__main__':
    main()