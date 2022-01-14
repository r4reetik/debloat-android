const adbAction = (result) => {
    if (result) {
        clearInterval(checkADBDevice);
        window.location = "dashboard.html";
    }
}

let checkADBDevice = setInterval(() => {
    eel.checkADB()(adbAction);
}, 1024);
