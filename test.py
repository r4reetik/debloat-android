from operator import index
import subprocess as sp


def checkADB():
    adbOutput = sp.getoutput("adb devices")
    splitedADBOutput = adbOutput.split('\n')
    deviceIndex = splitedADBOutput.index("List of devices attached") + 1

    if len(splitedADBOutput) > deviceIndex + 2:
        print("Please remove all other devices with ADB permissions.")
    elif splitedADBOutput[deviceIndex] != '':
        phoneInfo = splitedADBOutput[deviceIndex].split()
        if phoneInfo[1] != "unauthorized":
            print("ADB connected on", phoneInfo[0])
        else:
            print("Unauthorized to access ADB.")
    else:
        print("No ADB enabled phone found.")


def checkConnect():
    connectedOutput = sp.getoutput("powershell Get-PnpDevice -PresentOnly")
    splitedConnectedOutput = connectedOutput.split('\n')
    deviceIndex = -1

    for i in range(len(splitedConnectedOutput)):
        if "WPD" in splitedConnectedOutput[i]:
            deviceIndex = i
            break

    if deviceIndex > -1:
        deviceInfo = splitedConnectedOutput[deviceIndex].split()[2:]
        deviceInfo.pop()
        deviceName = ' '.join(deviceInfo)
        print("Connected Device:", deviceName)
    else:
        print("Device not Connected.")
