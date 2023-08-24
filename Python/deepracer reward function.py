import math

def reward_function(params):
    if params["is_offtrack"]:
        return -1e4
    
    if abs(params["steering_angle"]) > 20:
        return -1000.
    
    if not params["all_wheels_on_track"]:
        return -100.
        
    w1_x, w1_y = params["waypoints"][params["closest_waypoints"][1]]
    w0_x, w0_y = params["waypoints"][params["closest_waypoints"][0]]
    
    # Calculating angle of the road
    delta_y = w1_y - w0_y
    delta_x = w1_x - w0_x
    if delta_x==0: delta_x = 1e-6
    
    wp_angle = math.degrees(math.atan(delta_y/delta_x))
    
    if delta_x<0:
        if wp_angle<=0:
            wp_angle += 180
        elif wp_angle>0:
            wp_angle -= 180
    # wp_angle -> current angle of the road
    
    car_angle = params["heading"]
    speed = params["speed"]
    
    # angle diff between car and waypoint
    angle = abs(car_angle-wp_angle)
    angle = min(angle, 360-angle)
    
    reward = 1000 * speed * (params["progress"]/params["steps"]) - angle
    return reward if reward!=0 else 1e-3


# ------------------------------------------------------------------------------------------------------------------

# def angle(x2, y2, x1, y1):
#     delta_y = y2 - y1
#     delta_x = x2 - x1
#     if delta_x==0: delta_x = 1e-6
    
#     wp_angle = math.degrees(math.atan(delta_y/delta_x))
    
#     if delta_x<0:
#         if wp_angle<=0:
#             wp_angle += 180
#         elif wp_angle>0:
#             wp_angle -= 180
            
#     print(wp_angle)
    
# angle(2.2, 7, 7.18, 5.84)