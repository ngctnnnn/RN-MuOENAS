import React from 'react'
import { View, Text, StyleSheet, Image, Button } from 'react-native';
import { launchImageLibrary } from 'react-native-image-picker';

export default class App extends React.Component {
    state = {
        PHOTO: null,
    }

    handleChoosePhoto = () => {
        const options = {
            noData: true,
            includeBase64: false
        };
        launchImageLibrary(options, response => {
            console.log("response", response.assets[0].uri);
            this.setState({ PHOTO: response });
        });
    };

    render() {
        const { PHOTO } = this.state;
        return(
            <View style={{flex: 1}}>
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
                    <Button title="Take a photo" onPress={this.handleChoosePhoto}/>
                    <Button title="Upload a photo" style={{ marginTop: 100 }} onPress={this.handleChoosePhoto}/>
                </View>
            </View>
        );
    }
}
 
const styles = StyleSheet.create({
    hello: {
        flex: 1,
        fontSize: 24,
        textAlign: 'center',
        marginTop: 20,
    },
    PhotoContent: {
        flex: 1,
        alignItems: 'center',
        justifyContent: "center",
    }, 
    Photo: {
        width: 300,
        height: 300
    },
    ButtonContent: {
        flex: 1,
        justifyContent: 'center',
        alignContent: 'center'
    }

});