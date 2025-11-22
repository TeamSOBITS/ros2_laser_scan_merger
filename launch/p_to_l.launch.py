import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    merger_launch_file = os.path.join(
        get_package_share_directory('ros2_laser_scan_merger'),
        'launch',
        'merge_2_scan.launch.py'
    )

    return LaunchDescription([
        Node(
            package='pointcloud_to_laserscan', 
            executable='pointcloud_to_laserscan_node',
            name='camera_pointcloud_to_scan',  

            remappings=[
                ('cloud_in', '/hsrb/head_rgbd_sensor/depth_registered/points'),
                ('scan', '/camera_scan') 
            ],

            parameters=[{
                'target_frame': 'base_range_sensor_link', 
                'min_height': 0.05, 
                'max_height': 1.0, 
                'angle_min': -1.57, 
                'angle_max': 1.57, 
                'angle_increment': 0.0087, 
                'range_min': 0.2, 
                'range_max': 10.0, 
                'use_inf': True,

                # QoS override 設定
                'qos_overrides': {
                    '/hsrb/head_rgbd_sensor/depth_registered/points': {
                        'subscription': {
                            'depth': 1,
                            'reliability': 'reliable',
                            'durability': 'volatile'
                        }
                    },
                    '/camera_scan': {
                        'publisher': {
                            'depth': 1,
                            'reliability': 'best_effort',
                            'durability': 'volatile'
                        }
                    }
                }
            }],
            output='screen',
        )
        ,
        # Include the laser scan merger launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(merger_launch_file)
        )
    ])
