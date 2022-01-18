import subprocess as sp

nameOutput = sp.getoutput(
    'adb shell getprop | findstr "ro.product.vendor.model"')
connectedDeviceName = nameOutput[nameOutput.index(':') + 3 : -1]
print(connectedDeviceName)
