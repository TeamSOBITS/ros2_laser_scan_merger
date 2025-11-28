import os
import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterFile

def get_config_value(yaml_path, node_name, param_name, default_value):
    try:
        if not os.path.exists(yaml_path):
            return default_value
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
        return config.get(node_name, {}).get('ros__parameters', {}).get(param_name, default_value)
    except Exception as e:
        print(f"[WARN] Failed to read YAML for {node_name}.{param_name}: {e}")
        return default_value

def launch_setup(context, *args, **kwargs):
    robot_name = LaunchConfiguration('robot_name').perform(context)
    
    bringup_dir = get_package_share_directory('sobits_slam')
    config_file_path = os.path.join(bringup_dir, 'param', robot_name, 'sensor_fusion_config.yaml')

    configured_params = ParameterFile(config_file_path)

    cam_in_topic = get_config_value(config_file_path, '/camera_pointcloud_to_scan', 'remap_cloud_in_target', '/hsrb/head_rgbd_sensor/depth_registered/points')
    cam_out_topic = get_config_value(config_file_path, '/camera_pointcloud_to_scan', 'remap_scan_out_target', '/hsrb/camera_scan')
    
    final_pc_in_topic_default = get_config_value(config_file_path, '/ros2_laser_scan_merger', 'pointCloudTopic', '/cloud_in')
    final_pc_in_topic = get_config_value(config_file_path, '/pointcloud_to_laserscan', 'remap_cloud_in_target', final_pc_in_topic_default)
    final_scan_out_topic = get_config_value(config_file_path, '/pointcloud_to_laserscan', 'remap_scan_out_target', '/hsrb/merged_scan')

    camera_pc_to_scan_node = Node(
        package='pointcloud_to_laserscan', 
        executable='pointcloud_to_laserscan_node',
        name='camera_pointcloud_to_scan',  
        remappings=[
            ("cloud_in", cam_in_topic),
            ("scan", cam_out_topic)
        ],
        parameters=[configured_params],
        output='screen',
    )
    
    scan_merger_node = Node(
        package='ros2_laser_scan_merger',
        executable='ros2_laser_scan_merger',
        parameters=[configured_params],
        output='screen',
        respawn=True,
        respawn_delay=2.0,
    )

    final_pc_to_scan_node = Node(
        name='pointcloud_to_laserscan',
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        parameters=[configured_params],
        remappings=[
            ("cloud_in", final_pc_in_topic),
            ("scan", final_scan_out_topic)
        ],
        output='screen'
    )

    return [
        camera_pc_to_scan_node,
        scan_merger_node,
        final_pc_to_scan_node
    ]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('robot_name', default_value='hsr_sim'),
        OpaqueFunction(function=launch_setup)
    ])