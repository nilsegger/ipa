function setRaumRow(id, name, stockwerkId, stockwerkName, row) {

    let rowId = "raum-"+id+"-row";
    let viewId = "raum-"+id+"-view";
    let deleteId = "raum-"+id+"-delete";
    let tableId = "#raum-table";

    let columns = '<td>'+name+'</td><td>'+stockwerkName+'</td><td><button class="btn-info btn" id="'+viewId+'">Editieren</button><button id="'+deleteId+'" class="btn-danger btn">Löschen</button></td>';
    let table = $(tableId);

    if(row === undefined) {
        table.append('<tr id="'+rowId+'">'+columns+'</tr>');
    } else {
        row.html(columns);
    }

    $("#" + viewId).click(
        function () {
            selectedRaum = id;
            $("#raum-name").val(name);
            $("#raum-stockwerk").val(stockwerkId);

            $("#raum-form").modal('show');
        }
    );

    $("#" + deleteId).click(
        function () {
            Client.delete(endpoint + 'raeume/' + id, function (response) {
                if(response.status === 200) {
                    $("#" + rowId).remove();
                } else {
                    // TODO fehlermeldig
                }
            })

        }
    );

}


function raumForm(method, url, id, row) {

    let name = $("#raum-name");
    let stockwerId = $("#raum-stockwerk");

    let nameValid = check(name, 3, 100);
    let stockwerkValid = check(stockwerId);

    if(nameValid && stockwerkValid) {
        let nameVal = name.val();
        let stockwerkVal = stockwerId.val();

        let request = {
            'name': nameVal,
            'stockwerk': {
                'id': Number(stockwerkVal)
            }
        };

        method(url, JSON.stringify(request), function(response) {

            if(response.status === 200) {

                if(id === undefined) {
                    id = JSON.parse(response.responseText)["id"];
                }

                setRaumRow(id, nameVal, stockwerkVal, $("#raum-stockwerk").text(), row);

                 $("#raum-form").modal("hide");

            } else {
                // TODO fehlermeldig
            }

        });

    }

}


function loadRaeume() {

    Client.get(endpoint + 'raeume', function(response) {
        if(response.status === 200) {
            let list = JSON.parse(response.responseText)['list'];
            for(let i = 0; i < list.length; i++) {
                let item = list[i];
                setRaumRow(item["id"], item["name"], item["stockwerk"]["id"], item["stockwerk"]["name"] + " " + item["gebaeude"]["name"]);
            }
        } else {
            // TODO Fehlermeldig
        }

    })

}

let selectedRaum;

$(document).ready(function() {
    loadRaeume();

    $("#create-raum-btn").click(function () {
        selectedRaum = undefined;
        $("#raum-name").val("");
        $("#raum-stockwerk").val("");
    });

    $("#raum-save-btn").click(function() {

        if(selectedRaum === undefined) {
            raumForm(Client.post, endpoint + 'raeume');
        } else {
            raumForm(Client.put, endpoint + 'raeume/' + selectedRaum, selectedRaum, $("#raum-"+ selectedRaum +"-row"));
        }

    });
});