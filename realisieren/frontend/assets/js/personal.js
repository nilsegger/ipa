function appendPersonal(uuid, benutzername, name, rolle, row) {

    let columns = '<td>' + benutzername + '</td><td>' + name + '</td></td><td>' + rolle + '</td><td><button id="personal-' + uuid + '-view" class="btn btn-info">Ansehen</button><button id="personal-' + uuid + '-delete" class="btn btn-danger">Löschen</button></td>';

    if(row === undefined) {
        $("#personal-table").append('<tr id="personal-' + uuid + '-row">' + columns + '</tr>');
    } else {
        row.html(columns);
    }

    $("#personal-" + uuid + "-view").click(function () {
        selected = uuid;
        $("#personal-form").modal("show");
        $("#benutzername").val(benutzername);
        $("#name").val(name);
        $("#rolle").val(rolle);
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

    let benutzernameValid = check(benutzername, 3, 100, skipEmptyValidation);
    let passwortValid = check(passwort, 8, 100, skipEmptyValidation);
    let nameValid = check(name, 3, 100, skipEmptyValidation);
    let rolleValid = check(rolle, skipEmptyValidation);

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

let offset = 0;
let endOfData = false;

function loadPersonal() {

    Client.get(endpoint + 'personal?offset=' + offset, function (response) {

        if (response.status === 200) {

            let result = JSON.parse(response.responseText);

            offset = result['offset'];
            endOfData = result['is_end'];
            let list = result['list'];

            for (let i = 0; i < list.length; i++) {
                let item = list[i];
                let uuid = item['uuid'];
                let benutzername = item['benutzername'];
                let name = item['name'];
                let rolle = item['rolle'];

                appendPersonal(uuid, benutzername, name, rolle);

            }

        } else {
            // TODO Fehlermeldig.
        }

    })

}

let selected;

$(document).ready(function () {

    $("#create-personal-btn").click(function () {
        selected = undefined;
    });

    $("#personal-save-btn").click(function () {
        if (selected === undefined) {
            savePersonal(Client.post, endpoint + 'personal');
        } else {
            savePersonal(Client.put, endpoint + 'personal/' + selected, selected, $("#personal-"+selected+"-row"));
        }
    });

    loadPersonal();
});