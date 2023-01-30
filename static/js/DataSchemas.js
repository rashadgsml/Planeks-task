window.onload = function () {
    reloadList()
};

function reloadList() {
    $.ajax({
        method: "GET",
        url: schema_list_url,
        dataType: "json",
        success: function (data) {
            schema_tbody = document.getElementById("schema-tbody");
            schema_tbody.innerHTML = ""

            try {
                $("#table").find("tr:gt(1)").remove();
            } catch { }

            trs = "";
            data.forEach((data, counter) => {
                trs += `
                <tr>
                    <td><b>${counter + 1}<b></td>
                    <td>${data.title}</td>
                    <td>${data.modified_at}</td>
                    <td>
                        <a href="${schema_detail_url.replace('0', data.id)}" class="edit" title="Edit" data-toggle="tooltip"><i
                                class="material-icons">&#xE254;</i></a>
                        <a onclick="deleteSchema(this, '${data.id}')" class="delete" title="Delete" data-toggle="tooltip"><i
                                class="material-icons">&#xE872;</i></a>
                    </td>
                </tr>`;
            });
            schema_tbody.insertAdjacentHTML("beforeend", trs);
        },
    });
}


function deleteSchema(event, obj_id) {
    $(event).parents("tr").remove()
    $.ajax({
        method: "DELETE",
        headers: {'X-CSRFToken': csrftoken},
        url: schema_detail_api_url.replace("0", obj_id),
        dataType: "json",
    });
}

