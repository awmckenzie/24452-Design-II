import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)


try:
    actuators = 8
    div = 160/8
    pipe = rs.pipeline()

    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)

    pipe.start(config)

    decimate = rs.decimation_filter(4)
    # spatial = rs.spatial_filter()
    # disparity = rs.disparity_transform()
    # temporal = rs.temporal_filter()
    # hole_fill = rs.hole_filling_filter()
    print()
    while True:
        frames = pipe.wait_for_frames()

        depth_frame = frames.get_depth_frame()

        depth_frame = decimate.process(depth_frame)
        # depth_frame = disparity.process(depth_frame)
        # depth_frame = spatial.process(depth_frame)
        # depth_frame = temporal.process(depth_frame)
        # depth_frame = disparity.process(depth_frame, transform_to_disparity=False)
        # depth_frame = hole_fill.process(depth_frame)

        depth_image = np.asanyarray(depth_frame.get_data())
        sums = np.zeros(8)
        counts = np.zeros(8)
        # print(depth_image)
        for i in range(120):
            for j in range(160):
                if type(depth_image[i,j]) is not np.uint16:
                    depth_image[i,j] = 0
                if depth_image[i,j] > 2000 or depth_image[i,j] < 600:
                    depth_image[i,j] = 0
                
                ind = int(j//div)
                if depth_image[i,j] != 0:
                    counts[ind] += 1
                    sums[ind] += depth_image[i,j]
        for i in range(actuators):
            if counts[i] > 0:
                sums[i] = int(sums[i] / counts[i])
        print(sums)
        # weight by the size of count, 1 point with valid depth value should not be counted

	# servo actuation for just 2 servos for now
        maxDepth = 1999
        for i in range(2):
            kit.servo[i].angle = sums[i]*180/maxDepth

        # depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('RealSense', depth_colormap)
        # cv2.waitKey(1)


finally:
    print('pipeline stop')
    pipe.stop()
