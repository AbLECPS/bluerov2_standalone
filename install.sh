#!/bin/bash

clear
echo '#########################################'
echo '# This will install BlueROV2 standalone #'
echo '#                                       #'
echo '#       ~/.bashrc will be updated       #'
echo '#                                       #'
echo '#       Press any key to continue       #'
echo '#########################################'
read -rsn1

echo 'Setting environment variables:'
echo ''
echo "export ALC_HOME=$PWD" >> ~/.bashrc
echo "export ALC_WORKING_DIR=$PWD/../alc_workspace" >> ~/.bashrc
source ~/.bashrc

FOLDER=$ALC_WORKING_DIR
if [ -d "$FOLDER" ]; then
    echo "$FOLDER exists."
else 
    mkdir $FOLDER
fi


echo 'Pulling ablecps/alc, ablecps/alc_data, roskinetic-core image from dockerhub'
echo ''
docker pull ablecps/alc:latest
docker tag ablecps/alc:latest alc:latest
docker pull ablecps/alc_data:latest
docker tag ablecps/alc_data:latest alc_data:latest
docker pull ros:kinetic-ros-core
docker run --rm  -e ALC_WORKING_DIR=$ALC_WORKING_DIR -v $ALC_WORKING_DIR:$ALC_WORKING_DIR alc_data:latest bash -c "source file.sh"
docker rmi alc_data:latest

echo 'Creating docker network'
docker network inspect ros > /dev/null 2>&1
if [ $? -eq 0 ]; then 
    echo 'Skipped, docker network already exists'
else
    docker network create \
        --gateway 172.18.0.1 \
        --subnet 172.18.0.0/16 \
        ros
    echo 'docker network created'
fi

echo 'Building sources:'
echo ''
pushd bluerov2_standalone/catkin_ws/
source build_sources.sh
popd



echo '#########################################'
echo '#     Please update /etc/hosts file with:
echo '#########################################'
echo ''
echo '172.18.0.2 ros-master'
echo '172.18.0.4 aa_uuvsim'
echo ''
echo '#########################################'
echo '#                Finished               #'
echo '#########################################'
