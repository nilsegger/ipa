function loadList(url, callback) {
    Client.get(url, function (response) {
        if (response.status === 200) {
            let result = JSON.parse(response.responseText);
            let list = result['list'];
            callback(list, result['is_end'], result['offset']);
        } else {
            // TODO Fehlermeldig
        }
    })
}

function loadGebaeude(callback, offset = 0) {
    loadList(endpoint + 'gebaeude?offset=' + offset.toString(), callback);
}

function loadStockwerke(callback, offset = 0) {
    loadList(endpoint + 'stockwerke?offset=' + offset.toString(), callback);
}

function loadRaeume(callback, offset = 0) {
    loadList(endpoint + 'raeume?offset=' + offset.toString(), callback)
}

function loadMeldungen(callback, offset = 0) {
    loadList(endpoint + 'meldungen?type=unbearbeitet&offset=' + offset.toString(), callback);
}

function loadPersonal(callback, offset = 0) {
    loadList(endpoint + 'personal?offset=' + offset.toString(), callback);
}

function loadSensoren(callback, offset = 0) {
    loadList(endpoint + 'sensoren?offset=' + offset.toString(), callback);
}

function loadMaterial(callback, offset = 0) {
    loadList(endpoint + 'materialien?offset=' + offset.toString(), callback);
}

function loadBeobachter(callback, offset = 0) {
    loadList(endpoint + 'beobachter?offset=' + offset.toString(), callback);
}

function loadMaterialZuBeobachter(beobachterID, callback, offset = 0) {
    loadList(endpoint + 'beobachter/' + beobachterID + '/materialien?offset=' + offset.toString(), callback);
}

function loadSensorWerte(eui, min, max, callback) {
    loadList(endpoint + 'sensoren/' + eui + '/werte?min=' + min + '&max=' + max, callback);
}

function loadSensorBeobachter(eui, callback) {
    loadList(endpoint + 'sensoren/' + eui + '/beobachter', callback);
}

let tableStatus = {};

function populateTable(name, listLoader, spinnerElem, emptyElem, loadMoreBtnElem, rowBuilder) {
    spinnerElem.show();
    emptyElem.hide();
    if (loadMoreBtnElem !== undefined) {
        loadMoreBtnElem.hide();
    }
    let offset = name in tableStatus ? tableStatus[name] : 0;

    listLoader(function (list, endOfData, offset) {
        tableStatus[name] = offset;
        if (!endOfData) {
            if (loadMoreBtnElem !== undefined) {
                loadMoreBtnElem.show();
            }
        }
        spinnerElem.hide();
        if (list.length === 0) {
            emptyElem.show();
        } else {
            for (let i = 0; i < list.length; i++) {
                rowBuilder(list[i]);
            }
        }
    }, offset);
}