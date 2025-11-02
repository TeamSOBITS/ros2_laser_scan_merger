#
#   created by: Michael Jonathan (mich1342)
#   github.com/mich1342
#   24/2/2022
#
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
import launch_ros.actions
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    config_file_cmd = DeclareLaunchArgument(
        'config_file',
        default_value=os.path.join(
            get_package_share_directory('ros2_laser_scan_merger'),
            'config',
            'params.yaml'))
    remapping_param_point_cmd = DeclareLaunchArgument(
        'pointcloud_remapping',
        default_value="/cloud_in")
    remapping_param_scan_cmd = DeclareLaunchArgument(
        'scan_remapping',
        default_value="/scan")

    return LaunchDescription([
        config_file_cmd,
        remapping_param_point_cmd,
        remapping_param_scan_cmd,
        
        launch_ros.actions.Node(
            package='ros2_laser_scan_merger',
            executable='ros2_laser_scan_merger',
            parameters=[LaunchConfiguration('config_file')],
            output='screen',
            respawn=True,
            respawn_delay=2,
        ),

        launch_ros.actions.Node(
            name='pointcloud_to_laserscan',
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            remappings=[
                ('/cloud_in', LaunchConfiguration('pointcloud_remapping')),
                ('/scan', LaunchConfiguration('scan_remapping')),
            ],
            parameters=[LaunchConfiguration('config_file')],
        )
        
    ])
