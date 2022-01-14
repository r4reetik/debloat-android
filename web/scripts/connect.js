const connectAction = (result) => {
    if (result) {
        clearInterval(checkConnectedDevice);
        window.location = "adb.html";
    }
}

let checkConnectedDevice = setInterval(() => {
    eel.checkConnect()(connectAction);
}, 1024);
