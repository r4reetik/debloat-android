selectedAppCategory = "all";
selectedApps = [];

const insertInTable = () => {
    fetch("../data/phoneApps.json")
        .then((response) => response.json())
        .then((appsJSON) => {
            document.querySelector("body > div > div.row.my-3.px-3 > div > table > tbody").innerHTML = "";
            appsJSON[selectedAppCategory].forEach((package) => {
                document.querySelector("body > div > div.row.my-3.px-3 > div > table > tbody").insertAdjacentHTML(
                    "beforeend",
                    `<th scope="row">
                            <input
                                class="form-check-input big-checkbox"
                                type="checkbox"
                                name="appsSelected"
                                value="${package}"
                            />
                        </th>
                        <td>---x---</td>
                        <td>${package}</td>`
                );
            });
        });
};

let radioButtonsElement = document.querySelectorAll('input[name="appsCategory"]');
radioButtonsElement.forEach((element) => {
    element.addEventListener("click", () => {
        selectedAppCategory = element.value;
        insertInTable();
    });
});

document.getElementById("btnUninstall").addEventListener("click", () => {
    let checkboxAppsElement = document.querySelectorAll('input[name="appsSelected"]');
    selectedApps = [];
    checkboxAppsElement.forEach((element) => {
        if (element.checked) {
            eel.uninstallApp(element.value);
        }
    });

    eel.populateApps()(insertInTable);
});

eel.populateApps()(insertInTable);
