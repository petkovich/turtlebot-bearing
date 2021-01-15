This ros node turns the turtlebot towards the nearest obstacle.
If there isn't any obstacle in proximity, it turns to hardcoded default bearing.

requirements:
git clone -b kinetic-devel https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git

optional:
sudo apt-get install ros-your_distro-teleop-twist-keyboard


open terminal:

export TURTLEBOT3_MODEL=burger
roslaunch turtlebot3_gazebo turtlebot3_house.launch 

in new window:

rosrun teleop_twist_keyboard teleop_twist_keyboard.py 

in new window:

rosrun turtlebot_orientation turtlebot_orientation.py