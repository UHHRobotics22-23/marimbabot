/*
 * The main node for the serial based mallet hardware interface.
 */
#include <ros/ros.h>
#include <controller_manager/controller_manager.h>
#include "marimbabot_hardware/servo_interface_serial.hpp"

int main(int argc, char **argv) {
    ros::init(argc, argv, "mallet_hardware_control_node");

    // Get device parameters from parameter server
    ros::NodeHandle node_handle { "~" };
    int baud;
    std::string device;
    int top_limit;
    int bottom_limit;
    node_handle.param("device", device, std::string("/dev/ttyUSB0"));
    node_handle.param("baud", baud, 115200);

    ROS_INFO("Starting hardware control node for device %s", device.c_str());

    // Initialize the servo interface and controller manager
    ServoInterface servo_interface(node_handle, device, baud);
    controller_manager::ControllerManager controller_manager(&servo_interface);

    ros::AsyncSpinner spinner(1);
    spinner.start();
    ros::Rate loop_rate(100);

    // Initialize the servo interface
    servo_interface.initialize();

    // Controller loop
    // This is the main functionality of the node.
    // It reads the state of the servo motor, updates the controller manager, and writes the command to the servo motor.
    while(ros::ok()) {
        servo_interface.read();
        controller_manager.update(servo_interface.get_time(), servo_interface.get_period());
        servo_interface.write();
    
        loop_rate.sleep();
    }
}