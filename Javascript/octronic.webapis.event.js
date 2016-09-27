var OctronicEventApi = function(domain) {

    this.domain = domain;

    this.insertEvent = function(event,callback) {
        $.ajax({
            method: "POST",
            url: domain+"/event",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(event)
        }).done(callback);
    };

    return this;
};
