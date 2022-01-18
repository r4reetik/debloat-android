selectedAppCategory = "all";
searchString = "";

const insertDeviceInfo = (details) => {
    document.getElementById("displayDevice").innerText = details[0];
    document.getElementById("displaySerial").innerText = details[1];
};

const insertInTable = () => {
    eel.populateDeviceInfo()(insertDeviceInfo);

    fetch("../data/phoneApps.json")
        .then((response) => response.json())
        .then((appsJSON) => {
            document.querySelector("body > div > div.row.my-3.px-3 > div > table > tbody").innerHTML = "";
            appsJSON[selectedAppCategory].forEach((package) => {
                if (package.toLowerCase().includes(searchString.toLowerCase()) || searchString === "") {
                    document.querySelector("body > div > div.row.my-3.px-3 > div > table > tbody").insertAdjacentHTML(
                        "beforeend",
                        `<tr id="${package}">
                            <th scope="row">
                                <input
                                    class="form-check-input big-checkbox"
                                    type="checkbox"
                                    name="appsSelected"
                                    value="${package}"
                                />
                            </th>
                            <td>---x---</td>
                            <td>${package}</td>
                        </tr>`
                    );
                }
            });
        });
};

document.getElementById("inputSearch").addEventListener("input", (obj) => {
    searchString = obj.target.value;
    insertInTable();
});

let radioButtonsElement = document.querySelectorAll('input[name="appsCategory"]');
radioButtonsElement.forEach((element) => {
    element.addEventListener("click", () => {
        selectedAppCategory = element.value;
        insertInTable();
    });
});

document.getElementById("btnUninstall").addEventListener("click", () => {
    let checkboxAppsElement = document.querySelectorAll('input[name="appsSelected"]');
    let count = 0;
    checkboxAppsElement.forEach((element) => {
        if (element.checked) {
            ++count;
            eel.uninstallApp(element.value);
        }
    });

    if (count > 0) {
        swal("Good job!", "Selected apps successfully uninstalled.", "success");
    } else {
        swal("Oops!", "No apps selected", "error");
    }

    eel.populateApps()(insertInTable);
});

document.getElementById("btnRefresh").addEventListener("click", () => {
    eel.populateApps()(insertInTable);
});

eel.populateApps()(insertInTable);

const adbAction = (result) => {
    if (!result) {
        clearInterval(checkADBDevice);
        window.location = "adb.html";
    }
};

let checkADBDevice = setInterval(() => {
    eel.checkADB()(adbAction);
}, 1024);
