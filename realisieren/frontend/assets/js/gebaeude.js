function setGebaeudeRow(id, name, row) {

    let columns = '<td>'+name+'</td><td><button class="btn-info btn" id="gebaeude-'+id+'-view">Editieren</button><button id="gebaeude-'+id+'-delete" class="btn-danger btn">Löschen</button></td>';
    let table = $("#gebaeude-table");
    if(row === undefined) {
        table.append('<tr id="gebaeude-'+id+'-row">'+columns+'</tr>')
    } else {
        row.html(columns);
    }

    $("#gebaeude-" + id + "-view").click(
        function () {
            selectedGebaeude = id;
            reset($("#gebaeude-name"), name);
            $("#gebaeude-form").modal('show');
        }
    );

    $("#gebaeude-" + id + "-delete").click(
        function () {
            Client.delete(endpoint + 'gebaeude/' + id, function (response) {
                if(response.status === 200) {
                    $("#gebaeude-"+id+"-row").remove();
                } else {
                    // TODO fehlermeldig
                }
            })

        }
    );

}

function gebaeudeForm(method, url, id, row) {

    let name = $("#gebaeude-name");

    if(check(name, 3, 100)) {
        let nameVal = name.val();
        method(url, JSON.stringify({'name': nameVal}), function(response) {

            if(response.status === 200) {

                if(id === undefined) {
                    id = JSON.parse(response.responseText)["id"];
                }

                setGebaeudeRow(id, nameVal, row);

                 $("#gebaeude-form").modal("hide");

            } else {
                // TODO fehlermeldig
            }

        });

    }

}

let selectedGebaeude;

$(document).ready(function() {

    populateTable('gebaeude', loadGebaeude, $("#gebaeude-loader"), $("#gebaeude-empty"), undefined, function (item) {
        setGebaeudeRow(item["id"], item["name"]);
    });

    $("#create-gebaeude-btn").click(function () {
        selectedGebaeude = undefined;
        $("#gebaeude-name").val("");
    });

    $("#gebaeude-save-btn").click(function() {

        if(selectedGebaeude === undefined) {
            gebaeudeForm(Client.post, endpoint + 'gebaeude');
        } else {
            gebaeudeForm(Client.put, endpoint + 'gebaeude/' + selectedGebaeude, selectedGebaeude, $("#gebaeude-"+ selectedGebaeude +"-row"));
        }

    });
});