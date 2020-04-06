let sensorArt;

function preparePage(eui, callback) {

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

let diagramCounter = 0;

function createDiagram(title, labels, datasets) {
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

function createDataset(label, data, color="#c84646") {
    let dataset = {
        label: label,
        data: data,
        borderWidth: 1,
        fill: false,
        borderColor: color,
    };

    return dataset;
}

function displayValues(values) {

    let labels = [];

    let data = {
        'temperature': {},
        'light': {},
        'humidity': {},
        'motion': {},
        'co2': {}
    };

    let last;

    for (let i = 0; i < values.length; i++) {
        let erhalten = values[i]["erhalten"];
        let date = new Date(erhalten * 1000);

        let label = date.toLocaleDateString('de-CH');
        if (label !== last) {
            last = label;
            labels.push(label);
        }

        let werte = JSON.parse(values[i]['dekodiertJSON']);

        for (let key in data) {
            if (key in werte) {
                if (!(label in data[key])) data[key][label] = [];
                data[key][label].push(werte[key]);
            }
        }
    }

    let container = $("#diagram-container");
    container.html("");

    let diagramsVisualized = 0;

    for (let key in data) {

        let min = [];
        let max = [];
        let avg = [];

        for (let _ in data[key]) {
            let res = findMinMaxAvg(data[key][_]);
            min.push(res[0]);
            max.push(res[1]);
            avg.push(res[2]);
        }

        if(min.length !== 0) {

            diagramsVisualized += 1;

            let datasets = [
                createDataset('Min', min),
                createDataset('Max', max, "#802E9E"),
                createDataset('Avg', avg, "#C8FF46")
            ];

            createDiagram(key.toUpperCase(), labels, datasets);
        }
    }

    if(diagramsVisualized === 0) {
        container.html("<p class='text-primary'><b>Keine Daten gefunden.</b></p>");
    }

}

function loadValues(eui, min, max) {

    Client.get(endpoint + 'sensoren/' + eui + '/werte?min=' + min + '&max=' + max, function (response) {

        if (response.status === 200) {

            let result = JSON.parse(response.responseText);

            displayValues(result['list']);
        } else {
            // TODO fehlermeldig
        }

    })

}

function dateToInputValue(date) {
     return date.toISOString().slice(0,10);
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

            loadValues(eui, min, max)
        });

        filter.click(function () {

            let h24 = 60* 60 * 24;
            let min = (new Date(inpFrom.val())).valueOf() / 1000 - h24;
            let max = ((new Date(inpTo.val())).valueOf() / 1000) + h24;

            loadValues(eui, min, max)
        });

    }



});