def config():
    config = {
        'actuators':                8,
        'x_res':                    1280,
        'y_res':                    720,
        'fps':                      30,

        'queue_size':               1,
        'depth_decimation_level':   5,
        'cv_decimation_level':      4,
        'min_count':                200,

        'min_dist':                 600,
        'max_dist':                 2000,

        'servo_zero_offset':         [5,  12,  15,  0,  0,  0,  0,  0]
    }
    return config