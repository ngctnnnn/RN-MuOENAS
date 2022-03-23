import React, {Component} from 'react';
import {Alert, AppRegistry, StyleSheet, Text, View} from 'react-native';
import Button from 'react-native-button';

var styles = StyleSheet.create({
    hello: {
        fontSize: 20,
        textAlign: 'center',
        margin: 10
    },
    button: {
        fontSize: 20,
        padding: 10,
        color: 'white',
        backgroundColor: 'green',
        borderRadius: 10
    }
  });

export default class App extends Component {
    _onPressButton = () => (
        Alert.alert("U pressed the button !")
    )
    render() {
        return(<View style={{
            flex: 1,
            justifyContent: 'center',
            alignItems: 'center'
        }}>

        <Text style={styles.hello}>Code base for CS523 project</Text>

        <Button style={styles.button}
        onPress={() => { navi}}
        >This is a button</Button>

        </View>);
    }
}


AppRegistry.registerComponent('Test', () => App)