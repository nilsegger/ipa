function setStockwerkRow(id, name, niveau, gebaeudeId, gebaeudeName, row) {

    let rowId = "stockwerk-" + id + "-row";
    let viewId = "stockwerk-" + id + "-view";
    let deleteId = "stockwerk-" + id + "-delete";
    let tableId = "#stockwerk-table";

    let columns = '<td>' + name + '</td><td>' + niveau + '</td><td>' + gebaeudeName + '</td><td><button class="btn-info btn" id="' + viewId + '">Editieren</button><button id="' + deleteId + '" class="btn-danger btn">Löschen</button></td>';
    let table = $(tableId);

    if (row === undefined) {
        table.append('<tr id="' + rowId + '">' + columns + '</tr>');
    } else {
        row.html(columns);
    }

    $("#" + viewId).click(
        function () {
            selectedStockwerk = id;
            reset($("#stockwerk-name"), name);
            reset($("#stockwerk-niveau"), niveau);
            reset($("#stockwerk-gebaeude"), gebaeudeId);
            $("#stockwerke-form").modal('show');
        }
    );

    $("#" + deleteId).click(
        function () {
            Client.delete(endpoint + 'stockwerke/' + id, function (response) {
                if (response.status === 200) {
                    $("#" + rowId).remove();
                } else {
                    // TODO fehlermeldig
                }
            })

        }
    );

}


function stockwerkForm(method, url, id, row) {

    let name = $("#stockwerk-name");
    let niveau = $("#stockwerk-niveau");
    let gebaeudeID = $("#stockwerk-gebaeude");

    console.log(gebaeudeID.val());

    let nameValid = check(name, 3, 100);
    let niveauValid = check(niveau);
    let gebaeudeIDValid = check(gebaeudeID);

    if (nameValid && niveauValid && gebaeudeIDValid) {
        let nameVal = name.val();
        let niveauVal = niveau.val();
        let gebaeudeIdVal = gebaeudeID.val();

        let request = {
            'name': nameVal,
            'niveau': Number(niveauVal),
            'gebaeude': {
                'id': Number(gebaeudeIdVal)
            }
        };

        method(url, JSON.stringify(request), function (response) {

            if (response.status === 200) {

                if (id === undefined) {
                    id = JSON.parse(response.responseText)["id"];
                }

                setStockwerkRow(id, nameVal, niveauVal, gebaeudeIdVal, $("#stockwerk-gebaeude option:selected").text(), row);

                $("#stockwerke-form").modal("hide");

            } else {
                // TODO fehlermeldig
            }

        });

    }

}

let selectedStockwerk;

$(document).ready(function () {

    populateTable('stockwerke', loadStockwerke, $("#stockwerke-loader"), $("#stockwerke-empty"), undefined, function (item) {
        setStockwerkRow(item["id"], item["name"], item["niveau"], item["gebaeude"]["id"], item["gebaeude"]["name"]);
    });

    loadGebaeude(function (list) {
        for (let i = 0; i < list.length; i++) {
            let item = list[i];
            $("#stockwerk-gebaeude").append('<option value="' + item["id"] + '">' + item["name"] + '</option>');
        }
    });

    $("#create-stockwerk-btn").click(function () {
        selectedStockwerk = undefined;
        reset($("#stockwerk-name"));
        reset($("#stockwerk-niveau"));
        reset($("#stockwerk-gebaeude"));
    });

    $("#stockwerk-save-btn").click(function () {

        if (selectedStockwerk === undefined) {
            stockwerkForm(Client.post, endpoint + 'stockwerke');
        } else {
            stockwerkForm(Client.put, endpoint + 'stockwerke/' + selectedStockwerk, selectedStockwerk, $("#stockwerk-" + selectedStockwerk + "-row"));
        }

    });
});