/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

function openEditModal(id, name, description) {
    var editProductId = document.getElementById('editProductId');
    var editProductName = document.getElementById('editProductName');
    var editProductDescription = document.getElementById('editProductDescription');

    editProductId.value = id;
    editProductName.value = name;
    editProductDescription.value = description;
}

function openDeleteModal(id, name) {
    document.getElementById('itemName').textContent = name;
    const deleteUrl = `/admin/delete_product/${id}`;
    document.getElementById('confirmDeleteBtn').setAttribute('href', deleteUrl);

    document.getElementById('deleteConfirmModal').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            document.getElementById('confirmDeleteBtn').click();
        }
    });
}
function openDeleteAllModal() {
    document.getElementById('itemName').textContent = 'All Concepts';
    const deleteUrl = `/admin/delete_all_product`;
    document.getElementById('confirmDeleteBtn').setAttribute('href', deleteUrl);

    document.getElementById('deleteConfirmModal').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            document.getElementById('confirmDeleteBtn').click();
        }
    });
}

function openEditUserModal(id) {
    var editUserId = document.getElementById('editUserId');
    var editUserName = document.getElementById('editUserName');

    editUserId.value = id;
    editUserName.value = id;
}

function openDeleteUserModal(id) {
    document.getElementById('itemName').textContent = id;
    const deleteUrl = `/admin/delete_user/${id}`;
    document.getElementById('confirmDeleteBtn').setAttribute('href', deleteUrl);

    document.getElementById('deleteConfirmModal').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            document.getElementById('confirmDeleteBtn').click();
        }
    });
}

function openDeleteAllUserModal() {
    document.getElementById('itemName').textContent = 'All Users';
    const deleteUrl = `/admin/delete_all_users`;
    document.getElementById('confirmDeleteBtn').setAttribute('href', deleteUrl);

    document.getElementById('deleteConfirmModal').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            document.getElementById('confirmDeleteBtn').click();
        }
    });
}


