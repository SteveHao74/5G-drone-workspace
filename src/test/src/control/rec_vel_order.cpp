#include <stdio.h>
#include <stdlib.h>
#include <ros/ros.h>
#include <std_msgs/Bool.h>
#include <mavros_msgs/SetMode.h>
#include <mavros_msgs/State.h>
#include <geometry_msgs/Twist.h>

double tar_lx=0,tar_ly=0,tar_lz=0,tar_az=0;//初始化

bool start=false;

/*无人机当前飞行模式状态*/
mavros_msgs::State current_state;
void state_cb(const mavros_msgs::State::ConstPtr& msg){
    current_state = *msg;
}

/*订阅键盘信号*/
void keyCallback(const std_msgs::Bool::ConstPtr& msg)
{
    start=msg->data;
}

int main(int argc, char** argv)
{
    ros::init(argc,argv,"rec_vel_order_node");

    ros::NodeHandle nh;
    ros::Subscriber key_sub = nh.subscribe<std_msgs::Bool>("/key_press",10,keyCallback);

    ros::Publisher pub_ = nh.advertise<geometry_msgs::Twist>("/vel_order", 1);
    
    ros::Subscriber state_sub = nh.subscribe<mavros_msgs::State>
            ("/mavros/state", 10, state_cb);

    ros::ServiceClient set_mode_client = nh.serviceClient<mavros_msgs::SetMode>
            ("/mavros/set_mode");

    ros::Rate loop_rate(20);

    geometry_msgs::Twist tar_vel;

    /*将SetMode的请求设置为自动降落模式*/
    mavros_msgs::SetMode land_set_mode;
    land_set_mode.request.custom_mode = "AUTO.LAND";

    tar_vel.linear.x = tar_lx;
    tar_vel.linear.y = tar_ly;
    tar_vel.linear.z = tar_lz;
    tar_vel.angular.z = tar_az;

    pub_.publish(tar_vel);//发布零值速度指令
    
    while(start == false){ros::spinOnce();}//等待键盘启动信号
    if(start == true){//当接收到键盘启动信号时开始执行
        tar_lx = 0;
        tar_ly = 0;
        tar_lz = 2;//起飞速度2m/s
        tar_vel.linear.x = tar_lx;
        tar_vel.linear.y = tar_ly;
        tar_vel.linear.z = tar_lz;
        pub_.publish(tar_vel);//发布速度指令
	ROS_INFO("taking off");
        ros::Time flight_time = ros::Time::now();
        while(ros::Time::now() - flight_time <= ros::Duration(2.0)){ros::spinOnce();}//以当前设定速度飞行2s

        /*在上述指令执行完毕后，发布零值速度指令持续1s，给飞机在当前方向上降速留点时间*/
        tar_lx = 0;
        tar_ly = 0;
        tar_lz = 0;
        tar_vel.linear.x = tar_lx;
        tar_vel.linear.y = tar_ly;
        tar_vel.linear.z = tar_lz;
        pub_.publish(tar_vel);
        flight_time = ros::Time::now();
        while(ros::Time::now() - flight_time <= ros::Duration(1.0)){ros::spinOnce();}

        tar_lx = 0;
        tar_ly = 1;//向北以1m/s速度飞行2s
        tar_lz = 0;
        tar_vel.linear.x = tar_lx;
        tar_vel.linear.y = tar_ly;
        tar_vel.linear.z = tar_lz;
        pub_.publish(tar_vel);
	ROS_INFO("flying to north");
        flight_time = ros::Time::now();
        while(ros::Time::now() - flight_time <= ros::Duration(2.0)){ros::spinOnce();}

        tar_lx = 0;
        tar_ly = 0;
        tar_lz = 0;
        tar_vel.linear.x = tar_lx;
        tar_vel.linear.y = tar_ly;
        tar_vel.linear.z = tar_lz;
        pub_.publish(tar_vel);
        flight_time = ros::Time::now();
        while(ros::Time::now() - flight_time <= ros::Duration(1.0)){ros::spinOnce();}

        tar_lx = -1;//向西以1m/s速度飞行2s
        tar_ly = 0;
        tar_lz = 0;
        tar_vel.linear.x = tar_lx;
        tar_vel.linear.y = tar_ly;
        tar_vel.linear.z = tar_lz;
        pub_.publish(tar_vel);
	ROS_INFO("flying to west");
        flight_time = ros::Time::now();
        while(ros::Time::now() - flight_time <= ros::Duration(2.0)){ros::spinOnce();}

        tar_lx = 0;
        tar_ly = 0;
        tar_lz = 0;
        tar_vel.linear.x = tar_lx;
        tar_vel.linear.y = tar_ly;
        tar_vel.linear.z = tar_lz;
        pub_.publish(tar_vel);
        flight_time = ros::Time::now();
        while(ros::Time::now() - flight_time <= ros::Duration(1.0)){ros::spinOnce();}

        tar_lx = 0;
        tar_ly = -1;//向南以1m/s速度飞行2s
        tar_lz = 0;
        tar_vel.linear.x = tar_lx;
        tar_vel.linear.y = tar_ly;
        tar_vel.linear.z = tar_lz;
        pub_.publish(tar_vel);
	ROS_INFO("flying to south");
        flight_time = ros::Time::now();
        while(ros::Time::now() - flight_time <= ros::Duration(2.0)){ros::spinOnce();}

        tar_lx = 0;
        tar_ly = 0;
        tar_lz = 0;
        tar_vel.linear.x = tar_lx;
        tar_vel.linear.y = tar_ly;
        tar_vel.linear.z = tar_lz;
        pub_.publish(tar_vel);
        flight_time = ros::Time::now();
        while(ros::Time::now() - flight_time <= ros::Duration(1.0)){ros::spinOnce();}

        tar_lx = 1;//向东以1m/s速度飞行2s
        tar_ly = 0;
        tar_lz = 0;
        tar_vel.linear.x = tar_lx;
        tar_vel.linear.y = tar_ly;
        tar_vel.linear.z = tar_lz;
        pub_.publish(tar_vel);
	ROS_INFO("flying to east");
        flight_time = ros::Time::now();
        while(ros::Time::now() - flight_time <= ros::Duration(2.0)){ros::spinOnce();}

        tar_lx = 0;
        tar_ly = 0;
        tar_lz = 0;
        tar_vel.linear.x = tar_lx;
        tar_vel.linear.y = tar_ly;
        tar_vel.linear.z = tar_lz;
        pub_.publish(tar_vel);
        flight_time = ros::Time::now();
        while(ros::Time::now() - flight_time <= ros::Duration(1.0)){ros::spinOnce();}

        /*以上正方形任务执行完毕后将飞机飞行状态转为自动降落模式*/
        if( current_state.mode != "AUTO.LAND"){
            if( set_mode_client.call(land_set_mode) &&
                land_set_mode.response.mode_sent){
                ROS_INFO("Drone Landing");
            }
        }
    }

    return(0);
}
