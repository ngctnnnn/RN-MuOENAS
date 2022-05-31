import { StyleSheet, Text, View } from 'react-native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import React from 'react'
import Home from './screens/Home';

const Stack=createNativeStackNavigator();

const StackNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{
      headerShown: true,
      headerStyle: {
        backgroundColor: '#42a5f5',
      },
      headerTintColor: '#fff',
      headerTitleStyle: {
        fontWeight: 'bold',
      },
    }}>
        <Stack.Group>
            <Stack.Screen name="CS532 Demo App" component={Home}></Stack.Screen>
        </Stack.Group>
    </Stack.Navigator>
  )
}

export default StackNavigator

const styles = StyleSheet.create({})