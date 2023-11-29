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
                id: radioButtonFIFO
                x: 75
                y: 75
                height: 50
                text: qsTr("FIFO")
                onClicked: {
                    backend.changeOption(0)
                }
            }

            RadioButton {
                id: radioButtonSC
                x: 250
                y: 75
                height: 50
                text: qsTr("SEGUNDA CHANCE")
                onClicked: {
                    backend.changeOption(1)
                }
            }

            RadioButton {
                id: radioButtonNUR
                x: 500
                y: 75
                height: 50
                text: qsTr("NUR")
                onClicked: {
                    backend.changeOption(2)
                }
            }

            RadioButton {
                id: radioButtonMUR
                x: 660
                y: 75
                height: 50
                text: qsTr("MUR")
                onClicked: {
                    backend.changeOption(3)
                }
            }
        }

        Button {
            id: buttonFile
            x: 830
            y: 132
            text: qsTr("Escolher arquivo")
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

        Button {
            id: buttonRun
            x: 1030
            y: 132
            text: qsTr("Rodar")
            checked: false
            display: AbstractButton.TextOnly
            checkable: false
            flat: false
            icon.cache: true
            icon.color: "#ddff0000"
            icon.width: 48
            onClicked: {
                backend.run()
            }
        }

        Text {
            id: textFile
            x: 831
            y: 186
            color: "#5c2727"
            text: 'Escolha um arquivo'
            font.pixelSize: 18
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

        TextField {
            id: textFieldFrames
            x: 830
            y: 27
            placeholderText: qsTr("Frames")
            onEditingFinished: {
                if (!isNaN(parseFloat(textFieldFrames.text)) && isFinite(textFieldFrames.text)) {
                     backend.changeFrames(textFieldFrames.text)
                }
            }
        }

        TextField {
            id: textFieldReference
            x: 830
            y: 80
            placeholderText: qsTr("Referências")
            onEditingFinished: {
                if (!isNaN(parseFloat(textFieldReference.text)) && isFinite(textFieldReference.text)) {
                    backend.changeReferences(textFieldReference.text)
                }
            }
        }

        FileDialog {
                id: fileDialog
                title: "Escolha um arquivo"
                folder: shortcuts.home
                selectFolder: false
                selectExisting: true
                nameFilters: ["Text files (*.txt)"]

                onAccepted: { 
                    textFile.text = 'Arquivo escolhido'
                    backend.changeFileName(fileDialog.fileUrls)
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
