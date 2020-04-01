const endpoint = "http://localhost:8000/";
const self = "http://localhost:4000/";
const login = self;
const dashboard = self + "dashboard";

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

    static logout() {
        sessionStorage.removeItem('accessToken');
        sessionStorage.removeItem('refreshToken');
        window.location.replace(login);
    }

}


class Client {

    static _request(url, method, callback, isNested= false) {
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
            complete: function (response) {
                if(response.status === 401 && !isNested) {
                    Auth.retrieveNewAccessToken(function () {
                        Client._request(url, method, callback, true);
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

    static post() {

    }

    static put() {

    }

    static delete() {

    }
}


function check(elem, min_len, max_len) {
    /*
        Prüft ob der Wert eines Input Elements nicht null ist
        und er mindest und maximal Länge entspricht.
     */

    let value = elem.val();

    let minValid = min_len == null ? true : value.length >= min_len;
    let maxValid = max_len == null ? true : value.length <= max_len;

    if (!value || !minValid || !maxValid) {
        elem.addClass('is-invalid');
        return false;
    } else {
        elem.removeClass('is-invalid');
        return true;
    }

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
        window.location.replace(dashboard);
    } else if (!signedIn && window.location.href !== login) {
        Auth.logout();
    }
});