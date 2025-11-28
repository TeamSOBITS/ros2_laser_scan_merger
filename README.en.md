<a name="readme-top"></a>

[JA](README.md) | [EN](README.en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

# ROS2 Laser Scan Merger

<!-- 目次 -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#introduction">Introduction</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started
</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">installation</a></li>
      </ul>
    </li>
    <li><a href="#launch-and-usage">Launch and Usage</a></li>
    <li><a href="#parameters">Parameters</a></li>
    <li><a href="#milestones">Milestones</a></li>
    <li><a href="#references">References</a></li>
  </ol>
</details>

## Introduction
This repository **merges** multiple **LaserScan/Lidar** topics to generate a new, virtual **LaserScan** topic.

It is also capable of merging point clouds obtained from **RGB-D cameras** with **2D Lidar** topics.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started
This section explains how to set up this repository.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Prerequisites
Before you proceed with the installation, make sure you have the following environment set up.

| System  | Version |
| --- | --- |
| Ubuntu | 22.04 (Jammy Jellyfish) |
| ROS    | Humble Hawksbill |
| Python | 3.10 |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

1. Navigate to the `src` folder in your ROS2 workspace.

    ```sh
    cd ~/colcon_ws/src/
    ```

2. Clone this repository.
    ```sh
    git clone -b humble-devel https://github.com/TeamSOBITS/ros2_laser_scan_merger.git
    ```
3. Navigate into the repository.

    ```sh
    cd ros2_laser_scan_merger/
    ```
4. Install dependent packages.
    ```sh
    bash install.sh
    ```
5. Compile the package.

    ```sh
    cd ~/colcon_ws/
    ```
    ```sh
    colcon build --symlink-install
    ```
    ```sh
    source ~/colcon_ws/install/setup.sh
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Launch and Usage
Before running, please confirm that Sobits [Sobits Navigation Stack](https://github.com/TeamSOBITS/sobits_navigation_stack) is installed.

1. Launch the robot and confirm that 3D point cloud data is being published.

2. When merging a **point cloud** from an **RGB-D camera** and a **2D Lidar scan**, change `robot_name` in the [merge_2_scan.launch.py](launch/merge_2_scan.launch.py) file to the robot's name you are using, and execute the following command.

```sh
ros2 launch ros2_laser_scan_merger merge_2_scan.launch.py 
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Parameters
- The following are the parameters configurable per robot in the `sensor_fusion_config.yaml` file from the [Sobits Navigation Stack](https://github.com/TeamSOBITS/sobits_navigation_stack/tree/humble-devel/sobits_slam/param).

- The parameters for converting the **RGB-D camera's point cloud** into a **LaserScan** type are as follows:

| Parameter Name | Description |
| :--- | :--- |
| **`angle_increment`** | The angular resolution of the output **LaserScan**. |
| **`angle_max`** | The maximum scan angle of the output **LaserScan**. |
| **`angle_min`** | The minimum scan angle of the output **LaserScan**. |
| **`range_max`** | The maximum detection range of the output **LaserScan**. |
| **`range_min`** | The minimum detection range of the output **LaserScan**. |
| **`max_height`** | The maximum height of the point cloud to include in the scan. |
| **`min_height`** | The minimum height of the point cloud to include in the scan. |
| **`target_frame`** | The coordinate system (frame ID) of the output **LaserScan**. |
| **`use_inf`** | Whether to treat distances exceeding `range_max` as **infinity** (`inf`). |
| **`remap_cloud_in_target`** | The name of the input **PointCloud2** topic before conversion. |
| **`remap_scan_out_target`** | The name of the output **LaserScan** topic after conversion. |

***

* The parameters for **merging two LaserScan** type data are as follows:

| Parameter Name | Description |
| :--- | :--- |
| **`pointCloudFrameId`** | The coordinate system (frame ID) of the merged **PointCloud2**. |
| **`scanTopic1`** | The topic name of the first **LaserScan** to be merged. |
| **`scanTopic2`** | The topic name of the second **LaserScan** to be merged. |
| **`show1`** | Whether to include the first scan data in the merge. |
| **`show2`** | Whether to include the second scan data in the merge. |
| **`target_frame`** | The coordinate system (frame ID) of the merged **LaserScan**. |
| **`remap_scan_out_target`** | The topic name of the merged **LaserScan**. |


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Milestones
Please visit the Issue page to check for current bugs or requests for new features.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## References
[ros2_laser_scan_merger](https://github.com/mich1342/ros2_laser_scan_merger)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TeamSOBITS/ros2_laser_scan_merger.svg?style=for-the-badge
[contributors-url]: https://github.com/TeamSOBITS/ros2_laser_scan_merger/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TeamSOBITS/ros2_laser_scan_merger.svg?style=for-the-badge
[forks-url]: https://github.com/TeamSOBITS/ros2_laser_scan_merger/network/members
[stars-shield]: https://img.shields.io/github/stars/TeamSOBITS/ros2_laser_scan_merger.svg?style=for-the-badge
[stars-url]: https://github.com/TeamSOBITS/ros2_laser_scan_merger/stargazers
[issues-shield]: https://img.shields.io/github/issues/TeamSOBITS/ros2_laser_scan_merger.svg?style=for-the-badge
[issues-url]: https://github.com/TeamSOBITS/ros2_laser_scan_merger/issues
[license-shield]: https://img.shields.io/github/license/TeamSOBITS/ros2_laser_scan_merger.svg?style=for-the-badge
[license-url]: LICENSE