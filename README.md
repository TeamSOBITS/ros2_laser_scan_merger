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
  <summary>目次</summary>
  <ol>
    <li>
      <a href="#概要">概要</a>
    </li>
    <li>
      <a href="#セットアップ">セットアップ</a>
      <ul>
        <li><a href="#環境条件">環境条件</a></li>
        <li><a href="#インストール方法">インストール方法</a></li>
      </ul>
    </li>
    <li><a href="#実行操作方法">実行・操作方法</a></li>
    <li><a href="#パラメータ">パラメータ</a></li>
    <li><a href="#マイルストーン">マイルストーン</a></li>
    <li><a href="#参考文献">参考文献</a></li>
  </ol>
</details>

## 概要
本リポジトリは複数の **LaserScan/Lidar** トピックをマージし，新しい仮想的な **LaserScan** トピックを生成します．
RGB-Dカメラから得られる点群と2D Lidarのトピックをマージすることもできます．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## セットアップ
ここで，本レポジトリのセットアップ方法について説明します．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### 環境条件
まず，以下の環境を整えてから，次のインストール方法に進んでください．
| System  | Version |
| --- | --- |
| Ubuntu | 22.04 (Jammy Jellyfish) |
| ROS    | Humble Hawksbill |
| Python | 3.10 |

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### インストール方法

1. ROS2の`src`フォルダに移動します．
    ```sh
    cd ~/colcon_ws/src/
    ```

2. 本レポジトリをcloneします．
    ```sh
    git clone -b humble-devel https://github.com/TeamSOBITS/ros2_laser_scan_merger.git
    ```
3. レポジトリの中へ移動します．
    ```sh
    cd ros2_laser_scan_merger/
    ```
4. 依存パッケージをインストールします．時間がかかるので注意．
    ```sh
    bash install.sh
    ```
5. パッケージをコンパイルします．
    ```sh
    cd ~/colcon_ws/
    ```
    ```sh
    colcon build --symlink-install
    ```
    ```sh
    source ~/colcon_ws/install/setup.sh
    ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## 実行・操作方法

実行する前に,[Sobits Navigation Stack](https://github.com/TeamSOBITS/sobits_navigation_stack)がインストールされているか確認してください.

1. ロボットを起動し,3次元点群が発行されているか確認する.

2. RGB-Dカメラの点群と2D Lidarのスキャンをマージする場合、[merge_2_scan.launch.py ](launch/merge_2_scan.launch.py)で`robot_name`を使用するロボット名に変更し，以下のコマンドを実行します。

```sh
ros2 launch ros2_laser_scan_merger merge_2_scan.launch.py 
```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## パラメータ

以下は[Sobits Navigation Stack](https://github.com/TeamSOBITS/sobits_navigation_stack/tree/humble-devel/sobits_slam/param)の `sensor_fusion_config.yaml` でロボットごとに設定可能なパラメータです．

- RGB-Dカメラの点群をLaserScan型に変換するパラメータは以下の通りです．

| パラメータ名 | 説明 |
| --- | --- |
| angle_increment | 出力LaserScanの角度分解能 |
| angle_max | 出力LaserScanの最大スキャン角度 |
| angle_min | 出力LaserScanの最小スキャン角度 |
| range_max | 出力LaserScanの最大検知距離 |
| range_min | 出力LaserScanの最小検知距離 |
| max_height | スキャンに含める点群の高さの最大値 |
| min_height | スキャンに含める点群の高さの最小値 |
| target_frame | 出力LaserScanの座標系(フレームID) |
| use_inf | range_maxを超える距離を無限大(inf)として扱うか |
| remap_cloud_in_target | 変換前に入力するPointCloud2トピック名 |
| remap_scan_out_target | 変換後に出力するLaserScanトピック名 |

- 2つのLaserScan型のデータをマージするパラメータは以下の通りです．

| パラメータ名 | 説明 |
| --- | --- |
| pointCloudFrameId | マージ後のPointCloud2の座標系(フレームID) |
| scanTopic1 | マージ対象とする1つ目のLaserScanトピック名 |
| scanTopic2 | マージ対象とする2つ目のLaserScanトピック名 |
| show1 | 1つ目のスキャンデータをマージに含めるか |
| show2 | 2つ目のスキャンデータをマージに含めるか |
| target_frame |  マージ後のLaserScanの座標系(フレームID) |
| remap_scan_out_target | マージ後のLaserScanトピック名 |


<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## マイルストーン

現時点のバッグや新規機能の依頼を確認するためにIssueページ をご覧ください．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


## 参考文献
[ros2_laser_scan_merger](https://github.com/mich1342/ros2_laser_scan_merger)

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

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