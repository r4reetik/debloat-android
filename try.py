import subprocess as sp
import json

appData = {}

allAppsOutput = sp.getoutput("adb shell pm list packages -e")
splitedAllAppsOutput = allAppsOutput.replace("package:", '').split('\n')
for package in splitedAllAppsOutput:
    packagePathOutput = sp.getoutput(
        "adb shell pm list packages -f " + package)
    pPath = packagePathOutput[8:packagePathOutput.find(
        ".apk") + 4]
    dumpData = sp.getoutput(
        "adb shell aapt dump badging "+pPath+" | findstr application-label:")

    appData[package] = dumpData[dumpData.find(
        "'")+1:-1] if dumpData[dumpData.find("'")+1:-1] != "" else "OS Application"

print(appData)
