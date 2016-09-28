/*
    octronic.webapis.user.js

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

    this.makeRequest = function(method,url,user,hash,signature,callback) {
        $.ajax({
            method : method,
            url    : domain+url,
            beforeSend: function (xhr) {
                    xhr.setRequestHeader ("Authorization", "Basic " + btoa(hash+ ":"+signature));
                    xhr.setRequestHeader ("From", user);
            },
        }).done(callback);
    };

    return this;
};
