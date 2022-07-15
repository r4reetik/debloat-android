from struct import pack
from unicodedata import name
from unittest import expectedFailure
import eel
import subprocess as sp
import json

eel.init("web")

appsJSON = {}


def dumpStorage():
    indices = []
    packageName = []
    appSize = []
    appDataSize = []
    cacheSize = []

    rawData = sp.getoutput("adb shell dumpsys diskstats")
    rawData = rawData.replace("\\n", "").replace("\\", "").replace("\"", "")

    indices.append(rawData.index("Package Names"))
    indices.append(rawData.index("App Sizes"))
    indices.append(rawData.index("App Data Sizes"))
    indices.append(rawData.index("Cache Sizes"))

    packageName = rawData[indices[0] + 18: indices[1] - 2].split(",")
    appSize = rawData[indices[1] + 12: indices[2] - 2].split(",")
    appDataSize = rawData[indices[2] + 17: indices[3] - 2].split(",")
    cacheSize = rawData[indices[3] + 14: len(rawData) - 1].split(",")

    appsStorage = {}

    for i in range(len(packageName)):
        size = "{:.2f}".format((int(appSize[i]) +
                                int(appDataSize[i]) + int(cacheSize[i])) / 1048576)
        appsStorage[packageName[i]] = size

    with open("./web/data/appsStorage.json", "w") as file:
        json.dump(appsStorage, file)


def dumpPermission():
    allAppsOutput = sp.getoutput("adb shell pm list packages -e")
    splitedAllAppsOutput = allAppsOutput.replace("package:", '').split('\n')
    appData = {}

    for package in splitedAllAppsOutput:
        strPerm = "0"
        packagePathOutput = sp.getoutput(
            "adb shell pm list packages -f " + package)
        apkPath = packagePathOutput[8:packagePathOutput.find(
            ".apk") + 4]
        dumpPerms = sp.getoutput(
            "adb shell /data/local/tmp/aapt-arm dump permissions " + apkPath)

        if "CAMERA" in dumpPerms:
            strPerm += "1"
        if "LOCATION" in dumpPerms:
            strPerm += "2"
        if "STORAGE" in dumpPerms:
            strPerm += "3"
        if "PHONE" in dumpPerms:
            strPerm += "4"
        if "CONTACTS" in dumpPerms:
            strPerm += "5"

        appData[package] = strPerm

    with open("./web/data/appsPermission.json", "w") as file:
        json.dump(appData, file)


def fetchAll():
    allAppsOutput = sp.getoutput("adb shell pm list packages -e")
    splitedAllAppsOutput = allAppsOutput.replace("package:", '').split('\n')
    appData = {}
    with open("./web/data/ANS.json", "r") as file1:
        ans = json.load(file1)
        with open("./web/data/appsStorage.json", "r") as file2:
            appStor = json.load(file2)
            with open("./web/data/appsPermission.json", "r") as file3:
                appPerm = json.load(file3)
                for package in splitedAllAppsOutput:
                    try:
                        try:
                            try:
                                appData[package] = {
                                    "name": ans[package], "size": appStor[package], "perms": appPerm[package]}
                            except:
                                appData[package] = {
                                    "name": ans[package], "size": appStor[package], "perms": "0"}
                        except:
                            try:
                                appData[package] = {
                                    "name": ans[package], "size": "0.00", "perms": appPerm[package]}
                            except:
                                appData[package] = {
                                    "name": ans[package], "size": "0.00", "perms": "0"}
                    except:
                        try:
                            try:
                                packagePathOutput = sp.getoutput(
                                    "adb shell pm list packages -f " + package)
                                apkPath = packagePathOutput[8:packagePathOutput.find(
                                    ".apk") + 4]
                                dumpData = sp.getoutput(
                                    "adb shell /data/local/tmp/aapt-arm dump badging " + apkPath + " | findstr application-label:")
                                strPos = dumpData.find("'") + 1
                                dumpData = dumpData[strPos:-1]
                                appData[package] = {"name": dumpData, "size": appStor[package], "perms": appPerm[package]} if dumpData != "" else {
                                    "name": "OS Application", "size": appStor[package], "perms": appPerm[package]}
                            except:
                                packagePathOutput = sp.getoutput(
                                    "adb shell pm list packages -f " + package)
                                apkPath = packagePathOutput[8:packagePathOutput.find(
                                    ".apk") + 4]
                                dumpData = sp.getoutput(
                                    "adb shell /data/local/tmp/aapt-arm dump badging " + apkPath + " | findstr application-label:")
                                strPos = dumpData.find("'") + 1
                                dumpData = dumpData[strPos:-1]
                                appData[package] = {"name": dumpData, "size": appStor[package], "perms": "0"} if dumpData != "" else {
                                    "name": "OS Application", "size": appStor[package], "perms": "0"}
                        except:
                            try:
                                packagePathOutput = sp.getoutput(
                                    "adb shell pm list packages -f " + package)
                                apkPath = packagePathOutput[8:packagePathOutput.find(
                                    ".apk") + 4]
                                dumpData = sp.getoutput(
                                    "adb shell /data/local/tmp/aapt-arm dump badging " + apkPath + " | findstr application-label:")
                                strPos = dumpData.find("'") + 1
                                dumpData = dumpData[strPos:-1]
                                appData[package] = {"name": dumpData, "size": "0.00", "perms": appPerm[package]} if dumpData != "" else {
                                    "name": "OS Application", "size": "0.00", "perms": appPerm[package]}
                            except:
                                packagePathOutput = sp.getoutput(
                                    "adb shell pm list packages -f " + package)
                                apkPath = packagePathOutput[8:packagePathOutput.find(
                                    ".apk") + 4]
                                dumpData = sp.getoutput(
                                    "adb shell /data/local/tmp/aapt-arm dump badging " + apkPath + " | findstr application-label:")
                                strPos = dumpData.find("'") + 1
                                dumpData = dumpData[strPos:-1]
                                appData[package] = {"name": dumpData, "size": "0.00", "perms": "0"} if dumpData != "" else {
                                    "name": "OS Application", "size": "0.00", "perms": "0"}

    appsJSON["all"] = appData


def fetchUser():
    allAppsOutput = sp.getoutput("adb shell pm list packages -3")
    splitedAllAppsOutput = allAppsOutput.replace("package:", '').split('\n')
    appData = {}
    with open("./web/data/ANS.json", "r") as file1:
        ans = json.load(file1)
        with open("./web/data/appsStorage.json", "r") as file2:
            appStor = json.load(file2)
            with open("./web/data/appsPermission.json", "r") as file3:
                appPerm = json.load(file3)
                for package in splitedAllAppsOutput:
                    try:
                        try:
                            try:
                                appData[package] = {
                                    "name": ans[package], "size": appStor[package], "perms": appPerm[package]}
                            except:
                                appData[package] = {
                                    "name": ans[package], "size": appStor[package], "perms": "0"}
                        except:
                            try:
                                appData[package] = {
                                    "name": ans[package], "size": "0.00", "perms": appPerm[package]}
                            except:
                                appData[package] = {
                                    "name": ans[package], "size": "0.00", "perms": "0"}
                    except:
                        try:
                            try:
                                packagePathOutput = sp.getoutput(
                                    "adb shell pm list packages -f " + package)
                                apkPath = packagePathOutput[8:packagePathOutput.find(
                                    ".apk") + 4]
                                dumpData = sp.getoutput(
                                    "adb shell /data/local/tmp/aapt-arm dump badging " + apkPath + " | findstr application-label:")
                                strPos = dumpData.find("'") + 1
                                dumpData = dumpData[strPos:-1]
                                appData[package] = {"name": dumpData, "size": appStor[package], "perms": appPerm[package]} if dumpData != "" else {
                                    "name": "OS Application", "size": appStor[package], "perms": appPerm[package]}
                            except:
                                packagePathOutput = sp.getoutput(
                                    "adb shell pm list packages -f " + package)
                                apkPath = packagePathOutput[8:packagePathOutput.find(
                                    ".apk") + 4]
                                dumpData = sp.getoutput(
                                    "adb shell /data/local/tmp/aapt-arm dump badging " + apkPath + " | findstr application-label:")
                                strPos = dumpData.find("'") + 1
                                dumpData = dumpData[strPos:-1]
                                appData[package] = {"name": dumpData, "size": appStor[package], "perms": "0"} if dumpData != "" else {
                                    "name": "OS Application", "size": appStor[package], "perms": "0"}
                        except:
                            try:
                                packagePathOutput = sp.getoutput(
                                    "adb shell pm list packages -f " + package)
                                apkPath = packagePathOutput[8:packagePathOutput.find(
                                    ".apk") + 4]
                                dumpData = sp.getoutput(
                                    "adb shell /data/local/tmp/aapt-arm dump badging " + apkPath + " | findstr application-label:")
                                strPos = dumpData.find("'") + 1
                                dumpData = dumpData[strPos:-1]
                                appData[package] = {"name": dumpData, "size": "0.00", "perms": appPerm[package]} if dumpData != "" else {
                                    "name": "OS Application", "size": "0.00", "perms": appPerm[package]}
                            except:
                                packagePathOutput = sp.getoutput(
                                    "adb shell pm list packages -f " + package)
                                apkPath = packagePathOutput[8:packagePathOutput.find(
                                    ".apk") + 4]
                                dumpData = sp.getoutput(
                                    "adb shell /data/local/tmp/aapt-arm dump badging " + apkPath + " | findstr application-label:")
                                strPos = dumpData.find("'") + 1
                                dumpData = dumpData[strPos:-1]
                                appData[package] = {"name": dumpData, "size": "0.00", "perms": "0"} if dumpData != "" else {
                                    "name": "OS Application", "size": "0.00", "perms": "0"}

    appsJSON["user"] = appData


def fetchSystem():
    allAppsOutput = sp.getoutput("adb shell pm list packages -s")
    splitedAllAppsOutput = allAppsOutput.replace("package:", '').split('\n')
    appData = {}
    with open("./web/data/ANS.json", "r") as file1:
        ans = json.load(file1)
        with open("./web/data/appsStorage.json", "r") as file2:
            appStor = json.load(file2)
            with open("./web/data/appsPermission.json", "r") as file3:
                appPerm = json.load(file3)
                for package in splitedAllAppsOutput:
                    try:
                        try:
                            try:
                                appData[package] = {
                                    "name": ans[package], "size": appStor[package], "perms": appPerm[package]}
                            except:
                                appData[package] = {
                                    "name": ans[package], "size": appStor[package], "perms": "0"}
                        except:
                            try:
                                appData[package] = {
                                    "name": ans[package], "size": "0.00", "perms": appPerm[package]}
                            except:
                                appData[package] = {
                                    "name": ans[package], "size": "0.00", "perms": "0"}
                    except:
                        try:
                            try:
                                packagePathOutput = sp.getoutput(
                                    "adb shell pm list packages -f " + package)
                                apkPath = packagePathOutput[8:packagePathOutput.find(
                                    ".apk") + 4]
                                dumpData = sp.getoutput(
                                    "adb shell /data/local/tmp/aapt-arm dump badging " + apkPath + " | findstr application-label:")
                                strPos = dumpData.find("'") + 1
                                dumpData = dumpData[strPos:-1]
                                appData[package] = {"name": dumpData, "size": appStor[package], "perms": appPerm[package]} if dumpData != "" else {
                                    "name": "OS Application", "size": appStor[package], "perms": appPerm[package]}
                            except:
                                packagePathOutput = sp.getoutput(
                                    "adb shell pm list packages -f " + package)
                                apkPath = packagePathOutput[8:packagePathOutput.find(
                                    ".apk") + 4]
                                dumpData = sp.getoutput(
                                    "adb shell /data/local/tmp/aapt-arm dump badging " + apkPath + " | findstr application-label:")
                                strPos = dumpData.find("'") + 1
                                dumpData = dumpData[strPos:-1]
                                appData[package] = {"name": dumpData, "size": appStor[package], "perms": "0"} if dumpData != "" else {
                                    "name": "OS Application", "size": appStor[package], "perms": "0"}
                        except:
                            try:
                                packagePathOutput = sp.getoutput(
                                    "adb shell pm list packages -f " + package)
                                apkPath = packagePathOutput[8:packagePathOutput.find(
                                    ".apk") + 4]
                                dumpData = sp.getoutput(
                                    "adb shell /data/local/tmp/aapt-arm dump badging " + apkPath + " | findstr application-label:")
                                strPos = dumpData.find("'") + 1
                                dumpData = dumpData[strPos:-1]
                                appData[package] = {"name": dumpData, "size": "0.00", "perms": appPerm[package]} if dumpData != "" else {
                                    "name": "OS Application", "size": "0.00", "perms": appPerm[package]}
                            except:
                                packagePathOutput = sp.getoutput(
                                    "adb shell pm list packages -f " + package)
                                apkPath = packagePathOutput[8:packagePathOutput.find(
                                    ".apk") + 4]
                                dumpData = sp.getoutput(
                                    "adb shell /data/local/tmp/aapt-arm dump badging " + apkPath + " | findstr application-label:")
                                strPos = dumpData.find("'") + 1
                                dumpData = dumpData[strPos:-1]
                                appData[package] = {"name": dumpData, "size": "0.00", "perms": "0"} if dumpData != "" else {
                                    "name": "OS Application", "size": "0.00", "perms": "0"}

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
    sp.run("adb push aapt-arm /data/local/tmp")
    sp.run("adb shell chmod 0755 /data/local/tmp/aapt-arm")

    dumpStorage()
    dumpPermission()

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
