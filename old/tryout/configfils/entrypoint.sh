#!/bin/bash

# This script sets up the runtime environment, sources necessary scripts, 
# sets environment variables, and handles DDS configurations.
# It acts as an executable wrapper for running commands within the ROS environment.
# The script also enables error signals, sources the ROS installation, 
# prints passed arguments, and executes them.

# Exit immediately if a command exits with a non-zero status
set -e

# Source the ROS 2 setup script
if [ -f /opt/ros/humble/setup.bash ]; then
  source /opt/ros/humble/setup.bash
fi

# Source the colcon argument completion script
if [ -f /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash ]; then
  source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash
else
  echo "Warning: /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash not found"
fi

# Print the provided arguments
echo "Provided arguments: $@"

# Execute the provided command or fall back to bash
exec "$@"