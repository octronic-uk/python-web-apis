var OctronicUserApi = function(domain) {

    this.domain = domain;
    this.token = null;
    this.token_b64 = null;

    this.createUser = function(username,password,callback) {
        $.ajax({
            method: "POST",
            url: domain+"/user/create",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                username : username,
                password : password
            })
        }).done(callback);
    };

    this.get_token = function(username,password,callback) {
        $.ajax({
            method  : "GET",
            url     : domain+"/user/token",
            beforeSend: function (xhr) {
                    xhr.setRequestHeader ("Authorization", "Basic " + btoa(username + ":" + password));
            },
        }).done(function(result) {
            this.token = result;
            callback(this.token);
        });
    };

    this.makeRequest = function(url,method,token,callback) {
        if (this.token_b64 != null) {
            $.ajax({
                method : method,
                url    : domain+url,
                header : {
                  'Authorization': 'Basic ' + this.token_b64,
                }
            }).done(callback);
        } else {
            callback(null);
        }
    };

    return this;
};
