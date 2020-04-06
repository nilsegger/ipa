function setSensorRow(id, art, name, raumId, raumName, row) {

    /*
        Erstellt eine Sensor Reihe in der Tabelle.
     */

    let rowId = "sensor-" + id + "-row";
    let viewId = "sensor-" + id + "-view";
    let deleteId = "sensor-" + id + "-delete";
    let openId = "sensor-" + id + "-open";
    let tableId = "#sensor-table";

    let columns = '<td>' + id + '</td><td>' + art + '</td><td>' + name + '</td><td>' + raumName + '</td><td><button class="btn-primary btn" id="' + openId + '">Ansehen</button><button class="btn-info btn" id="' + viewId + '">Editieren</button><button id="' + deleteId + '" class="btn-danger btn">Löschen</button></td>';
    let table = $(tableId);

    if (row === undefined) {
        table.append('<tr id="' + rowId + '">' + columns + '</tr>');
    } else {
        row.html(columns);
    }

    $("#" + viewId).click(
        function () {
            selectedSensor = id;
            $("#sensor-eui").prop('disabled', true);
            $("#sensor-duplicate-alert").hide();
            reset($("#sensor-eui"), id);
            reset($("#sensor-name"), name);
            reset($("#sensor-raum"), raumId);
            reset($("#sensor-art"), art);
            $("#sensor-form").modal('show');
        }
    );

    $("#" + deleteId).click(
        function () {
            Client.delete(endpoint + 'sensoren/' + id, function (response) {
                if (response.status === 200) {
                    $("#" + rowId).remove();
                } else {
                    // TODO fehlermeldig
                }
            })

        }
    );

    $("#" + openId).click(function () {
        window.location.href = self + "sensor.html#"+id;
    });

}


function sensorForm(method, url, row) {

    /*
        Überprüft die Werte in der Form und schickt eine Anfrage an das Backend.
     */

    let duplicateAlert = $("#sensor-duplicate-alert");

    duplicateAlert.hide();

    let eui = $("#sensor-eui");
    let name = $("#sensor-name");
    let art = $("#sensor-art");
    let sensorRaum = $("#sensor-raum");

    let euiValid = check(eui, 16, 16);
    let nameValid = check(name, 3, 100);
    let artValid = check(art);
    let raumValid = check(sensorRaum);

    if (euiValid && nameValid && artValid && raumValid) {
        let euiVal = eui.val();
        let artVal = art.val();
        let nameVal = name.val();
        let raumVal = sensorRaum.val();

        let request = {
            'dev_eui': euiVal,
            'name': nameVal,
            'art': artVal,
            'raum': {
                'id': Number(raumVal)
            }
        };


        method(url, JSON.stringify(request), function (response) {

            if (response.status === 200) {

                setSensorRow(euiVal, artVal, nameVal, raumVal, $("#sensor-raum option:selected").text(), row);

                $("#sensor-form").modal("hide");

            } else if (response.status === 422) {
                duplicateAlert.show();
                // TODO fehlermeldig
            }

        });

    }

}

let selectedSensor;

$(document).ready(function () {

    populateTable('sensoren', loadSensoren, $("#sensor-loader"), $("#sensor-empty"), undefined, function (item) {
        setSensorRow(item["dev_eui"], item["art"], item["name"], item["raum"]["id"], item["raum"]["name"] + ", " + item["stockwerk"]["name"] + ", " + item["gebaeude"]["name"]);
    });

    loadRaeume(function (list) {
        for (let i = 0; i < list.length; i++) {
            let item = list[i];
            $("#sensor-raum").append("<option value='" + item["id"] + "'>" + item["name"] + ", " + item["stockwerk"]["name"] + ", " + item["gebaeude"]["name"] + "</option>");
        }
    });


    $("#create-sensor-btn").click(function () {
        selectedSensor = undefined;
        reset($("#sensor-eui"));
        $("#sensor-eui").prop('disabled', false);
        reset($("#sensor-name"));
        reset($("#sensor-art"));
        reset($("#sensor-raum"));
        $("#sensor-duplicate-alert").hide();
    });

    $("#sensor-save-btn").click(function () {

        if (selectedSensor === undefined) {
            sensorForm(Client.post, endpoint + 'sensoren');
        } else {
            sensorForm(Client.put, endpoint + 'sensoren/' + selectedSensor, $("#sensor-" + selectedSensor + "-row"));
        }

    });
});