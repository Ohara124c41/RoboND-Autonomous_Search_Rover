import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function

def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if Rover.picking_up:
        Rover.throttle = 0

    elif Rover.near_sample and not Rover.picking_up:
        if Rover.vel == 0:
            Rover.brake = 0
            Rover.send_pickup = True
        else:
            Rover.throttle = 0
            Rover.brake = Rover.brake_set

    elif Rover.rock_angles is not None and len(Rover.rock_angles) > 1:
        Rover.throttle = 0.05
        # Set steering to average angle clipped to the range +/- 15
        Rover.steer = np.clip(np.mean(Rover.rock_angles * 180 / np.pi), -10, 10) ## changed

    elif Rover.nav_angles is not None:

        # Check for Rover.mode status
        if Rover.mode == 'FORWARD':
            print('FORWARD MODE')
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:
                # If mode is forward, navigable terrain looks good
                # and velocity is below max, then throttle
                if Rover.vel < 0.01 and Rover.throttle != 0:
                    Rover.brake = 0
                    Rover.mode = 'OBSTRUCTED'
                elif Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                    # Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -10, 10)

                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -10, 10) ## changed
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'STOP'
            elif Rover.steer > 5:
                Rover.count += 1

            elif Rover.steer <= 5:
                Rover.count = 0

            elif Rover.count > 100:
                Rover.mode = 'looping'

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'STOP':
            print('STOP MODE')
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -10 ## changed # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'FORWARD'

        elif Rover.mode == 'OBSTRUCTED':
            print('OBSTRUCTED')
            Rover.brake = 0
            Rover.throttle = 0
            Rover.steer = -10 ##15
            Rover.mode = 'FORWARD'

        elif Rover.mode == 'looping':
            print('LOOPING')
            Rover.count = 0
            Rover.throttle = 0
            Rover.steer = -10 ##15
            Rover.brake = 0
            Rover.count += 1
            if Rover.count > 50:
                Rover.mode = 'FORWARD'
                Rover.count = 0

    # Just to make the rover do something
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0

    return Rover

