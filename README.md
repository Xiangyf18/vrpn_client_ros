# vrpn_client_ros  

ROS2 client nodes for the [VRPN](https://github.com/vrpn/vrpn/wiki) library, compatible with VICON, OptiTrack, and other [hardware interfaces](https://github.com/vrpn/vrpn/wiki/Supported-hardware-devices).

Codes have been tested  with RO2  Galactic distribution  on Ubuntu 20.04 and OptiTrack setup with Motive.



## Quick Start

Simple  installation tutorial  for VRPN library.

```shell
git clone https://github.com/vrpn/vrpn.git
cd vrpn
mkdir build
cd build
cmake ..
make
make install
```

Simple  installation tutorial  for this repository.

```shell
mkdir -p  dev_ws/src
cd dev_ws/src
git clone https://github.com/Xiangyf18/vrpn_client_ros.git
cd ..
# needed if you have both ros and ros2
unset  CMAKE_PREFIX_PATH
source /opt/ros/galactic/setup.bash

colcon build
```

Source the setup file  by  `source  install/setup.bash` .

And run the line `ros2 launch vrpn_client_ros vrpn_location_pose.launch` to get rostopic you need.