import React, {Component} from 'react';
import {Alert, AppRegistry, StyleSheet, Text, View} from 'react-native';
import Button from './assets/button';

var styles = StyleSheet.create({
    hello: {
        fontSize: 20,
        textAlign: 'center',
        margin: 10,
    },
    button: {
        fontSize: 20,
        padding: 10,
        color: 'black',
        backgroundColor: 'grey',
        borderRadius: 10,
        borderStyle: 'solid',
        borderColor: 'black',
        marginRight:40,
        marginLeft:40,
        marginTop:10,
    },
});

export default class App extends Component {
    // _onPressButton = () => Alert.alert('You pressed the button !');
    render() {
        return (
            <View
                style={{
                    flex: 1,
                    justifyContent: 'center',
                    alignItems: 'center',
                }}
            >
                <Text style={styles.hello}>Code base for CS523 project</Text>

                {/* <Button name="camera"
                    style={styles.button}
                    onPress={() => {
                        alert('You tapped the button!');
                    }}
                >
                    This is a button
                </Button> */}
                <Button name="camera"/>
            </View>
        );
    }
}

AppRegistry.registerComponent('Test', () => App);
