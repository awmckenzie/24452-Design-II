def config():
    config = {
        'actuators':                8,
        'x_res':                    1280,
        'y_res':                    720,
        'fps':                      30,

        'queue_size':               1,
        'depth_decimation_level':   5,
        'cv_decimation_level':      2,
        'min_count':                .10, # % of the column that needs to be valid
        'min_dist':                 600,
        'max_dist':                 2000,
        'border_trunc':             8, # rows/cols to truncate, must be multiple of 8

        'servo_zero_offset':         [15,  22,  25,  0,  0,  0,  0,  0]
    }
    return config