# Use ROS2 Rolling Desktop base image
FROM osrf/ros:rolling-desktop

# Install necessary ROS2 and Gazebo packages
RUN apt update && apt install -y \
    ros-rolling-gazebo-ros-pkgs \
    ros-rolling-ros-controllers \
    ros-rolling-gazebo-ros-control \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /root/ros2_ws
WORKDIR /root/ros2_ws

# Copy the contents of your RoboGardener repository into the container
COPY . /root/ros2_ws/src

# Source ROS2 and build the workspace
RUN /bin/bash -c "source /opt/ros/rolling/setup.bash && colcon build"

# Set the default command to open a bash shell when the container is run
ENTRYPOINT ["/bin/bash"]
