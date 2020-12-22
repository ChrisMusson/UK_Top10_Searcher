var data;

function fetchJSONData() {
    return $(document).ready(function () {
        return $.getJSON("all_top_10_singles_artist.json", function (x) {
            data = x;
        }).fail(function () {
            console.log("An error has occurred.");
        });
    })
}

function tableCreate(data) {
    var searchTerm = document.getElementById("search").value;
    searchTerm = searchTerm.replace(/[^0-9a-z]/gi, '').toLowerCase();
    var body = document.body;

    try {
        var tbl = document.getElementById("table");
        tbl.remove();
        var tbl = document.createElement('table');
    } catch (err) {
        var tbl = document.createElement('table');
    }

    var headers = ["Title", "Artist(s)", "Peak", "Peak Date"]
    tbl.setAttribute("id", "table")
    var row = tbl.insertRow(0);
    for (var i = 0; i < headers.length; i++) {
        var headerCell = document.createElement("TH");
        headerCell.innerHTML = headers[i];
        row.appendChild(headerCell);
    }

    var rows = 1;

    for (i = 0; i < data.length; i++) {
        var title = data[i]["title"].replace(/[^0-9a-z]/gi, '').toLowerCase();
        if (title.includes(searchTerm)) {
            var tr = tbl.insertRow(rows);
            var td0 = tr.insertCell(0);
            var td1 = tr.insertCell(1);
            var td2 = tr.insertCell(2);
            var td3 = tr.insertCell(3);

            var newText = document.createTextNode(data[i]["title"]);
            td0.appendChild(newText);

            var newText = document.createTextNode(data[i]["artist"]);
            td1.appendChild(newText);

            var newText = document.createTextNode(data[i]["peak"]);
            td2.appendChild(newText);

            var newText = document.createTextNode(data[i]["date"]);
            td3.appendChild(newText);

            rows++;
        }
    }


    if (rows > 1) {
        body.appendChild(tbl);
    }
}