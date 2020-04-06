const endpoint = "http://localhost:8000/";
const self = "http://localhost:4000/";
const login = self;
const adminDashboard = self + "dashboard.html";
const personalDashboard = self + "dashboard_personal.html";

class Auth {

    static saveTokens(access, refresh) {
        sessionStorage.setItem('accessToken', access);
        if(refresh != null) {
            sessionStorage.setItem('refreshToken', refresh);
        }
    }

    static retrieveAccessToken() {
        return sessionStorage.getItem('accessToken');
    }

    static retrieveRefreshToken() {
        return sessionStorage.getItem('refreshToken');
    }

    static retrieveNewAccessToken(callback) {

        $.ajax(endpoint + 'login', {
            method: 'PUT',
            data: Auth.retrieveAccessToken(),
            complete: function (response) {
                if(response.code === 200) {
                    let responseText = JSON.parse(response.responseText);
                    Auth.saveTokens(responseText["token"]);
                } else {
                    Auth.logout();
                }
            }
        })

    }

    static getRole() {
        let token = Auth.retrieveAccessToken();
        let payload = atob(token.split('.')[1]);
        return JSON.parse(payload)['role'];
    }

    static logout() {
        sessionStorage.removeItem('accessToken');
        sessionStorage.removeItem('refreshToken');
        window.location.replace(login);
    }

}


class Client {

    static _request(url, method, callback, data, isNested= false) {
        /*
            Verpackt in die Anfrage den Authorization Header.
            Wenn die Anfrage mit einem 401 Status Antwortet, so wird ein neuer
            Access Token angefragt und dieselbe Anfrage nochmals gestartet.
         */
        return $.ajax(url, {
            method: method,
            headers: {
                'Authorization': 'Bearer ' + Auth.retrieveAccessToken()
            },
            data: data,
            complete: function (response) {
                if(response.status === 401 && !isNested) {
                    Auth.retrieveNewAccessToken(function () {
                        Client._request(url, method, callback, data,true);
                    })
                } else if(response.status === 401 && isNested) {
                    Auth.logout();
                }
                callback(response);
            }
        });
    }

    static get(url, callback) {
        Client._request(url, 'GET', callback);
    }

    static post(url, data, callback) {
        Client._request(url, 'POST', callback, data);
    }

    static put(url, data, callback) {
        Client._request(url, 'PUT', callback, data);
    }

    static delete(url, callback) {
        Client._request(url, 'DELETE', callback);
    }
}


function check(elem, min_len, max_len, skipEmpty=false) {
    /*
        Prüft ob der Wert eines Input Elements nicht null ist
        und er mindest und maximal Länge entspricht.
     */

    let value = elem.val();

    if(!value && skipEmpty) return true;

    let minValid = min_len == null ? true : value.length >= min_len;
    let maxValid = max_len == null ? true : value.length <= max_len;

    if (value == null || !value || !minValid || !maxValid) {
        elem.addClass('is-invalid');
        return false;
    } else {
        elem.removeClass('is-invalid');
        return true;
    }

}

function reset(elem, val) {
    /*
       Entfernt die Klasse is-invalid und setzt den Wert eines Input Feldes auf den val Parameter,
       ist dieser undefined, so wird das Feld leer.
     */
    elem.val(val === undefined ? "" : val);
    elem.removeClass('is-invalid');
}

$(document).ready(function () {
    /*
        Wird die Login Seite geöffnet wenn man berits eingeloggt ist,
        wird man auf die Dashboard Seite weitergeleitet.
        Ist man jedoch nicht eingeloggt und ist auf einer nicht Login Seite,
        so wird man auf die Login Seite weitergeleitet.
     */

    let signedIn = Auth.retrieveRefreshToken() != null;
    if (signedIn && window.location.href === login) {
        if(Auth.getRole() === 'ADMIN') {
            window.location.replace(adminDashboard);
        } else {
            window.location.replace(personalDashboard);
        }
    } else if (!signedIn && window.location.href !== login) {
        Auth.logout();
    } else if(signedIn && Auth.getRole() === 'PERSONAL' && window.location.href !== personalDashboard) {
        window.location.replace(personalDashboard);
    }

    $("#logout-btn").click(function () {
        Auth.logout();
    })
});