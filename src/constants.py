controller_rate = 30 # 30Hz is enough for this turtlebot
default_bearing = 1.0 #if there is no object nearby, orientate towards 1 radian
control_min_threshold = 0.1 #radian, don't move if close enough
control_max_threshold = 0.4 #radian, don't move too fast
range_threshold = 1.0 #only turn to really close object