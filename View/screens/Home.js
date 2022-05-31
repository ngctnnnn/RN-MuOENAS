import { StyleSheet, Text, View, SafeAreaView, Button, Image } from 'react-native'
import React, {useState, setState} from 'react'
import { launchCamera, launchImageLibrary } from 'react-native-image-picker'
import * as FS from 'expo-file-system'
import AppButton from '../components/AppButton'


const Home = () => {
    const [PHOTO_uri, setPHOTO_uri] = useState(null)
    const [pred, setPred] = useState(null)
    const [prob, setProb] = useState(null)
    const toServer = async (mediaFile) => {
        let type = mediaFile.type;
        let schema = "http://";
        let host = "localhost";
        let route = "/image";
        let port = "5000";
        let url = "";
        let content_type = "image/jpg";

        url = schema + host + ":" + port + route;

        let response = await FS.uploadAsync(url, mediaFile.uri, {
        headers: {
            "content-type": content_type,
        },
        httpMethod: "POST",
        uploadType: FS.FileSystemUploadType.BINARY_CONTENT,
        });

        setPred(JSON.parse(response['body'])['Prediction'])
        setProb(JSON.parse(response['body'])['Probability']);
    };

    const uriToBase64 = async (uri) => {
        let base64 = await FS.readAsStringAsync(uri, {
        encoding: FS.EncodingType.Base64,
        });
        return base64;
    };

    const options={
        title: 'Select Image',
        type: 'library',
        options: {
            selectionLimit: 1,
            mediaType: "photo",
            includeBase64: true,
        },
    }
    
    const cameraOptions={
        options: {
            includeBase64: true,
        }
    }

    const TakePhoto = async () => {
        launchCamera(cameraOptions, (response) => {
            console.log('Response = ', response);
        
            if (response.didCancel) {
                alert('User cancelled camera picker');
                return;
            } else if (response.errorCode == 'camera_unavailable') {
                alert('Camera not available on device');
                return;
            } else if (response.errorCode == 'permission') {
                alert('Permission not satisfied');
                return;
            } else if (response.errorCode == 'others') {
                alert(response.errorMessage);
                return;
            }
            console.log('base64 -> ', response.assets[0].base64);
            console.log('uri -> ', response.assets[0].uri);
            console.log('width -> ', response.assets[0].width);
            console.log('height -> ', response.assets[0].height);
            console.log('fileSize -> ', response.assets[0].fileSize);
            console.log('type -> ', response.assets[0].type);
            console.log('fileName -> ', response.assets[0].fileName);
            setPHOTO_uri(response.assets[0].uri)
            console.log('Complete')

            if (response.assets[0].type == "image") {
                toServer({
                  type: response.assets[0].type,
                  base64: response.assets[0].base64,
                  uri: response.assets[0].uri,
                }).then(response);
            } else {
                let base64 = uriToBase64(response.assets[0].uri);
                toServer({
                  type: response.assets[0].type,
                  base64: base64,
                  uri: response.assets[0].uri,
                });
            }
        })
    }

    const UploadImage = () => {
        launchImageLibrary(options, (response) => {
            console.log('Response = ', response);
        
            if (response.didCancel) {
                alert('User cancelled camera picker');
                return;
            } else if (response.errorCode == 'camera_unavailable') {
                alert('Camera not available on device');
                return;
            } else if (response.errorCode == 'permission') {
                alert('Permission not satisfied');
                return;
            } else if (response.errorCode == 'others') {
                alert(response.errorMessage);
                return;
            }
            console.log('base64 -> ', response.assets[0].base64);
            console.log('uri -> ', response.assets[0].uri);
            console.log('width -> ', response.assets[0].width);
            console.log('height -> ', response.assets[0].height);
            console.log('fileSize -> ', response.assets[0].fileSize);
            console.log('type -> ', response.assets[0].type);
            console.log('fileName -> ', response.assets[0].fileName);
            setPHOTO_uri(response.assets[0].uri)
            console.log('Complete')

            if (response.assets[0].type == "image") {
                toServer({
                  type: response.assets[0].type,
                  base64: response.assets[0].base64,
                  uri: response.assets[0].uri,
                }).then(response);
            } else {
                let base64 = uriToBase64(response.assets[0].uri);
                toServer({
                  type: response.assets[0].type,
                  base64: base64,
                  uri: response.assets[0].uri,
                });
            }
        })
    }
    return (
        <SafeAreaView style={styles.mainContainer}>
        <View style={styles.buttonContainer}>
            <AppButton name='clouduploado' 
                       title='Upload Photo' 
                       backgroundColor="#42a5f5" 
                       onPress={() => UploadImage()} 
                       style={styles.but2}
                       />

            <AppButton name='camerao' 
                       title='Take Photo' 
                       backgroundColor="#42a5f5" 
                       onPress={() => TakePhoto()} 
                       style={styles.but1}
                       />
        </View>
        <View style={{ flexGrow: 1, justifyContent: 'center', paddingTop: 100 }}>
            {PHOTO_uri &&
                <Image
                source={{ uri: PHOTO_uri }}
                style={styles.mainPhoto}
                />
            }
        </View>
        <View style={{ flexGrow: 1, justifyContent: 'center', paddingBottom: 120 }}>
            {PHOTO_uri &&
                <Text style={styles.predText}>Prediction: {pred} {'('}{prob}{')'}</Text>
            }
        </View>
        </SafeAreaView>
    )
}

export default Home

const styles = StyleSheet.create({
    mainContainer: {
        flexGrow: 1,
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
        height: '100%',
    },
    mainPhoto: {
        width: 300,
        height: 300,
        paddingBottom: 100
    },
    buttonContainer: {
        position: 'absolute',
        bottom: 10
    },
    but1: {
       position: 'absolute',
       left: 20,
       bottom: 20
    },
    but2: {
        position: 'absolute',
        right: 20,
        bottom: 20
    },
    predText: {
        fontSize: 20,
        color: "#000"
    }
})