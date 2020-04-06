let sensorArt;

function preparePage(eui, callback) {

    /*
        Lädt die Attribute eines Sensors von der API.
     */

    Client.get(endpoint + 'sensoren/' + eui, function (response) {

        if (response.status === 200) {

            let result = JSON.parse(response.responseText);

            sensorArt = result["art"];

            $("#sensor-eui").html(eui);
            $("#sensor-name").html(result["name"]);
            $("#sensor-gebaeude").html(result["gebaeude"]["name"]);
            $("#sensor-stockwerk").html(result["stockwerk"]["name"]);
            $("#sensor-raum").html(result["raum"]["name"]);

            callback();
        } else {
            // TODO fehlermeldig
        }

    });

}


function beobachterMeldungErstellen(beobachterId) {

    /*
        Funktion zum Erstellen einer Meldung.
     */

    let beschreibung = $("#beschreibung");

    if (check(beschreibung, 3)) {

        let request = {
            'beschreibung': beschreibung.val(),
            'beobachter': {'id': beobachterId}
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

function displayBeobachter(list) {

    /*
        Stellt alle Beobachter des Sensors in einer Tabelle dar und aktiviert die Buttons zum auslösen einer Meldung.
     */

    let table = $("#sensor-beobachter");

    for (let i = 0; i < list.length; i++) {

        let item = list[i];
        let id = 'beobachter-' + item["id"] + '-btn';

        let row = '<tr><td>' + item['art'] + '</td><td>' + item['name'] + '</td><td>' + item['ausloeserWert'] + '</td><td>' + item['stand'] + '</td><td>' + item['wertName'] + '</td><td><button id="' + id + '" class="btn btn-primary">Meldung auslösen</button></td></tr>';
        table.append(row);

        $("#" + id).click(function () {
            $("#meldung-form").modal("show");
            $('#beschreibung-save-btn').off('click');
            $("#beschreibung-save-btn").click(function () {
                beobachterMeldungErstellen(item["id"]);
            });
        })
    }

}

let diagramCounter = 0;

function createDiagram(title, labels, datasets) {
    /*
        Erstellt ein Chart.js Diagramm im Diagram Container.
     */
    let container = $("#diagram-container");
    diagramCounter += 1;
    let id = "diagram-" + diagramCounter;
    let chart_html = '<div class="mt-6"><h5>' + title + '</h5><div class="mt-6"><div class="table-responsive"><canvas id="' + id + '" style="min-height: 400px"></canvas></div></div></div>';
    container.append(chart_html);
    let ctx = document.getElementById(id).getContext('2d');

    let chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: false,
            maintainAspectRatio: false
        }
    });
}

function findMinMaxAvg(values) {
    /*
        Findet den kleinsten und grössten Wert in einem Array und berechnet auch noch den Durchschnittlichen.
     */

    let min;
    let max;
    let avg = 0;

    for (let i = 0; i < values.length; i++) {
        let value = values[i];
        if (min === undefined || value < min) min = value;
        if (max === undefined || value > max) max = value;
        avg += value;
    }

    return [min, max, avg / values.length];
}

function createDataset(label, data, color = "#c84646") {
    /*
        Erstellt ein Dataset welches von Chart.js gelesen werden kann.
     */
    let dataset = {
        label: label,
        data: data,
        borderWidth: 1,
        fill: false,
        borderColor: color,
    };

    return dataset;
}

let displayDelta = 3600000;
let values;

function displayValues() {

    /*
        Gruppiert die Werte nach dem displayDelta Kriterium und stellt diese mit createDiagram dar.
     */

    let container = $("#diagram-container");
    if (values.length === 0) {
        container.html("<p class='text-primary'><b>Keine Daten gefunden.</b></p>");
        return;
    } else {
        container.html("");
    }

    let labels = [];
    let groupedValues = {};

    let lastReceived;
    let label;

    for (let i = 0; i < values.length; i++) {
        let value = values[i];
        let received = new Date(value['erhalten'] * 1000);

        if (lastReceived === undefined || received.valueOf() - lastReceived.valueOf() >= displayDelta) {
            // Offset wurde überschritten, somit wird ein neues Label erstellt.
            label = received.toLocaleString('de-CH');
            labels.push(label);
            lastReceived = received;
            groupedValues[label] = [];


        }
        groupedValues[label].push(value);
    }

    let counts = [];
    // Beinhaltet min, max und avg pro Sensor Wert
    let valueCounts = {};
    for (let i = 0; i < labels.length; i++) {
        let label = labels[i];

        // Zählerstand Werte
        counts.push(groupedValues[label].length);

        let specificValueCounts = {};

        for(let q = 0; q < groupedValues[label].length; q++) {
            let data = JSON.parse(groupedValues[label][q]['dekodiertJSON']);

            for(let key in data) {
                if(!(key in specificValueCounts)) specificValueCounts[key] = [];
                specificValueCounts[key].push(data[key]);
            }
        }

        for(let key in specificValueCounts) {
            if(!(key in valueCounts)) valueCounts[key] = {'min': [], 'max': [], 'avg': []};
            let result = findMinMaxAvg(specificValueCounts[key]);
            valueCounts[key]['min'].push(result[0]);
            valueCounts[key]['max'].push(result[1]);
            valueCounts[key]['avg'].push(result[2]);
        }
    }

    createDiagram('Zählerstand', labels, [createDataset("Anzahl Packete", counts)]);

    for(let key in valueCounts) {
        createDiagram(key.toUpperCase(), labels, [
            createDataset('Min', valueCounts[key]['min']),
            createDataset('Max', valueCounts[key]['max'], "#802E9E"),
            createDataset('Avg', valueCounts[key]['avg'], "#C8FF46"),
        ])
    }

}

function dateToInputValue(date) {
    /*
        Verwandelt ein Date Object in einen String welcher von Input[type=date] gelesen werden können.
        Kopiert von https://stackoverflow.com/questions/28729634/set-values-in-input-type-date-and-time-in-javascript
     */
    return date.toISOString().slice(0, 10);
}


$(document).ready(function () {

    let eui = window.location.href.split('#')[1];

    let inpFrom = $("#from");
    let inpTo = $("#to");
    let filter = $("#filter-btn");

    if (eui !== undefined && eui) {
        preparePage(eui, function () {
            let max = Date.now() / 1000;
            let min = max - (60 * 60 * 24 * 7);

            inpFrom.val(dateToInputValue(new Date(min * 1000)));
            inpTo.val(dateToInputValue(new Date(max * 1000)));

            loadSensorWerte(eui, min, max, function (list) {
                values = list;
                displayValues();
            });
            loadSensorBeobachter(eui, displayBeobachter);
        });

        filter.click(function () {

            let h24 = 60 * 60 * 24;
            let min = (new Date(inpFrom.val())).valueOf() / 1000 - h24;
            let max = ((new Date(inpTo.val())).valueOf() / 1000) + h24;

            loadSensorWerte(eui, min, max, function (list) {
                values = list;
                displayValues();
            });
        });

        $("#filter-delta-btn").click(function () {
            displayDelta = Number($("#delta").val());
            displayValues();
        });
    }


});