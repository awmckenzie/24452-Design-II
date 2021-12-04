def config():
    config = {
        'actuators':                8,
        'x_res':                    1280,
        'y_res':                    720,
        'fps':                      30,

        'queue_size':               1,
        'depth_decimation_level':   6,
        'cv_decimation_level':      4,
        'min_count':                50,

        'min_dist':                 600,
        'max_dist':                 2000,

        'servo_min_angles':         [0,  0,  0,  0,  0,  0,  0,  0],
        'servo_max_angles':         [90, 90, 90, 90, 90, 90, 90, 90]
    }
    return config