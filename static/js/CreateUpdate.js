window.onload = function () {
    if (obj_id) {
        // It means it is edit view
        document.title = "Edit schema"
        $("#page-title").text("Edit schema")
        $("#submit-btn").text("Update")
        fillForm()
    }
};


function fillForm() {
    $.ajax({
        method: "GET",
        url: schema_detail_api_url.replace("0", obj_id),
        dataType: "json",
        success: function (data) {
            $("#title").val(data.title)
            $("#column_sep").val(data.column_sep)
            $("#string_char").val(data.string_char)
            $("#columns").html("")
            data.columns.forEach((data, counter) => {
                $(".add-column").click()
                document.getElementsByName("c_name")[counter].value = data.name
                document.getElementsByName("type")[counter].value = data.column_type
                if (data.column_type == "Integer") {
                    from = document.getElementsByName("from")
                    to = document.getElementsByName("to")
                    from[counter].value = data.int_from
                    to[counter].value = data.int_to
                    $(from[counter]).parents(".form-group")[0].querySelector('.integer').style.display = "block"
                    $(to[counter]).parents(".form-group")[0].querySelector('.integer').style.display = "block"
                }
                document.getElementsByName("order")[counter].value = data.order

            });
        },
    });
}


$(".add-column").click(function () {
    var column = `
    <div class="column">
                <div class="form-group">
                    <div class="col-md-4">
                        <label>Column name</label>
                        <input type="text" class="form-control" name="c_name">
                    </div>
                </div>
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Type</label>
                        <select class="form-control form-control-lg type" name="type">
                            <option value="Full name">Full name</option>
                            <option value="Job">Job</option>
                            <option value="Email">Email</option>
                            <option value="Domain name">Domain name</option>
                            <option value="Phone number">Phone number</option>
                            <option value="Text">Text</option>
                            <option value="Integer">Integer</option>
                            <option value="Address">Address</option>
                            <option value="Date">Date</option>
                        </select>
                    </div>
                </div>
                <div class="form-group">
                    <div class="col-md-1">
                        <div class="integer" style="display: none;"><label>From</label>
                            <input type="number" class="form-control" name="from">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="col-md-1">
                        <div class="integer" style="display: none;"><label>To</label>
                            <input type="number" class="form-control" name="to">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="col-md-2">
                        <label>Order</label>
                        <input type="number" class="form-control" name="order">
                    </div>
                </div>
                <div class="form-group">
                    <div class="col-md-2">
                        <br>
                        <td><a style="cursor: pointer;" class="text-danger delete">Delete</a></td>
                    </div>
                </div>
            </div>
    `;
    $("#columns").append(column);
    $('[data-toggle="tooltip"]').tooltip();
});


$(document).on("click", ".delete", function () {
    $(this).parents("div.column").remove();
    $(".add-new").removeAttr("disabled");
});


$(document).on("change", ".type", function () {
    integer_fields = $(this).parents('div.column').children("div.form-group")
    $(this).parents('div.column .integer').css('display', 'block')
    if ($(this).val() == "Integer") {
        integer_fields[2].querySelector('.integer').style.display = "block"
        integer_fields[3].querySelector('.integer').style.display = "block"
    }
    else {
        integer_fields[2].querySelector('.integer').style.display = "none"
        integer_fields[3].querySelector('.integer').style.display = "none"
    }
});


$("#schema-form").on("submit", function (event) {
    event.preventDefault();
    check_validation = checkValidation()
    if (!check_validation.valid){
        return showErrorMessage(check_validation.message)
    }
    data = collectData();

    var myHeaders = new Headers()
    myHeaders.append('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value)
    var formData = new FormData()

    method = "POST"
    request_url = schema_create_url
    if (obj_id) {
        method = "PUT"
        request_url = schema_detail_api_url.replace("0", obj_id)
    }

    var requestOptions = {
        method: method,
        headers: myHeaders,
        body: formData,
        redirect: 'follow',
    };

    formData.append('title', $("#title").val())
    formData.append('column_sep', $("#column_sep").val())
    formData.append('string_char', $("#string_char").val())

    formData.append('columns', JSON.stringify(data.columns));

    response = fetch(request_url, requestOptions)
        .then(function (response) {
            response.json().then(data => {
            })
            if (response.ok) {
                window.location.replace(schema_list_view);
            }
        })
});


function checkValidation() {
    valid = true
    message = "Fill all required fields to submit"
    if (!$("#title").val()) {
        valid = false
        setError($("#title"))
    }
    names = document.getElementsByName("c_name")
    types = document.getElementsByName("type")
    froms = document.getElementsByName("from")
    tos = document.getElementsByName("to")
    for (let i = 0; i < names.length; i++) {
        if(!names[i].value){
            valid = false
            setError($(names[i]))
        }
        if(types[i].value == "Integer"){
            if(!froms[i].value){
                valid = false
                setError($(froms[i]))
            }
            if(!tos[i].value){
                valid = false
                setError($(tos[i]))
            }
            if((froms[i].value && tos[i].value) && (parseInt(froms[i].value)>parseInt(tos[i].value))){
                setError($(froms[i]))
                setError($(tos[i]))
                message = "'From' value must be smaller than 'To' value"
                valid = false
            }
        }
    }
    return {valid:valid, message:message}
}


function collectData() {
    column_array = []
    c_names = document.getElementsByName("c_name")
    types = document.getElementsByName("type")
    froms = document.getElementsByName("from")
    tos = document.getElementsByName("to")
    orders = document.getElementsByName("order")
    for (let i = 0; i < c_names.length; i++) {
        int_from = froms[i].value
        int_to = tos[i].value
        if (!froms[i].value) {
            int_from = null
        }
        if (!tos[i].value) {
            int_to = null
        }
        order = orders[i].value
        if(!orders[i].value){
            order = null
        }
        column_array.push(
            {
                name: c_names[i].value,
                column_type: types[i].value,
                order: order,
                int_from: int_from,
                int_to: int_to,
            }
        )
    }
    return {
        columns: column_array
    }
}
