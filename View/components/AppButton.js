import { StyleSheet, Text, View } from 'react-native'
import React from 'react'
import Icon from 'react-native-vector-icons/AntDesign'
const AppButton = (props) => {
  return(
    <View style={props.style}>
        <Icon.Button
            name={props.name}
            backgroundColor={props.backgroundColor}
            onPress={props.onPress}
            size={20}
            borderRadius={15}
            
        >
            <Text style={styles.AppText}>{props.title}</Text>
        </Icon.Button>
    </View>
  )
}

export default AppButton

const styles = StyleSheet.create({
    AppText: {
        fontSize: 20,
        color: '#fff'
    }
})