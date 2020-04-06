function toggleForm() {
    /*
        Wechselt die Ansicht zwischen Loading und Form.
     */
    $("#form").toggle(0);
    $("#spinner").toggle(0);
}

function signIn() {
    /*
        Prüft zuerst den Inhalt vom Benutzernamen und Passwort,
        danach schickt es eine Anfrage auf /login
        und setzt entsprechend die Access und Refresh Tokens.
     */

    let benutzername = $("#benutzername");
    let passwort = $("#passwort");

    let benutzerNameValid = check(benutzername, 3, 100);
    let passwortValid = check(passwort, 8, 100);

    let success = $("#success-alert");
    let error = $("#error-alert");

    if (benutzerNameValid && passwortValid) {
        success.fadeOut(0);
        error.fadeOut(0);
        toggleForm();

        $.ajax(
            endpoint + 'login', {
                method: 'POST',
                data: JSON.stringify({
                    'username': benutzername.val(),
                    'password': passwort.val()
                }),
                complete: function(response) {
                    toggleForm();
                    if(response.status === 200) {
                        success.fadeIn(0);
                        let responseText = JSON.parse(response.responseText);
                        Auth.saveTokens(responseText["token"], responseText["refresh_token"]);
                        if(Auth.getRole() === 'ADMIN') {
                            window.location.replace(adminDashboard);
                        } else {
                            window.location.replace(personalDashboard);
                        }
                    } else {
                        error.fadeIn(0);
                    }
                }
            }
        );
    }
}


$(document).ready(function () {
    $("#login-btn").click(signIn);
});