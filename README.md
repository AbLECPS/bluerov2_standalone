# BlueROV2 Standalone Insaller

This script will install BlueROV2 standalone code only with LECs and BehaviorTree. Disable these nodes to create customized controllers pipe-tracking, obstacle-avoidance and autonomy.

# Prerequisites
## Setup/configure:

- Linux OS (tested with Ubuntu 22.04, WSL2 with Ubunutu 22.04)

- NVidia GPU and Driver

- Nvidia Driver version >= 565.75 is recommended for compatability with CUDA 12.7

- Docker

    Tested with docker version 25.0.2

    Configure your user account to use docker without ‘sudo’

    Be sure to log out, then log back in so group changes will be applied

- Nvidia Container Runtime version >=1.15

    
## Other tools required as part of the setup.

- Install Git

    sudo apt-get update
    sudo apt-get install git



# Installing BlueROV2 Planner

-   run the following command to build and install bluervo2
```
source install.sh
```

The install
         
    creates folders alc_workspace and sets up the envrionment variables alc_home, alc_working_dir.
        
    pulls dockers alc:latest, alc_data:latest and  roskinetic-core.
        
    copies data into alc_workspace from the alc_data docker


# Update /etc/hosts file

Once install is completed, please follow the instuctions printed to update the /etc/hosts file.
Alternately, please update  /etc/hosts file with the following lines

```
172.18.0.2 ros-master
172.18.0.4 aa_uuvsim
```

# Run

The instructions in this section describe how to run the BlueROV simulation natively on the host machine.
The docker launch scripts below map the display from the host to docker.

Open three terminals:

**1.: Start roscore docker**
```
cd $ALC_HOME/bluerov2_standalone/catkin_ws
source run_roscore.sh
```

**2.: Start bluerovsim docker**
```
cd $ALC_HOME/bluerov2_standalone/catkin_ws
source run_bluerov_sim.sh
```
In the docker 
```
source run_xvfb.sh
source src/vandy_bluerov/scripts/bluerov_launch.sh
```

**Preset scenarios**

If you want to run a preset scenario, run eg.: 
```
source $ALC_HOME/bluerov2_standalone/catkin_ws/src/vandy_bluerov/scripts/cp2_00_single_thr_deg.sh 
```
Check scenarios.md for more detail about available scenarios from command line and toolchain.

**3.: Optional for visual representation: start rviz**
```
docker exec -it bluerov_sim bash
```
In the docker

```
source run_xvfb.sh
source src/vandy_bluerov/rviz/bluerov2_control.rviz
```

