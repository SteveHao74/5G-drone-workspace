#include <stdio.h>
#include <stdlib.h>
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>

double lx=0,ly=0,lz=0,az=0;//初始化

void velCallback(const geometry_msgs::Twist::ConstPtr& msg)//订阅/vel_order回调赋值，接收rec_vel_order的速度指令
{
    lx=msg->linear.x;
    ly=msg->linear.y;
    lz=msg->linear.z;
    az=msg->angular.z;
}

int main(int argc, char** argv)
{
    ros::init(argc,argv,"rec_vel_exe_node");

    ros::NodeHandle nh;
    ros::Subscriber vel_sub = nh.subscribe<geometry_msgs::Twist>("/vel_order",10,velCallback);//订阅/vel_order
    ros::Publisher pub_ = nh.advertise<geometry_msgs::Twist>("/mavros/setpoint_velocity/cmd_vel_unstamped", 1);//定义发布者，发布速度指令

    ros::Rate loop_rate(20);//循环频率20Hz

    geometry_msgs::Twist vel_;
    /*以20Hz频率执行速度指令*/
    while(ros::ok()){
        vel_.linear.x = lx;
        vel_.linear.y = ly;
        vel_.linear.z = lz;
        vel_.angular.z = az;

        pub_.publish(vel_);//发布话题

        ros::spinOnce();
        loop_rate.sleep();
    }

    return(0);
}
