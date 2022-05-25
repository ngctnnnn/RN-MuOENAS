import React from 'react'
import { View, Text, StyleSheet, Image, Button } from 'react-native';
import { launchImageLibrary, launchCamera } from 'react-native-image-picker';

export default class App extends React.Component {
    state = {
        PHOTO: null,
    }

    handleChoosePhoto = () => {
        const LibraryOptions = {
            noData: true,
            includeBase64: false
        };
        launchImageLibrary(LibraryOptions, response => {
            console.log("response", response.assets[0].uri);
            this.setState({ PHOTO: response });
        });
    };

    handleTakePhoto = () => {
        const CameraOptions = {
            noData: true,
            cameraType: 'back',
            includeBase64: false
        };
        launchCamera(CameraOptions, response => {
            console.log("response", response.assets[0].uri);
            this.setState({ PHOTO: response });
        });
    };

    render() {
        const { PHOTO } = this.state;
        return(
            <View style={styles.MainContainer}>
                <View style={styles.hello}>
                    <Text style={styles.hello}>Code base for CS523 project</Text>
                </View>

                <View style={styles.PhotoContent}>
                    {PHOTO && (
                        <Image
                            source={{ uri: PHOTO.assets[0].uri }}
                            style={styles.Photo}
                        />
                    )}
                </View> 

                <View style={styles.ButtonContent}>
                    <Button title="Take a photo" onPress={this.handleTakePhoto}/>
                    <Button title="Upload a photo"  onPress={this.handleChoosePhoto}/>
                </View>
            </View>
        );
    }
}
 
const styles = StyleSheet.create({
    MainContainer: {
        // flex: 1,
        // alignItems: 'center',
        // justifyContent: "center",
        // marginTop: 40
    },
    hello: {
        // flex: 1,
        fontSize: 24,
        textAlign: 'center',
        alignSelf: 'center',
    },
    PhotoContent: {
        // flex: 4
    }, 
    Photo: {
        width: 300,
        height: 300
    },
    ButtonContent: {
        // flex: 2,
        // justifyContent: 'space-evenly',
        // flexDirection: 'row',
        // alignSelf: 'center',
        // position: 'absolute',
        // bottom: 100
    },
});