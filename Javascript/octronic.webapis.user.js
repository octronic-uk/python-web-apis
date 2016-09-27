var OctronicUserApi = function(domain) {

    this.domain = domain;

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
        }).done(callback)
    };

    this.makeRequest = function(method,url,hash,signature,callback) {
        $.ajax({
            method : method,
            url    : domain+url,
            beforeSend: function (xhr) {
                    xhr.setRequestHeader ("Authorization", "Basic " + btoa(hash+ ":"+signature));
            },
        }).done(callback);
    };

    return this;
};
