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
        'border_trunc':             10, # rows/cols to truncate

        'servo_zero_offset':         [5,  12,  15,  0,  0,  0,  0,  0]
    }
    return config