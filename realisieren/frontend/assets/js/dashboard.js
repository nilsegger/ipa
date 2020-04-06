function setSolved(meldungId) {
    /*
        Setzt bearbeitet auf True und schickt eine Anfrage ans Backend, funktioniert diese, so wird die Reihe aus der Tabelle entfernt.
     */
    let request = {
        'bearbeitet': true
    };
    Client.put(endpoint + 'meldungen/' + meldungId.toString(), JSON.stringify(request), function () {
        $("#meldung-" + meldungId).remove();
    });
}

function deleteMeldung(meldungId) {
    /*
        Löscht eine Meldung komplett aus der Datenbank.
     */
    Client.delete(endpoint + 'meldungen/' + meldungId.toString(), function () {
        $("#meldung-" + meldungId).remove();
    })
}


let offset = 0;
let endOfData = false;
let loading = false;

function getMeldungen(callback) {
    /*
        Auflistung aller Meldungen welche noch unbearbeitet sind. Ruft callback mit kompletter Liste auf.
     */

    if (loading || endOfData) return;

    Client.get(endpoint + 'meldungen?type=unbearbeitet&offset=' + offset.toString(), function (response) {

        try {
            if (response.status === 200) {

                let result = JSON.parse(response.responseText);

                offset = result["offset"];
                endOfData = result["is_end"];

                callback(result['list']);
            } else {
                // TODO Fehlermeldig
                callback([]);
            }
        } finally {
            loading = false;
        }
    });
}

function addRow(id, art, datum, beschreibung, melderID, melderName, raumID, raumName, stockwerk, gebaeude) {
    /*
        Erstellt eine Reihe in der Tabelle. Aktiviert Onclick listeners für Buttons.
     */

    let table = $("#meldungen_table");

    let row = `<tr id="meldung-${id}">
            <td>${art}</td>
            <td>${datum}</td>
            <td>${beschreibung} </td>
            <td>${melderName}</td>
            <td><span class="card-title">${raumName} <small
                    class="text-muted">${stockwerk} ${gebaeude}</small></span>
            </td>
            <td>
                <div class="btn-group" role="group" aria-label="Basic example">
                  <button type="button" class="btn btn-success" id="solved-meldung-${id}-btn">Gelöst</button>
                  <button type="button" class="btn btn-danger" id="delete-meldung-${id}-btn">Löschen</button>
                </div>
            </td>
        </tr>`;

    table.append(row);
    $("#solved-meldung-" + id + "-btn").click(function () {
        setSolved(id);
    });
    $("#delete-meldung-" + id + "-btn").click(function () {
        deleteMeldung(id);
    });
}


function loadAdmin() {

    /*
        Ladet Daten für die Administratoren Ansicht und erstellt die Tabelle.
     */

    let spinnerRow = $("#loadingRow");
    let loadMoreBtnRow = $("#loadMoreBtnRow");

    spinnerRow.fadeIn(0);
    loadMoreBtnRow.fadeOut(0);

    getMeldungen(function (list) {

        if (list.length === 0) {
            let table = $("#meldungen_table");
            table.append("<tr><td colspan='6' class='text-primary'>Keine Meldungen vorhanden.</td></tr>");
        }

        for (let i = 0; i < list.length; i++) {
            let item = list[i];
            let datum = new Date(item["datum"] * 1000);
            let art = item["art"];
            let melderId;
            let melderName;

            if (art === 'AUTO') {
                melderId = item["beobachter"]["id"];
                melderName = item["beobachter"]["name"];
            } else {
                melderId = item["personal"]["uuid"];
                melderName = item["personal"]["name"];
            }
            addRow(item["id"], item["art"], datum.toLocaleString("de-CH"), item["beschreibung"], melderId, melderName, item["raum"]["id"], item["raum"]["name"], item["stockwerk"]["name"], item["gebaeude"]["name"]);
        }
        spinnerRow.fadeOut(0);
        if (!endOfData) {
            loadMoreBtnRow.fadeIn(0);
        }
    });

}


function sortByOrt(list) {

    /*
        Sortierungs Algorithmus für die Reinigunspersonal Ansicht.
        Gruppiert zuerst nach Gebäude, danach Stockwerk und schlussendlich die Räume.
     */

    let gebaeude = {};

    for (let i = 0; i < list.length; i++) {
        let item = list[i];

        let gebaeudeID = item["gebaeude"]["id"];
        let stockwerkNiveau = item["stockwerk"]["niveau"];
        let raumID = item["raum"]["id"];

        if (!(gebaeudeID in gebaeude)) {
            gebaeude[gebaeudeID] = {
                'name': item["gebaeude"]["name"],
                'stockwerke': {}
            };
        }
        if (!(stockwerkNiveau in gebaeude[gebaeudeID]['stockwerke'])) {
            gebaeude[gebaeudeID]['stockwerke'][stockwerkNiveau] = {
                'id': item["stockwerk"]["id"],
                'name': item["stockwerk"]["name"],
                'raeume': {}
            };
        }
        if (!(raumID in gebaeude[gebaeudeID]['stockwerke'][stockwerkNiveau]['raeume'])) {
            gebaeude[gebaeudeID]['stockwerke'][stockwerkNiveau]['raeume'][raumID] = {
                'name': item["raum"]["name"],
                'meldungen': []
            }
        }
        gebaeude[gebaeudeID]['stockwerke'][stockwerkNiveau]['raeume'][raumID]['meldungen'].push(item);
    }

    return gebaeude;
}

function loadMaterial(list) {
    /*
        Zählt wie oft eine Meldung eines Beobachters vorkommt und rechnet, nachdem er das Material geholt hat, wie viel davon dargestellt werden muss.
     */
    let beobachterCounter = {};

    for (let i = 0; i < list.length; i++) {
        let item = list[i];
        if (item['art'] !== 'AUTO') continue;
        let beobachter = item['beobachter']['id'];
        if (!(beobachter in beobachterCounter)) beobachterCounter[beobachter] = 0;
        beobachterCounter[beobachter]++;
    }

    let count = 0;
    let materialien = {};

    for (let beobachterKey in beobachterCounter) {
        Client.get(endpoint + 'beobachter/' + beobachterKey + '/materialien', function (response) {
            if (response.status === 200) {
                let items = JSON.parse(response.responseText)['list'];
                for (let i = 0; i < items.length; i++) {
                    let item = items[i];
                    let id = item["id"];
                    let name = item["name"];
                    let anzahl = item["anzahl"] * beobachterCounter[beobachterKey];

                    if (!(id in materialien)) {
                        materialien[id] = {'name': name, 'anzahl': anzahl}
                    } else {
                        materialien[id]['anzahl'] += anzahl
                    }

                }
            } else {
                // TODO Fehlermeldig
            }
            count++;

            if (count === Object.keys(beobachterCounter).length) {
                // Alle Anfragen haben fertig geladen.

                let materialContainer = $("#material-container");

                if (Object.keys(materialien).length === 0) {
                    materialContainer.html("<li class='list-group-item text-primary'>Keine Materialien benötigt.</li>");
                } else {
                    materialContainer.html("");
                }


                for (let id in materialien) {
                    let item = materialien[id];
                    let anzahl = item["anzahl"];

                    materialContainer.append('<li class="list-group-item"><div class="form-check"><input class="form-check-input" type="checkbox" value="" id="material-' + id + '"><label class="form-check-label" for="material-' + id + '">' + anzahl + 'x ' + item["name"] + '</label></div></li>');
                }

            }

        });
    }
}

function saveFeedback(raumID) {
    /*
        Schickt eine Anfrage ans Backend um eine Meldung zu erstellen.
     */
    let beschreibung = $("#beschreibung");
    if (check(beschreibung, 3)) {
        let request = {
            'beschreibung': beschreibung.val(),
            'raum': {'id': raumID}
        };
        Client.post(endpoint + 'meldungen', JSON.stringify(request), function (response) {

            if (response.status === 200) {
                beschreibung.val("");
                $("#meldung-form").modal("hide");
            } else {
                // TODO fehlermeldig
            }

        })
    }
}

let lastData = [];

function loadReinigungspersonal() {
    /*
        Lädt Ansicht für das Reinigunspersonal und stellt die Ansicht anhand von SortByOrt dar.
     */

    let container = $("#personal-container");
    container.fadeIn();

    let meldungenContainer = $("#meldungen-container");

    let loadMoreBtn = $("#meldung-load-more");
    loadMoreBtn.fadeOut(0);

    getMeldungen(function (list) {

        meldungenContainer.html("");

        list.push(...lastData);

        lastData = list;

        loadMaterial(list);

        let sorted = sortByOrt(list);

        if (Object.keys(sorted).length === 0) {
            meldungenContainer.append('<p class="text-primary">Keine offenen Meldungen!</p>');
        }

        for (let gebaeudeKey in sorted) {
            let gebaeude = sorted[gebaeudeKey];
            meldungenContainer.append("<h3>" + gebaeude['name'] + "</h3>");

            let stockwerkKeys = [];
            for (let key in gebaeude['stockwerke']) stockwerkKeys.push(Number(key));
            stockwerkKeys.sort();

            for (let i = 0; i < stockwerkKeys.length; i++) {
                let stockwerk = gebaeude['stockwerke'][stockwerkKeys[i]];

                meldungenContainer.append('<h4 class="stockwerk-title">' + stockwerk['name'] + '</h4>');

                for (let raumId in stockwerk['raeume']) {
                    let raum = stockwerk['raeume'][raumId];

                    let rows = '';

                    for (let i = 0; i < raum['meldungen'].length; i++) {
                        let meldung = raum['meldungen'][i];
                        let id = meldung["id"];
                        let art = meldung['art'];
                        let datum = new Date(meldung["datum"] * 1000);
                        let beschreibung = meldung['beschreibung'];
                        let melder;
                        if (art === 'AUTO') {
                            melder = meldung['beobachter']['name'];
                        } else {
                            melder = meldung['personal']['name'];
                        }

                        rows += '<tr id="meldung-' + id + '"><td>' + art + '</td><td>' + datum.toLocaleString("de-CH") + '</td><td>' + beschreibung + '</td><td>' + melder + '</td><td><button class="btn btn-success" type="button" id="meldung-' + id + '-btn">Gelöst</button></td><td><button class="btn btn-primary" type="button" id="meldung-' + id + '-btn-feedback">Feedback</button></td></tr>';
                    }

                    meldungenContainer.append('<h5 class="raum-title">' + raum["name"] + '</h5>');
                    meldungenContainer.append('<div class="raum-table-container table-responsive"><table class="table table-striped"><thead><tr><th>Art</th>\n' +
                        '            <th>Datum</th>\n' +
                        '            <th>Beschreibung</th>\n' +
                        '            <th>Melder</th>\n' +
                        '            <th>Gelöst</th><th>Feedback</th></tr></thead><tbody>' + rows + '</tbody></table></div>');

                    for (let i = 0; i < raum['meldungen'].length; i++) {
                        let id = raum['meldungen'][i]["id"];

                        $("#meldung-" + id + "-btn").click(function () {
                            setSolved(id);
                        });

                        $("#meldung-" + id + "-btn-feedback").click(function () {

                            $("#meldung-form").modal("show");

                            $("#beschreibung-save-btn").off();
                            $("#beschreibung-save-btn").click(function () {
                                saveFeedback(raum['meldungen'][i]["raum"]["id"]);
                            });

                        })
                    }
                }

            }
        }

        if (!endOfData) loadMoreBtn.fadeIn(0);

    });

}

$(document).ready(function () {

    /*
        Entscheidet durch Rolle im Access Key welche Ansicht dargestellt werden soll.
     */

    if (Auth.getRole() === 'ADMIN') {
        loadAdmin();
        $("#loadMoreBtn").click(loadAdmin);
        $("#admin-container").fadeIn(100);
    } else {
        loadReinigungspersonal();

        $("#meldung-load-more").click(loadReinigungspersonal);


    }
});