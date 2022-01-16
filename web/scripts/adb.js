const connectAction = (result) => {
    if (!result) {
        clearInterval(checkConnectedDevice);
        window.location = "connect.html";
    }
}

let checkConnectedDevice = setInterval(() => {
    eel.checkConnect()(connectAction);
}, 1024);


const adbAction = (result) => {
    if (result) {
        clearInterval(checkADBDevice);
        window.location = "dashboard.html";
    }
}

let checkADBDevice = setInterval(() => {
    eel.checkADB()(adbAction);
}, 1024);
