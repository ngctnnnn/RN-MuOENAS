#!/bin/sh
curl https://download.docker.com/linux/static/stable/x86_64/docker-20.10.3.tgz | tar xz
sudo cp ./docker/docker /usr/bin/ && rm -rf docker && docker version
docker pull reactnativecommunity/react-native-android
docker run reactnativecommunity/react-native-android
npm install -g yarn
yarn 
yarn run android