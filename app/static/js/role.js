
/* ========================== Add/Update Role ========================== */

const form = document.getElementById('roleForm')

form.addEventListener('submit', (e)=>{
    e.preventDefault()

    const formData = new FormData(form)
    const data = Object.fromEntries(formData)

    let id = document.getElementById('roleId').value

    if (id) {
        fetch(`/role/update?id=${id}`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data =>{
            if (data.status == "success") {
                alert(data.message)
                location.reload()
            }
            else{
                throw new Error(data.message);
            }
        })
        .catch(err =>{
            alert(err)
        })
    }else{
        fetch('/role/new', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data =>{
            if (data.status == "success") {
                alert(data.message)
                form.reset()
            }
            else{
                throw new Error(data.message);
            }
        })
        .catch(err =>{
            alert(err)
        })
    }
})


/* ========================== GET Role ========================== */


$(document).ready(function () {
    let table = $('#roleTable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/role/getAll",
            "type": "GET",
            "dataSrc": 'data',
            "error": function (xhr, error, thrown) {
                alert(xhr.responseText)
            }
        },
        "columns": [
            { "data": "name", "defaultContent": "N/A" },
            { "data": "addedTime", "defaultContent": "N/A" },
            { "data": "updatedTime", "defaultContent": "N/A" },
            { 
                "data": "id",
                "render": function(data, type, row) {
                    return `
                        <div class="dropdown">
                            <button type="button" class="btn p-0" data-bs-toggle="dropdown">
                              <i class="bi bi-three-dots-vertical"></i>
                            </button>
                            <div class="dropdown-menu">
                              <a class="dropdown-item edit-btn" href="javascript:void(0);" data-id="${data}"  data-bs-toggle="modal" data-bs-target="#addUserModal"><i class="bi bi-pencil-square me-1"></i>
                                Edit</a>
                              <a class="dropdown-item delete-btn" href="javascript:void(0);" data-id="${data}"><i class="bi bi-trash-fill me-1"></i>
                                Delete</a>
                            </div>
                        </div>
                    `;
                },
                "orderable": false
            }
        ],
        "order": [[0, "asc"]],
        "paging": true,
        "searching": true,
        "autoWidth": false,
    });
  

    $('#roleTable tbody').on('click', '.delete-btn', function() {
        let id = $(this).data('id');
        if(confirm('Are you sure you want to delete this role?')){
            $.ajax({
                url: `/role/deleteSpecific?id=${id}`,
                type: 'DELETE',
                success: function (response) {
                    if (response.status == "success") {
                        alert(response.message)
                        location.reload()
                    }   
                    else{
                        throw response.message
                    }
                },
                error: function (error) {
                    alert(error)
                }
            });
        }
    });
});


document.querySelector('table tbody').addEventListener('click', (e)=>{
    if (e.target.classList.contains('edit-btn')) {
        let id = e.target.dataset.id


        fetch(`/role/getSpecific?id=${id}`)
        .then(res => res.json())
        .then(response =>{
            if (response.status == "success") {
                const data = response.data

                document.getElementById('roleName').value = data.name
                document.getElementById('roleId').value = data.id
            }
            else{
                throw new Error(data.message);
            }
        })
        .catch(err =>{
            alert(err)
        })
    } 
})


document.getElementById('addUserModal').addEventListener('hidden.bs.modal', ()=>{location.reload()})