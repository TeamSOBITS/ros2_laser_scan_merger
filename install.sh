#!/bin/bash

echo "╔══╣ Install: ROS2 Laser Scan Merger (STARTING) ╠══╗"


# Install ROS packages
sudo apt-get update
sudo apt-get install -y \
    ros-${ROS_DISTRO}-pointcloud-to-laserscan


echo "╚══╣ Install: ROS2 Laser Scan Merger (FINISHED) ╠══╝"