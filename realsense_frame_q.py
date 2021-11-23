import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2
import time as t

actuators = 8
x_res = 640
y_res = 480
fps = 30
queue_size = 50
decimation_level = 1
min_dist = 600
max_dist = 2000

i_iter = int(y_res/decimation_level)
j_iter = int(x_res/decimation_level)

# def check_distance
try:
    pipeline = rs.pipeline()

    config = rs.config()
    config.enable_stream(rs.stream.depth, x_res, y_res, rs.format.z16, fps)

    frame_queue = rs.frame_queue(queue_size, keep_frames=True)

    decimation_filter = rs.decimation_filter(decimation_level)
    hole_filter = rs.hole_filling_filter()
    spatial_filter = rs.spatial_filter(0.5, 20, 5, 0)
    temporal_filter = rs.temporal_filter()
    depth2disparity = rs.disparity_transform()
    disparity2depth = rs.disparity_transform(False)
    

    pipeline.start(config, frame_queue)
    #pipeline.start(config)
    count = 0
    q_time_avg = 0
    filter_time_avg = 0
    loop_time_avg = 0
    open_cv_time_avg = 0

    while(True):
        t1 = t.time()
        #print(t1)
        frame = frame_queue.wait_for_frame()
        #frame = pipeline.wait_for_frames()
        depth_frame = frame.as_frameset().get_depth_frame()
        #depth_frame = frame.get_depth_frame()
        t2 = t.time() # time to queue
        depth_frame_filtered = depth_frame

        depth_frame_filtered = decimation_filter.process(depth_frame_filtered)
        depth_frame_filtered = depth2disparity.process(depth_frame_filtered)
        depth_frame_filtered = spatial_filter.process(depth_frame_filtered)
        depth_frame_filtered = temporal_filter.process(depth_frame_filtered)
        depth_frame_filtered = disparity2depth.process(depth_frame_filtered)
        depth_frame_filtered = hole_filter.process(depth_frame_filtered)

        t3 = t.time() # time to filter
        depth_image = np.asanyarray(depth_frame_filtered.get_data())
        # for i in range(i_iter):
        #     for j in range(j_iter):
        #           ind = (i,j)
                # if type(depth_image[i,j]) is not np.uint16:
                #     depth_image[i,j] = 0
#                if depth_image[i,j] > max_dist or depth_image[i,j] < min_dist:
#                    depth_image[i,j] = 0
        t4 = t.time() # loop time

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', depth_colormap)
        cv2.waitKey(1)
        t5 = t.time()
        #print(t5)
        #print()
        q_time_avg += t2-t1
        filter_time_avg += t3-t2
        loop_time_avg += t4-t3
        open_cv_time_avg += t5-t4
        count += 1
finally:
    pipeline.stop()
    q_time_avg = q_time_avg/count
    filter_time_avg = filter_time_avg/count
    loop_time_avg = loop_time_avg/count
    open_cv_time_avg = open_cv_time_avg/count
    total_time = q_time_avg + filter_time_avg + loop_time_avg + open_cv_time_avg
    print(q_time_avg, filter_time_avg, loop_time_avg, open_cv_time_avg, total_time)
    print('pipeline stop')
