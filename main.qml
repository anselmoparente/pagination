import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.3

Window {
    width: 1280
    height: 720
    visible: true
    title: qsTr("Paginação do Laion")

    Rectangle {
        width: 1280
        height: 720
        color: "#1e5da0"

        Rectangle {
            id: rectangle
            x: 15
            y: 19
            width: 810
            height: 200
            color: "#ffffff"

            RadioButton {
                id: radioButton
                x: 76
                y: 75
                height: 50
                text: qsTr("FIFO")
            }

            RadioButton {
                id: radioButton1
                x: 250
                y: 75
                height: 50
                text: qsTr("SEGUNDA CHANCE")
            }

            RadioButton {
                id: radioButton2
                x: 500
                y: 75
                height: 50
                text: qsTr("NUR")
            }

            RadioButton {
                id: radioButton3
                x: 661
                y: 75
                height: 50
                text: qsTr("MUR")
            }
        }

        Button {
            id: button
            x: 831
            y: 77
            text: qsTr("Escolha o arquivo")
            checked: false
            display: AbstractButton.TextOnly
            checkable: false
            flat: false
            icon.cache: true
            icon.color: "#ddff0000"
            icon.width: 48
            onClicked: {
                fileDialog.open()
            }
        }

        Text {
            id: text1
            x: 831
            y: 140
            color: "#5c2727"
            text: qsTr("Nome do arquivo carregado")
            font.pixelSize: 24
        }

        Rectangle {
            id: rectangle1
            x: 15
            y: 261
            width: 1250
            height: 443
            color: "#ffffff"

            Text {
                id: text2
                x: 17
                y: 40
                text: qsTr("Estado final: ")
                font.pixelSize: 24
            }

            Text {
                id: text3
                x: 17
                y: 210
                text: qsTr("Número de faltas:")
                font.pixelSize: 24
            }

            Text {
                id: text4
                x: 17
                y: 280
                text: qsTr("Número de acertos:")
                font.pixelSize: 24
            }

            Text {
                id: text5
                x: 17
                y: 350
                text: qsTr("Porcentagem de acertos: ")
                font.pixelSize: 24
            }
        }
        FileDialog {
                id: fileDialog
                title: "Escolha um arquivo"
                folder: shortcuts.home
                selectFolder: false

                onAccepted: {
                    console.log("Arquivo selecionado:", fileDialog.fileUrls)
                    // Faça algo com o arquivo selecionado
                }

                onRejected: {
                    console.log("Seleção de arquivo cancelada")
                }
            }
    }



    Connections{
            target: backend
        }
}
