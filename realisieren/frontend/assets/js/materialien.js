function setMaterialRow(id, name, row) {

    let rowId = "material-"+id+"-row";
    let viewId = "material-"+id+"-view";
    let deleteId = "material-"+id+"-delete";
    let tableId = "#materialien-table";

    let columns = '<td>'+name+'</td><td><button class="btn-info btn" id="'+viewId+'">Editieren</button><button id="'+deleteId+'" class="btn-danger btn">Löschen</button></td>';
    let table = $(tableId);

    if(row === undefined) {
        table.append('<tr id="'+rowId+'">'+columns+'</tr>');
    } else {
        row.html(columns);
    }

    $("#" + viewId).click(
        function () {
            selectedMaterial = id;
            reset($("#material-name"), name);
            $("#material-form").modal('show');
        }
    );

    $("#" + deleteId).click(
        function () {
            Client.delete(endpoint + 'materialien/' + id, function (response) {
                if(response.status === 200) {
                    $("#" + rowId).remove();
                } else {
                    // TODO fehlermeldig
                }
            })

        }
    );

}


function materialForm(method, url, id, row) {

    let name = $("#material-name");

    let nameValid = check(name, 3, 100);

    if(nameValid) {
        let nameVal = name.val();

        let request = {
            'name': nameVal
        };

        method(url, JSON.stringify(request), function(response) {

            if(response.status === 200) {

                if(id === undefined) {
                    id = JSON.parse(response.responseText)["id"];
                }

                setMaterialRow(id, nameVal, row);

                 $("#material-form").modal("hide");

            } else {
                // TODO fehlermeldig
            }

        });

    }

}

let selectedMaterial;

$(document).ready(function() {

    populateTable('materialien', loadMaterial, $("#materialien-loader"), $("#materialien-empty"), undefined, function (item) {
        setMaterialRow(item["id"], item["name"]);
    });

    $("#create-material-btn").click(function () {
        selectedMaterial = undefined;
        reset($("#material-name"));
    });

    $("#material-save-btn").click(function() {

        if(selectedMaterial === undefined) {
            materialForm(Client.post, endpoint + 'materialien');
        } else {
            materialForm(Client.put, endpoint + 'materialien/' + selectedMaterial, selectedMaterial, $("#material-"+ selectedMaterial +"-row"));
        }

    });
});