function setBeobachterRow(id, art, name, wertName, ausloeser, stand, sensorId, sensorName, row) {
    /*
        Erstellt eine Reihe in der Tabelle und aktiviert Onclick Listener für die Buttons.
     */
    let rowId = "beobachter-" + id + "-row";
    let viewId = "beobachter-" + id + "-view";
    let deleteId = "beobachter-" + id + "-delete";
    let tableId = "#beobachter-table";

    let columns = '<td>' + art + '</td><td>' + name + '</td><td>' + sensorName + '</td><td>' + wertName + '</td><td>' + ausloeser + '</td><td>' + stand + '</td><td><button class="btn-info btn" id="' + viewId + '">Editieren</button><button id="' + deleteId + '" class="btn-danger btn">Löschen</button></td>';
    let table = $(tableId);

    if (row === undefined) {
        table.append('<tr id="' + rowId + '">' + columns + '</tr>');
    } else {
        row.html(columns);
    }

    $("#" + viewId).click(
        function () {
            selectedBeobachter = id;
            reset($("#beobachter-art"), art);
            reset($("#beobachter-name"), name);
            reset($("#beobachter-wert-name"), wertName);
            reset($("#beobachter-ausloeser"), ausloeser);
            reset($("#beobachter-stand"), stand);
            $("#beobachter-form").modal('show');
        }
    );

    $("#" + deleteId).click(
        function () {
            Client.delete(endpoint + 'beobachter/' + id, function (response) {
                if (response.status === 200) {
                    $("#" + rowId).remove();
                } else {
                    // TODO fehlermeldig
                }
            })

        }
    );

}


function beobachterForm(method, url, id, row) {

    /*
        Bei Aufruf, validiert Inhalt der Benutzereingaben und schickt danach die Anfrage ans Backend.
        Wenn die Anfrage mit 200 Antwortet, so wird eine Reihe in der Tabelle erstellt oder aktualisiert.
     */

    let art = $("#beobachter-art");
    let name = $("#beobachter-name");
    let sensor = $("#beobachter-sensor");
    let stand = $("#beobachter-stand");
    let ausloeser = $("#beobachter-ausloeser");
    let wertName = $("#beobachter-wert-name");

    let artValid = check(art);
    let nameValid = check(name, 3, 100);
    let sensorValid = check(sensor);
    let ausloeserValid = check(ausloeser);

    if (!artValid || !nameValid || !sensorValid || !ausloeserValid) {
        return;
    } else if (art.val() === 'ZAEHLERSTAND' || check(wertName)) {

        let artVal = art.val();
        let nameVal = name.val();
        let sensorVal = sensor.val();
        let ausloeserVal = ausloeser.val();
        let wertNameVal = wertName.val();
        let standVal = stand.val();

        standVal = standVal ? Number(standVal) : 0;

        let request = {
            'art': artVal,
            'name': nameVal,
            'sensor': { 'dev_eui': sensorVal},
            'ausloeserWert': Number(ausloeserVal),
            'wertName': wertNameVal,
            'stand': standVal
        };

        method(url, JSON.stringify(request), function (response) {

            if (response.status === 200) {
                if (id === undefined) {
                    id = JSON.parse(response.responseText)["id"];
                }
                setBeobachterRow(id, artVal, nameVal, wertNameVal, ausloeserVal, standVal, sensorVal, $("#beobachter-sensor option:selected").text(), row);
                $("#beobachter-form").modal("hide");
            } else {
                // TODO fehlermeldig
            }

        });

    }

}

let selectedBeobachter;

$(document).ready(function () {

    /*
        Erstellt die Tabelle und bereitet die Form vor.
     */

    populateTable('beobachter', loadBeobachter, $("#beobachter-loader"), $("#beobachter-empty"), undefined, function (item) {
        setBeobachterRow(item["id"], item["art"], item["name"], item["wertName"], item["ausloeserWert"], item["stand"], item["sensor"]["id"], item["sensor"]["name"]);
    });

    loadSensoren(function (list) {
        for(let i = 0; i < list.length; i++) {
            $("#beobachter-sensor").append('<option value="'+list[i]['dev_eui']+'">'+list[i]['name']+'</option>');
        }
    });

    $("#create-beobachter-btn").click(function () {
        selectedBeobachter = undefined;
        reset($("#beobachter-art"));
        reset($("#beobachter-name"));
        reset($("#beobachter-wert-name"));
        reset($("#beobachter-ausloeser"));
        reset($("#beobachter-stand"));
    });

    $("#beobachter-save-btn").click(function () {
        if (selectedBeobachter === undefined) {
            beobachterForm(Client.post, endpoint + 'beobachter');
        } else {
            beobachterForm(Client.put, endpoint + 'beobachter/' + selectedBeobachter, selectedBeobachter, $("#beobachter-" + selectedBeobachter + "-row"));
        }

    });
});