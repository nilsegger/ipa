
function setSolved(meldungId) {
    let request = {
      'bearbeitet': true
    };
    Client.put(endpoint + 'meldungen/' + meldungId.toString(), JSON.stringify(request), function () {
        $("#meldung-" + meldungId).remove();
    });
}

function deleteMeldung(meldungId) {
    Client.delete(endpoint + 'meldungen/' + meldungId.toString(), function () {
        $("#meldung-" + meldungId).remove();
    })
}

function addRow(id, art, datum, beschreibung, melderID, melderName, raumID, raumName, stockwerk, gebaeude) {
    let table = $("#meldungen_table");

    let row = `<tr id="meldung-${id}">
            <td>Art</td>
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

function hideTableFooter(spinnerRow, loadMoreBtnRow) {
    spinnerRow.fadeOut(0);
    loadMoreBtnRow.fadeOut(0);
}

let offset = 0;
let endOfData = false;
let loading = false;

function load() {

    if (loading || endOfData) return;

    let spinnerRow = $("#loadingRow");
    let loadMoreBtnRow = $("#loadMoreBtnRow");


    Client.get(endpoint + 'meldungen?type=unbearbeitet&offset=' + offset.toString(), function (response) {

        try {
            if (response.status === 200) {

                let result = JSON.parse(response.responseText);

                offset = result["offset"];
                endOfData = result["is_end"];

                for (let i = 0; i < result['list'].length; i++) {
                    let item = result['list'][i];
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
                    addRow(item["id"], item["art"], datum.toLocaleString(), item["beschreibung"], melderId, melderName, item["raum"]["id"], item["raum"]["name"], item["stockwerk"]["name"], item["gebaeude"]["name"]);
                }

            } else {
                // TODO fehlermeldung
            }
        } finally {
            loading = false;
            if (endOfData) {
                hideTableFooter(spinnerRow, loadMoreBtnRow);
            } else {
                hideTableFooter(spinnerRow, loadMoreBtnRow);
                loadMoreBtnRow.fadeIn(0);
            }
        }


    });
}

$(document).ready(function () {
    load();

    $("#loadMoreBtn").click(load);
});