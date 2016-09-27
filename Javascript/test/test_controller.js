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
                $("#token").val(result.token);
                $("#hash").val(result.hash);
            }
        );
    }
};

var onCheckTokenButtonClicked = function() {
    var token = $("#token").val();
    var hash = $("#hash").val()
    console.log("Using token",token);
    var api = OctronicUserApi(URL);
    api.makeRequest('GET','/user/test_resource',hash, token,
        function(response) {
            console.log("Got response from tokenised request",response);
        }
    );
};

