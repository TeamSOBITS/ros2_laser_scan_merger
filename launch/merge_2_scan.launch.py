#
#   created by: Michael Jonathan (mich1342)
#   github.com/mich1342
#   24/2/2022
#

from launch import LaunchDescription
import launch_ros.actions

from ament_index_python.packages import get_package_share_directory
import os
def generate_launch_description():


    config = os.path.join(
        get_package_share_directory('ros2_laser_scan_merger'),
        'config',
        'params.yaml'
    )
    
    return LaunchDescription([
        # --- LaserScan Merger Node ---
        launch_ros.actions.Node(
            package='ros2_laser_scan_merger',
            executable='ros2_laser_scan_merger',
            parameters=[config],
            output='screen',
            respawn=True,
            respawn_delay=2,
        ),

        launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher_laser',
            output='screen',
            parameters=[config],
            namespace='static_transform_publisher'
        ),

        # --- PointCloud to LaserScan for final merged output ---
        launch_ros.actions.Node(
            name='pointcloud_to_laserscan',
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            parameters=[config]
        ),
    ])
