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

    var headers = ["Title", "Artist(s)"]
    tbl.setAttribute("id", "table")
    var row = tbl.insertRow(0);
    for (var i = 0; i < headers.length; i++) {
        var headerCell = document.createElement("TH");
        headerCell.innerHTML = headers[i];
        row.appendChild(headerCell);
    }


    var rows = 1;

    Object.keys(data).forEach(function (orig_key) {
        key = orig_key.replace(/[^0-9a-z]/gi, '').toLowerCase();
        if (key.includes(searchTerm)) {
            console.log(key);
            var tr = tbl.insertRow(rows);
            var td0 = tr.insertCell(0);
            var td1 = tr.insertCell(1);

            var newText = document.createTextNode(orig_key);
            td0.appendChild(newText);

            var newText = document.createTextNode(data[orig_key].join(", "));
            td1.appendChild(newText);
            rows++;
        }
    })

    if (rows > 1) {
        body.appendChild(tbl);
    }



}