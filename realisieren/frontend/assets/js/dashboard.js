
// TODO fetch Meldungen

function addRow(datum, beschreibung, sensorDevEUI, sensorName, raumID, raumName, stockwerk, gebaeude) {
    let table = $("#meldungen_table");

    let row = `<tr>
            <td>${datum}</td>
            <td>${beschreibung} </td>
            <td>${sensorName}</td>
            <td><span class="card-title">${raumName} <small
                    class="text-muted">${stockwerk} ${gebaeude}</small></span>
            </td>
            <td>
                <div class="btn-group" role="group" aria-label="Basic example">
                  <button type="button" class="btn btn-success">Gelöst</button>
                  <button type="button" class="btn btn-danger">Löschen</button>
                </div>
            </td>
        </tr>`;

    table.append(row);
}

// TODO Art darstelle und Melder
// TODO Login Refresh teste

$(document).ready(function () {

    Client.get(endpoint + 'meldungen', function(response) {

        if(response.status === 200) {
            let result = JSON.parse(response.responseText);
            for(let i  = 0; i < result['list'].length; i++) {
                let item = result['list'][i];
                console.log(item);
                let datum = new Date(item["datum"] * 1000);
                addRow(datum.toLocaleString(), item["beschreibung"], item["sensor"]["dev_eui"], item["sensor"]["name"], item["raum"]["id"], );
            }
        }

        console.log(response.responseText);
    });

});