import eel
import subprocess as sp
import json

eel.init("web")

appsJSON = {}
storageDumps = {}


def dumpStorage():
    storageDumps["output"] = sp.getoutput("adb shell dumpsys diskstats")


def fetchAll():
    allAppsOutput = sp.getoutput("adb shell pm list packages -e")
    splitedAllAppsOutput = allAppsOutput.replace("package:", '').split('\n')
    appData = {}
    for package in splitedAllAppsOutput:
        packagePathOutput = sp.getoutput(
            "adb shell pm list packages -f " + package)
        apkPath = packagePathOutput[8:packagePathOutput.find(".apk") + 4]
        dumpData = sp.getoutput(
            "adb shell aapt dump badging " + apkPath + " | findstr application-label:")
        strPos = dumpData.find("'") + 1
        dumpData = dumpData[strPos:-1]
        appData[package] = dumpData if dumpData != "" else "OS Application"
    appsJSON["all"] = appData


def fetchUser():
    userAppsOutput = sp.getoutput("adb shell pm list packages -3")
    splitedUserAppsOutput = userAppsOutput.replace("package:", '').split('\n')
    appData = {}
    for package in splitedUserAppsOutput:
        packagePathOutput = sp.getoutput(
            "adb shell pm list packages -f " + package)
        apkPath = packagePathOutput[8:packagePathOutput.find(".apk") + 4]
        dumpData = sp.getoutput(
            "adb shell aapt dump badging " + apkPath + " | findstr application-label:")
        strPos = dumpData.find("'") + 1
        dumpData = dumpData[strPos:-1]
        appData[package] = dumpData if dumpData != "" else "OS Application"
    appsJSON["user"] = appData


def fetchSystem():
    systemAppsOutput = sp.getoutput("adb shell pm list packages -s")
    splitedSystemAppsOutput = systemAppsOutput.replace(
        "package:", ''
    ).split('\n')
    appData = {}
    for package in splitedSystemAppsOutput:
        packagePathOutput = sp.getoutput(
            "adb shell pm list packages -f " + package)
        apkPath = packagePathOutput[8:packagePathOutput.find(".apk") + 4]
        dumpData = sp.getoutput(
            "adb shell aapt dump badging " + apkPath + " | findstr application-label:")
        strPos = dumpData.find("'") + 1
        dumpData = dumpData[strPos:-1]
        appData[package] = dumpData if dumpData != "" else "OS Application"
    appsJSON["system"] = appData


@eel.expose
def checkADB():
    adbOutput = sp.getoutput("adb devices")
    splitedADBOutput = adbOutput.split('\n')
    deviceIndex = splitedADBOutput.index("List of devices attached") + 1

    if len(splitedADBOutput) > deviceIndex + 2:
        print("Please remove all other devices with ADB permissions.")
        return 0
    elif splitedADBOutput[deviceIndex] != '':
        phoneInfo = splitedADBOutput[deviceIndex].split()
        if phoneInfo[1] != "unauthorized":
            print("ADB connected on", phoneInfo[0])
            connectedDeviceSerial = phoneInfo[0]
            return 1
        else:
            print("Unauthorized to access ADB.")
            return 0
    else:
        print("No ADB enabled phone found.")
        return 0


@eel.expose
def checkConnect():
    connectedOutput = sp.getoutput("powershell Get-PnpDevice -PresentOnly")
    splitedConnectedOutput = connectedOutput.split('\n')
    deviceIndex = -1

    for i in range(len(splitedConnectedOutput)):
        if "WPD" in splitedConnectedOutput[i] or "Android" in splitedConnectedOutput[i]:
            deviceIndex = i
            break

    if deviceIndex > -1:
        deviceInfo = splitedConnectedOutput[deviceIndex].split()[2:]
        deviceInfo.pop()
        deviceName = ' '.join(deviceInfo)
        print("Connected Device:", deviceName)
        connectedDeviceName = deviceName
        return 1
    else:
        print("Device not Connected.")
        return 0


@eel.expose
def populateApps():
    # dumpStorage()
    # with open("./web/data/storageDumps.json", "w") as file:
    #     json.dump(storageDumps, file)

    fetchAll()
    fetchUser()
    fetchSystem()
    with open("./web/data/phoneApps.json", "w") as file:
        json.dump(appsJSON, file)


@eel.expose
def uninstallApp(package):
    try:
        sp.call("adb shell pm clear " + package, shell=True)
    except:
        print("Java security exception of android.permission.CLEAR_APP_USER_DATA")
    sp.call("adb shell pm uninstall --user 0 " + package, shell=True)


@eel.expose
def populateDeviceInfo():
    nameOutput = sp.getoutput(
        'adb shell getprop | findstr "ro.product.vendor.model"'
    )
    connectedDeviceName = nameOutput[nameOutput.index(':') + 3: -1]
    serialOutput = sp.getoutput(
        'adb shell getprop | findstr "ro.boot.serialno"'
    )
    connectedDeviceSerial = serialOutput[serialOutput.index(':') + 3: -1]
    return [connectedDeviceName, connectedDeviceSerial]


eel.start("connect.html", mode="edge")
