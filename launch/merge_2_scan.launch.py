import os
import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def parse_yaml_for_remappings(yaml_path):
    remappings = {
        'cloud_in_target': '/hsrb/head_rgbd_sensor/depth_registered/points',
        'cam_scan_target': '/hsrb/camera_scan',
        'merged_pc_topic': '/hsrb/merged_cloud',
        'final_scan_target': '/hsrb/merged_scan'
    }
    try:
        with open(yaml_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        cam_params = config_data.get('/camera_pointcloud_to_scan', {}).get('ros__parameters', {})
        remappings['cloud_in_target'] = cam_params.get('remap_cloud_in_target', remappings['cloud_in_target'])
        remappings['cam_scan_target'] = cam_params.get('remap_scan_out_target', remappings['cam_scan_target'])

        merger_params = config_data.get('/ros2_laser_scan_merger', {}).get('ros__parameters', {})
        remappings['merged_pc_topic'] = merger_params.get('pointCloudTopic', remappings['merged_pc_topic'])

        final_pc_params = config_data.get('/pointcloud_to_laserscan', {}).get('ros__parameters', {})
        final_pc_in_target = final_pc_params.get('remap_cloud_in_target', remappings['merged_pc_topic'])
        remappings['merged_pc_topic'] = final_pc_in_target
        remappings['final_scan_target'] = final_pc_params.get('remap_scan_out_target', remappings['final_scan_target'])

    except Exception as e:
        print(f"[WARN] Failed to parse YAML: {e}")
    return remappings

def launch_setup(context, *args, **kwargs):
    robot_name = LaunchConfiguration('robot_name').perform(context)
    
    bringup_dir = get_package_share_directory('sobits_slam')
    config_file_path = os.path.join(bringup_dir, 'param', robot_name, 'slamtool_config.yaml')
    remap_data = parse_yaml_for_remappings(config_file_path)

    camera_pc_to_scan_node = Node(
        package='pointcloud_to_laserscan', 
        executable='pointcloud_to_laserscan_node',
        name='camera_pointcloud_to_scan',  
        remappings=[
            ("cloud_in", remap_data['cloud_in_target']),
            ("scan", remap_data['cam_scan_target'])
        ],
        parameters=[config_file_path],
        output='screen',
    )
    
    scan_merger_node = Node(
        package='ros2_laser_scan_merger',
        executable='ros2_laser_scan_merger',
        parameters=[config_file_path],
        output='screen',
        respawn=True,
        respawn_delay=2.0,
    )

    final_pc_to_scan_node = Node(
        name='pointcloud_to_laserscan',
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        parameters=[config_file_path],
        remappings=[
            ("cloud_in", remap_data['merged_pc_topic']),
            ("scan", remap_data['final_scan_target'])
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