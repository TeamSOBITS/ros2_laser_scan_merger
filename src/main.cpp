//
//   created by: Michael Jonathan (mich1342)
//   github.com/mich1342
//   24/2/2022
//   日本語コメント追加 by Gemini Code Assist
//

// C++ standard libraries
#include <cmath>
#include <string>
#include <vector>
#include <array>
#include <algorithm>

// ROS2 libraries
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"
#include "tf2_sensor_msgs/tf2_sensor_msgs.hpp"
#include "rcl_interfaces/msg/parameter_descriptor.hpp"
#include "laser_geometry/laser_geometry.hpp"
#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/approximate_time.h>

// PCL libraries
#include <pcl_conversions/pcl_conversions.h>
#include <sensor_msgs/point_cloud2_iterator.hpp>

// 2つのLaserScanメッセージを時間で同期させるためのポリシー定義
typedef message_filters::sync_policies::ApproximateTime<sensor_msgs::msg::LaserScan, sensor_msgs::msg::LaserScan> MySyncPolicy;

/**
 * @class scanMerger
 * @brief 複数のLaserScanメッセージを購読し、それらを一つのPointCloud2メッセージにマージするROS 2ノード。
 * 
 * このクラスは、message_filtersを使用して複数のLaserScanトピックを同期し、
 * laser_geometryとtf2を使用して各スキャンを共通の座標系に変換後、
 * 一つのPointCloud2としてパブリッシュします。
 */
class scanMerger : public rclcpp::Node
{
public:
  // message_filtersの同期ポリシーで使用するキューのサイズ
  static constexpr int SYNC_POLICY_QUEUE_SIZE = 10;

  // コンストラクタ
  scanMerger() : Node("ros2_laser_scan_merger"), tf_buffer_(this->get_clock()), tf_listener_(tf_buffer_)
  {
    RCLCPP_INFO(this->get_logger(), "TFを使用して座標変換を行います。");

    // パラメータの初期化と読み込み
    initialize_params();
    load_params(); // 初期値を読み込む

    // パラメータが外部から変更されたときに呼び出されるコールバック関数を登録
    param_callback_handle_ = this->add_on_set_parameters_callback(std::bind(&scanMerger::parameters_callback, this, std::placeholders::_1));

    // 2つのLaserScanトピックを購読するためのSubscriberを作成
    auto default_qos = rclcpp::QoS(rclcpp::SensorDataQoS());
    sub1_ = std::make_shared<message_filters::Subscriber<sensor_msgs::msg::LaserScan>>(this, topic1_, default_qos.get_rmw_qos_profile());
    sub2_ = std::make_shared<message_filters::Subscriber<sensor_msgs::msg::LaserScan>>(this, topic2_, default_qos.get_rmw_qos_profile());

    // 2つのトピックをタイムスタンプで同期させるためのSynchronizerを作成し、コールバック関数を登録
    sync_ = std::make_shared<message_filters::Synchronizer<MySyncPolicy>>(MySyncPolicy(SYNC_POLICY_QUEUE_SIZE), *sub1_, *sub2_);
    sync_->registerCallback(&scanMerger::scan_callback, this);

    point_cloud_pub_ = this->create_publisher<sensor_msgs::msg::PointCloud2>(cloudTopic_, rclcpp::SensorDataQoS());
  }

private:
  // 同期された2つのLaserScanメッセージを受信したときに呼び出されるコールバック関数
  void scan_callback(const sensor_msgs::msg::LaserScan::SharedPtr& laser1_msg, const sensor_msgs::msg::LaserScan::SharedPtr& laser2_msg)
  {
    update_point_cloud_tf(laser1_msg, laser2_msg);
  }

  // 受信したLaserScanメッセージを元に、座標変換を行いながらポイントクラウドを更新する
  void update_point_cloud_tf(const sensor_msgs::msg::LaserScan::SharedPtr& laser1, const sensor_msgs::msg::LaserScan::SharedPtr& laser2)
  {
    // 構造化された型に変換せずにマージするため、PCLPointCloud2の方が効率的
    pcl::PCLPointCloud2 cloud_merged;

    if (show1_ && laser1)
    {
      process_scan_with_tf(laser1, cloud_merged);
    }

    if (show2_ && laser2)
    {
      process_scan_with_tf(laser2, cloud_merged);
    }

    // マージされたポイントクラウドに点が存在する場合にパブリッシュする
    if (cloud_merged.width * cloud_merged.height > 0)
    {
      auto pc2_msg_ = std::make_shared<sensor_msgs::msg::PointCloud2>();
      pcl_conversions::fromPCL(cloud_merged, *pc2_msg_);
      pc2_msg_->header.frame_id = cloudFrameId_;
      
      // 2つのスキャンのうち、より新しい方のタイムスタンプを使用する
      pc2_msg_->header.stamp = (rclcpp::Time(laser1->header.stamp) > rclcpp::Time(laser2->header.stamp)) ? laser1->header.stamp : laser2->header.stamp;

      pc2_msg_->is_dense = false;
      point_cloud_pub_->publish(*pc2_msg_);
    }
  }

  /**
   * @brief 個々のLaserScanメッセージを座標変換し、ポイントクラウドに結合する
   * @param scan_in 入力となるLaserScanメッセージの共有ポインタ
   * @param cloud_out 結合先となるPCLPointCloud2の参照
   */
  void process_scan_with_tf(const sensor_msgs::msg::LaserScan::SharedPtr& scan_in, pcl::PCLPointCloud2& cloud_out)
  {
      if (!scan_in) return;
      
      sensor_msgs::msg::PointCloud2 cloud_transformed;

      // TF変換で例外が発生する可能性があるため、try-catchブロックで囲む
      try
      {
          // laser_geometryを使用して、LaserScanをターゲットフレームのPointCloud2に投影する
          // 2つのポイントクラウドが同じフィールドを持つようにするため（結合のため）、
          // 'intensity'チャンネルを無効にし、'index'チャンネルのみを明示的に要求する。
          // これにより、一方のスキャンに強度情報があり、もう一方にない場合のエラーを防ぐ。
          int channel_options = laser_geometry::channel_option::Index;
          projector_.transformLaserScanToPointCloud(cloudFrameId_, *scan_in, cloud_transformed, tf_buffer_, -1.0, channel_options);

          // PCLに変換してマージする。PCLPointCloud2を使用することで、コストの高いpcl::PointCloudへの変換を回避できる。
          pcl::PCLPointCloud2 cloud_to_merge;
          pcl_conversions::toPCL(cloud_transformed, cloud_to_merge);
          
          // 既存のクラウドに新しいクラウドを結合する
          pcl::concatenate(cloud_out, cloud_to_merge, cloud_out);
      }
      catch (tf2::TransformException &ex)
      {
          RCLCPP_WARN(this->get_logger(), "%s から %s への座標変換ができませんでした: %s", scan_in->header.frame_id.c_str(), cloudFrameId_.c_str(), ex.what());
          return;
      }
  }

  // ノード起動時にパラメータを宣言する
  void initialize_params()
  {
    this->declare_parameter("pointCloudTopic", "base/custom_cloud");
    this->declare_parameter("pointCloudFrameId", "laser");

    this->declare_parameter("scanTopic1", "scan1");
    this->declare_parameter("show1", true);

    this->declare_parameter("scanTopic2", "scan2");
    this->declare_parameter("show2", true);
  }

  // パラメータが変更されたときに呼び出されるコールバック関数
  rcl_interfaces::msg::SetParametersResult parameters_callback(const std::vector<rclcpp::Parameter> & /*parameters*/)
  {
      rcl_interfaces::msg::SetParametersResult result;
      result.successful = true;
      result.reason = "success";
      load_params();
      return result;
  }

  // パラメータサーバーから値を取得し、メンバ変数に格納する
  void load_params()
  {
    cloudTopic_ = this->get_parameter("pointCloudTopic").as_string();
    cloudFrameId_ = this->get_parameter("pointCloudFrameId").as_string();
    topic1_ = this->get_parameter("scanTopic1").as_string();
    show1_ = this->get_parameter("show1").as_bool();

    topic2_ = this->get_parameter("scanTopic2").as_string();
    show2_ = this->get_parameter("show2").as_bool();
  }

  // --- メンバ変数 ---
  // パラメータから読み込む変数
  std::string topic1_, topic2_, cloudTopic_, cloudFrameId_;
  bool show1_, show2_;
  // laser_geometryはスキャンごとの色付けをサポートしていないため、色に関するパラメータは不要になった
  // uint8_t laser1R_, laser1G_, laser1B_;
  // uint8_t laser2R_, laser2G_, laser2B_;
  
  // 事前計算した三角関数のテーブル（LUT）も不要になった
  // std::vector<float> lut_cos1_, lut_sin1_;
  // std::vector<float> lut_cos2_, lut_sin2_;

  // TF2関連
  tf2_ros::Buffer tf_buffer_;
  tf2_ros::TransformListener tf_listener_;

  // message_filters関連
  std::shared_ptr<message_filters::Subscriber<sensor_msgs::msg::LaserScan>> sub1_;
  std::shared_ptr<message_filters::Subscriber<sensor_msgs::msg::LaserScan>> sub2_;
  std::shared_ptr<message_filters::Synchronizer<MySyncPolicy>> sync_;

  // ROS 2インターフェース
  OnSetParametersCallbackHandle::SharedPtr param_callback_handle_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr point_cloud_pub_;
  // LaserScanからPointCloud2への変換を行うためのユーティリティ
  laser_geometry::LaserProjection projector_;

};

// main関数: ノードを初期化し、実行（スピン）する
int main(int argc, char* argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<scanMerger>());
  rclcpp::shutdown();
  return 0;
}
