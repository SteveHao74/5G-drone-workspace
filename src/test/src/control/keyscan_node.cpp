#include <termios.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/poll.h>
#include <boost/thread/thread.hpp>
#include <ros/ros.h>
#include <std_msgs/Bool.h>

#define KEYCODE_SPACE 0x20
	
bool flag=false;

class KeyboardTeleopNode
{
    private:
        ros::NodeHandle n_;

    public:
        ros::Publisher pub_;
        std_msgs::Bool key;
        KeyboardTeleopNode()
        {
            pub_ = n_.advertise<std_msgs::Bool>("/key_press", 1);
            ros::NodeHandle n_private("~");
        }

        ~KeyboardTeleopNode() { }
        void keyboardLoop();
};

KeyboardTeleopNode* tbk;
int kfd = 0;
struct termios cooked, raw;
bool done;

int main(int argc, char** argv)
{
    ros::init(argc,argv,"keyscan_node");
    KeyboardTeleopNode tbk;

    ros::NodeHandle nh;
    boost::thread t = boost::thread(boost::bind(&KeyboardTeleopNode::keyboardLoop, &tbk));

    ros::Rate loop_rate(20);

    while(ros::ok()){
        tbk.key.data = flag;
        tbk.pub_.publish(tbk.key);

        ros::spinOnce();

        loop_rate.sleep();
    }

    t.interrupt();
    t.join();

    tcsetattr(kfd, TCSANOW, &cooked);

    return(0);
}

void KeyboardTeleopNode::keyboardLoop()
{
    char c;

    tcgetattr(kfd, &cooked);
    memcpy(&raw, &cooked, sizeof(struct termios));
    raw.c_lflag &=~ (ICANON | ECHO);
    raw.c_cc[VEOL] = 1;
    raw.c_cc[VEOF] = 2;
    tcsetattr(kfd, TCSANOW, &raw);

    struct pollfd ufd;
    ufd.fd = kfd;
    ufd.events = POLLIN;
    int times=0;
    int num;

    for(;;)
    {
        boost::this_thread::interruption_point();

        if ((num = poll(&ufd, 1, 250)) < 0)
        {
            perror("poll():");
            return;
        }
        else if(num > 0)
        {
            if(read(kfd, &c, 1) < 0)
            {
                perror("read():");
                return;
            }
        }

        switch(c)
        {
            case KEYCODE_SPACE:
		        flag = true;
                break;
        }

        num = 0;
    }
}
