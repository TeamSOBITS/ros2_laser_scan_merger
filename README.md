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
    git clone -b feature/humble-devel https://github.com/TeamSOBITS/ros2_laser_scan_merger.git
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
2通りの起動方法があります．

- RGB-Dカメラの点群と2D Lidarを使用する場合，[p_to_l.launch.py](launch/p_to_l.launch.py)を起動
    ```sh
    ros2 launch ros2_laser_scan_merger p_to_l.launch.py 
    ```
- 2つの2D Lidarを使用する場合，[merge_2_scan.launch.py](launch/merge_2_scan.launch.py)を起動
    ```sh
    ros2 launch ros2_laser_scan_merger merge_2_scan.launch.py 
   ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## パラメータ

`config` ディレクトリ内の `params.yaml` ファイルで設定されます．


```yaml
/ros2_laser_scan_merger:
  ros__parameters:
    # --- 色設定 (注: 現在のlaser_geometryを用いた実装では，これらの色設定は反映されません) ---
    laser1B: 0                  # 1つ目のスキャンの点群の色 (青: 0-255)
    laser1G: 255                # 1つ目のスキャンの点群の色 (緑: 0-255)
    laser1R: 0                  # 1つ目のスキャンの点群の色 (赤: 0-255)
    laser2B: 255                # 2つ目のスキャンの点群の色 (青: 0-255)
    laser2G: 0                  # 2つ目のスキャンの点群の色 (緑: 0-255)
    laser2R: 0                  # 2つ目のスキャンの点群の色 (赤: 0-255)
    # --- トピックとフレームID設定 ---
    pointCloudTopic: cloud_in   # マージ処理後に出力するPointCloud2メッセージのトピック名
    pointCloudFrameId: base_range_sensor_link # マージ後のPointCloud2の座標系(フレームID)
    scanTopic1: /hsrb/base_scan # マージ対象とする1つ目のLaserScanトピック名
    scanTopic2: /camera_scan    # マージ対象とする2つ目のLaserScanトピック名
    # --- 表示設定 ---
    show1: true                 # 1つ目のスキャンデータをマージに含めるか (true/false)
    show2: true                 # 2つ目のスキャンデータをマージに含めるか (true/false)
    # --- 時間設定 ---
    use_sim_time: false         # シミュレーション時間(/clockトピック)を使用するか (true/false)
```
```yaml
/static_transform_publisher:
  ros__parameters:
    # --- 静的座標変換 (base_range_sensor_link -> laser) ---
    # このTFは，TFツリーを完成させるために定義されていますが，
    # 現在の設定では直接的な座標変換には使用されていません．
    x: 0.0                      # x軸方向の並進 (メートル)
    y: 0.0                      # y軸方向の並進 (メートル)
    z: 0.0                      # z軸方向の並進 (メートル)
    qx: 0.0                     # クォータニオンによる回転 (x)
    qy: 0.0                     # クォータニオンによる回転 (y)
    qz: 0.0                     # クォータニオンによる回転 (z)
    qw: 1.0                     # クォータニオンによる回転 (w)
    frame_id: "base_range_sensor_link" # 親となる座標系の名前
    child_frame_id: "laser"     # 子となる座標系の名前

```
```yaml
/pointcloud_to_laserscan:
  ros__parameters:
    # --- 出力LaserScanの仕様設定 ---
    angle_increment: 0.0087     # 出力LaserScanの角度分解能 (ラジアン単位)
    angle_max: 3.14             # 出力LaserScanの最大スキャン角度 (ラジアン単位)
    angle_min: -3.14            # 出力LaserScanの最小スキャン角度 (ラジアン単位)
    range_max: 10.0             # 出力LaserScanの最大検知距離 (メートル)
    range_min: 0.35             # 出力LaserScanの最小検知距離 (メートル)
    scan_time: 0.3333           # 1スキャンにかかる時間 (秒)．1/周波数．
    # --- 点群からLaserScanへの変換設定 ---
    max_height: 1.0             # スキャンに含める点群の高さの最大値 (メートル)
    min_height: 0.0             # スキャンに含める点群の高さの最小値 (メートル)
    target_frame: base_footprint # 出力LaserScanの座標系(フレームID)
    transform_tolerance: 0.01   # TFの座標変換を待つ最大時間 (秒)
    use_inf: true               # range_maxを超える距離を無限大(inf)として扱うか (true/false)
    inf_epsilon: 1.0            # use_infがfalseの時，無限遠を表すためにrange_maxに加算する値
    # --- ROS 2通信設定 ---
    queue_size: 16              # メッセージキューのサイズ
    use_sim_time: false         # シミュレーション時間(/clockトピック)を使用するか (true/false)
    # --- トピック名設定 (注: ローンチファイルのremappingsで上書きされることが多い) ---
    pointcloud_topic: cloud_in  # 入力として購読するPointCloud2トピック名
    scan_topic: /scan           # 変換後に出力するLaserScanトピック名
```

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