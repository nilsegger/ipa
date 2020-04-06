function addLink() {
    /*
        Fügt ein Material einem Beobachter hinzu. So wird dieses Material bei jeder Meldung des Beobachters vorgeschlagen.
     */

    let material = $("#material");
    let beobachter = $("#beobachter");
    let anzahl = $("#anzahl");

    let beobachterValid = check(beobachter);
    let materialValid = check(material);
    let anzahlValid = check(anzahl);

    if (beobachterValid && materialValid && anzahlValid) {

        let request = {
            'id': Number(material.val()),
            'anzahl': Number(anzahl.val())
        };

        Client.post(endpoint + 'beobachter/' + beobachter.val() + '/materialien/' + material.val(), JSON.stringify(request), function (response) {

            if (response.status === 200) {
                $("#beobachter-" + beobachter.val()).remove();
                let id = beobachter.val();
                let name = $("#beobachter option:selected").text();
                $("#beobachter-container").prepend(beobachterSection(id, name));
                loadBeobachterTable(id, name);
            } else {
                // TODO fehlermeldige
            }

        })

    }

}

function deleteLink(id) {

    /*
        Löscht die Verbindung eines Materiales zu Beobachters.
     */

    Client.delete(endpoint + 'beobachter/materialien/' + id, function (response) {
        if(response.status === 200) {
            $("#row-" + id).remove();
        } else {
            // TODO Fehlermeldig
        }
    })

}

function beobachterSection(id, name) {
    /*
        Erstellt eine Reihe aus der Tabelle.
     */
    return '<div class="mt-3" id="beobachter-' + id+ '"><h3>' + name + '</h3><div class="table-responsive"><table class="table table-striped"><thead><tr><th>Material</th><th>Anzahl</th><th>Löschen</th></tr></thead><tbody id="beobachter-' + id + '-table"></tbody><tfoot><tr id="beobachter-' + id + '-loader"><td colspan="3"><div class="spinner-border text-primary"></div></td></tr><tr id="beobachter-' + id + '-empty"><td colspan="3" class="text-primary">Keine Materialien.</td></tr></tfoot></table></div></div>';
}

function loadBeobachterTable(id, name) {

    /*
        Lädt die Daten für die Tabelle und aktiviert Onclick Listeners.
     */

    populateTable('beobachter-' + id, function (callback, offset) {
        loadMaterialZuBeobachter(id, callback, offset);
    }, $("#beobachter-" + id + "-loader"), $("#beobachter-" + id + "-empty"), undefined, function (item) {
        $("#beobachter-" + id + "-table").append("<tr id='row-"+item["id"]+"'><td>" + item["name"] + "</td><td>" + item["anzahl"] + "</td><td><button class='btn btn-danger' id='item-"+item["id"]+"'>Löschen</button></td></tr>");
        $("#item-"+item["id"]).click(function () {
            deleteLink(item["id"]);
        })
    });
}

$(document).ready(function () {

    $("#create-link").click(addLink);

    loadMaterial(function (list) {
        for (let i = 0; i < list.length; i++) {
            $("#material").append('<option value="' + list[i]["id"] + '">' + list[i]["name"] + '</option>');
        }
    });

    loadBeobachter(function (list) {
        for (let i = 0; i < list.length; i++) {
            $("#beobachter").append('<option value="' + list[i]["id"] + '">' +  list[i]["name"] + '</option>');
            $("#beobachter-container").append(beobachterSection(list[i]["id"],  list[i]["name"]));
            loadBeobachterTable(list[i]["id"], list[i]["name"]);
        }
    });

});