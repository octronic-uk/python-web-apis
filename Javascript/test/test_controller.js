/*
    test_controller.js

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

var URL="http://localhost:5000";

var onCreateUserButtonClicked = function() {
    var username = $("#create-username").val();
    var password = $("#create-password").val();

    if (username == "" || password == "") {
        console.log("Create User - Username/Password must not be empty");
    }
    else {
        console.log("Create User - Username:",username,"Password:",password);
        var api = OctronicUserApi(URL);
        api.createUser(username, password,
            function(result) {
                console.log(result); 
            }
        );
    }
};

var onGetTokenButtonClicked = function() {
    var username = $("#login-username").val();
    var password = $("#login-password").val();

    if (username == "" || password == "") {
        console.log("Get Token - Username/Password must not be empty");
    } else {
        console.log("Get Token - Username:",username,"Password:",password);
        var api = OctronicUserApi(URL);
        api.get_token(username, password,
            function(result) {
                console.log("Get token result",result);
                $("#check-token-button").prop('disabled',false);
                $("#user").val(result.user);
                $("#hash").val(result.hash);
                $("#sig").val(result.signature);
            }
        );
    }
};

var onCheckAuthButtonClicked = function() {
    console.log("Checking Authorisation...");
    var user = $("#user").val();
    var hash = $("#hash").val();
    var sig  = $("#sig").val();
    var api = OctronicUserApi(URL);
    api.makeRequest('GET','/user/test_resource',user, hash, sig,
        function(response) {
            console.log("Got response from authorised request",response);
        }
    );
};

