from ast import Try
import subprocess as sp
import json

print("  [START] -----X-----")

print("  [SETUP] -----X-----")
sp.run("adb push aapt-arm /data/local/tmp")
sp.run("adb shell chmod 0755 /data/local/tmp/aapt-arm")

print("[LOADING] Installed Packages")
allAppsOutput = sp.getoutput("adb shell pm list packages -e")
splitedAllAppsOutput = allAppsOutput.replace("package:", '').split('\n')

print("[LOADING] Present JSON")
appData = {}
with open("./web/data/ANS.json", "r") as file:
    appData = json.load(file)

for package in splitedAllAppsOutput:
    try:
        appData[package]
        print("  [CHECK] " + package)
    except:
        print("[PROCESS] " + package)
        packagePathOutput = sp.getoutput(
            "adb shell pm list packages -f " + package
        )
        apkPath = packagePathOutput[8:packagePathOutput.find(".apk") + 4]
        dumpData = sp.getoutput(
            "adb shell /data/local/tmp/aapt-arm dump badging " +
            apkPath + " | findstr application-label:"
        )
        strPos = dumpData.find("'") + 1
        dumpData = dumpData[strPos:-1]
        appData[package] = dumpData if dumpData != "" else "OS Application"

print("[PUSHING] Data to JSON")
with open("./web/data/ANS.json", "w") as file:
    json.dump(appData, file)

print("    [END] -----X-----")
