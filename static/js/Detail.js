window.onload = function () {
    uploadSchema()
    reloadDataset()
};


function uploadSchema() {
    $.ajax({
        method: "GET",
        url: schema_detail_url,
        dataType: "json",
        success: function (data) {
            schema_tbody = document.getElementById("schema-tbody");
            schema_tbody.innerHTML = ""

            try {
                $("#table").find("tr:gt(1)").remove();
            } catch { }

            trs = "";
            data.columns.forEach((data, counter) => {
                trs += `
                <tr>
                    <td><b>${counter + 1}<b></td>
                    <td>${data.name}</td>
                    <td>${data.column_type}</td>
                </tr>`;
            });
            schema_tbody.insertAdjacentHTML("beforeend", trs);
        },
    });
}


function reloadDataset() {
    $.ajax({
        method: "GET",
        url: dataset_list_url,
        data: {
            schema_id: obj_id
        },
        dataType: "json",
        success: function (data) {
            dataset_tbody = document.getElementById("dataset-tbody");
            dataset_tbody.innerHTML = ""

            try {
                $("#table").find("tr:gt(1)").remove();
            } catch { }

            trs = "";
            data.forEach((data, counter) => {
                trs += `
                <tr>
                    <td><b>${counter + 1}<b></td>
                    <td>${data.created_at}</td>
                    <td><button class="status-btn" disabled>Ready</button></td>
                    <td><a href="${data.file}">Download</a></td>
                </tr>`;
            });
            dataset_tbody.insertAdjacentHTML("beforeend", trs);
        },
    });
}


function generateCSV() {
    if(!$("#rows").val()){
        showErrorMessage(message="Enter number of rows before generating data")
        setError($("#rows"))
        return false
    }
    const currentdate = new Date();
    var datetime = currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear();
    dataset_tbody = document.getElementById("dataset-tbody");
    trs = `
        <tr>
            <td><b><b></td>
            <td>${datetime}</td>
            <td><button class="status-btn-pr" disabled>Processing</button></td>
            <td></td>
        </tr>`;
    dataset_tbody.insertAdjacentHTML("afterbegin", trs);
    $.ajax({
        method: "GET",
        url: generate_csv_url,
        data: {
            schema_id: obj_id,
            rows: $("#rows").val(),
        },
        dataType: "json",
        success: function (data) {
            reloadDataset()
        },
        error: function (data) {
            reloadDataset()
        },
    });
}
