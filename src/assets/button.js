import React from 'react';
import {StyleSheet, View, TouchableOpacity} from 'react-native';
import Ionicons from 'react-native-vector-icons/Ionicons';
import {CameraOptions, launchCamera} from 'react-native-image-picker';

const Button = () => {
    const openCamera = async () => {
        const option = {
            mediaType: 'photo',
            quality: 1,
        };
        await requestCameraPermission();
        launchCamera(option, res => {
            if (res.didCancel) {
                console.log('User Cancelled image picker');
            } else if (res.errorCode) {
                console.log(res.errorMessage);
            } else {
                // bla bla
            }
        });
    };

    // for Android
    const requestCameraPermission = async () => {
        try {
            const granted = await PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.CAMERA, {
                title: 'App Camera Permission',
                message: 'App needs access to your camera ',
                buttonNeutral: 'Ask Me Later',
                buttonNegative: 'Cancel',
                buttonPositive: 'OK',
            });
            if (granted === PermissionsAndroid.RESULTS.GRANTED) {
                console.log('Camera permission given');
            } else {
                console.log('Camera permission denied');
            }
        } catch (err) {
            console.warn(err);
        }
    };

    return (
        <TouchableOpacity
            style={{
                justifyContent: 'center',
                alignItems: 'center',
                marginTop: 60,
                backgroundColor: 'pink',
                width: 50,
                height: 50,
                borderRadius: 50,
            }}
            onPress={openCamera}>
            <Ionicons name="camera" size={25} color="white" />
        </TouchableOpacity>
    );
};

export default Button;