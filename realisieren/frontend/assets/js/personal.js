function appendPersonal(uuid, benutzername, name, rolle, row) {

    let columns = '<td>' + benutzername + '</td><td>' + name + '</td></td><td>' + rolle + '</td><td><button id="personal-' + uuid + '-view" class="btn btn-info">Ansehen</button><button id="personal-' + uuid + '-delete" class="btn btn-danger">Löschen</button></td>';

    if(row === undefined) {
        $("#personal-table").append('<tr id="personal-' + uuid + '-row">' + columns + '</tr>');
    } else {
        row.html(columns);
    }

    $("#personal-" + uuid + "-view").click(function () {
        selectedPersonal = uuid;
        reset($("#benutzername"), benutzername);
        reset($("#name"), name);
        reset($("#rolle"), rolle);
        reset($("#passwort"));
        $("#personal-form").modal("show");
    });

    $("#personal-" + uuid + "-delete").click(function () {
        deletePersonal(uuid);
    });
}

function deletePersonal(uuid) {
    Client.delete(endpoint + 'personal/' + uuid, function (response) {
        if(response.status === 200) {
            $("#personal-" + uuid + "-row").remove();
        } else {
            // TODO fehlermeldig
        }
    });
}

function savePersonal(method, url, uuid, row) {

    let benutzername = $("#benutzername");
    let passwort = $("#passwort");
    let name = $("#name");
    let rolle = $("#rolle");

    let skipEmptyValidation = uuid!==undefined;

    let benutzernameValid = check(benutzername, 3, 100);
    let passwortValid = check(passwort, 8, 100, skipEmptyValidation);
    let nameValid = check(name, 3, 100);
    let rolleValid = check(rolle);

    if (benutzernameValid && passwortValid && nameValid && rolleValid) {

        let request = {
            'name': name.val(),
            'benutzername': benutzername.val(),
            'passwort': passwort.val(),
            'rolle': rolle.val(),
        };

        let benutzernameAlert = $("#benutzername-warning");

        benutzernameAlert.hide();

        method(url, JSON.stringify(request), function (response) {

            if (response.status === 200) {

                $("#personal-form").modal('hide');

                if(uuid === undefined) {
                    let result = JSON.parse(response.responseText);
                    uuid = result['uuid'];
                }

                appendPersonal(uuid, benutzername.val(), name.val(), rolle.val(), row);

            } else if (response.status === 422) {
                benutzernameAlert.show();
            } else {
                // Fehlermeldig.
            }


        });

    }

}

let selectedPersonal;

$(document).ready(function () {

    populateTable('personal', loadPersonal, $("#personal-loader"), $("#personal-empty"), undefined, function (item) {
        appendPersonal(item['uuid'], item['benutzername'], item['name'], item['rolle']);
    });

    $("#create-personal-btn").click(function () {
        selectedPersonal = undefined;
        reset($("#benutzername"));
        reset($("#passwort"));
        reset($("#name"));
        reset($("#rolle"));
    });

    $("#personal-save-btn").click(function () {
        if (selectedPersonal === undefined) {
            savePersonal(Client.post, endpoint + 'personal');
        } else {
            savePersonal(Client.put, endpoint + 'personal/' + selected, selected, $("#personal-"+selected+"-row"));
        }
    });

});