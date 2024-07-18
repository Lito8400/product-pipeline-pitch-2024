/**
* Template Name: NiceAdmin
* Template URL: https://bootstrapmade.com/nice-admin-bootstrap-admin-html-template/
* Updated: Apr 20 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function(e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Initiate tooltips
   */
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  /**
   * Initiate quill editors
   */
  if (select('.quill-editor-default')) {
    new Quill('.quill-editor-default', {
      theme: 'snow'
    });
  }

  if (select('.quill-editor-bubble')) {
    new Quill('.quill-editor-bubble', {
      theme: 'bubble'
    });
  }

  if (select('.quill-editor-full')) {
    new Quill(".quill-editor-full", {
      modules: {
        toolbar: [
          [{
            font: []
          }, {
            size: []
          }],
          ["bold", "italic", "underline", "strike"],
          [{
              color: []
            },
            {
              background: []
            }
          ],
          [{
              script: "super"
            },
            {
              script: "sub"
            }
          ],
          [{
              list: "ordered"
            },
            {
              list: "bullet"
            },
            {
              indent: "-1"
            },
            {
              indent: "+1"
            }
          ],
          ["direction", {
            align: []
          }],
          ["link", "image", "video"],
          ["clean"]
        ]
      },
      theme: "snow"
    });
  }

  /**
   * Initiate TinyMCE Editor
   */

  const useDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isSmallScreen = window.matchMedia('(max-width: 1023.5px)').matches;

  tinymce.init({
    selector: 'textarea.tinymce-editor',
    plugins: 'preview importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media codesample table charmap pagebreak nonbreaking anchor insertdatetime advlist lists wordcount help charmap quickbars emoticons accordion',
    editimage_cors_hosts: ['picsum.photos'],
    menubar: 'file edit view insert format tools table help',
    toolbar: "undo redo | accordion accordionremove | blocks fontfamily fontsize | bold italic underline strikethrough | align numlist bullist | link image | table media | lineheight outdent indent| forecolor backcolor removeformat | charmap emoticons | code fullscreen preview | save print | pagebreak anchor codesample | ltr rtl",
    autosave_ask_before_unload: true,
    autosave_interval: '30s',
    autosave_prefix: '{path}{query}-{id}-',
    autosave_restore_when_empty: false,
    autosave_retention: '2m',
    image_advtab: true,
    link_list: [{
        title: 'My page 1',
        value: 'https://www.tiny.cloud'
      },
      {
        title: 'My page 2',
        value: 'http://www.moxiecode.com'
      }
    ],
    image_list: [{
        title: 'My page 1',
        value: 'https://www.tiny.cloud'
      },
      {
        title: 'My page 2',
        value: 'http://www.moxiecode.com'
      }
    ],
    image_class_list: [{
        title: 'None',
        value: ''
      },
      {
        title: 'Some class',
        value: 'class-name'
      }
    ],
    importcss_append: true,
    file_picker_callback: (callback, value, meta) => {
      /* Provide file and text for the link dialog */
      if (meta.filetype === 'file') {
        callback('https://www.google.com/logos/google.jpg', {
          text: 'My text'
        });
      }

      /* Provide image and alt text for the image dialog */
      if (meta.filetype === 'image') {
        callback('https://www.google.com/logos/google.jpg', {
          alt: 'My alt text'
        });
      }

      /* Provide alternative source and posted for the media dialog */
      if (meta.filetype === 'media') {
        callback('movie.mp4', {
          source2: 'alt.ogg',
          poster: 'https://www.google.com/logos/google.jpg'
        });
      }
    },
    height: 600,
    image_caption: true,
    quickbars_selection_toolbar: 'bold italic | quicklink h2 h3 blockquote quickimage quicktable',
    noneditable_class: 'mceNonEditable',
    toolbar_mode: 'sliding',
    contextmenu: 'link image table',
    skin: useDarkMode ? 'oxide-dark' : 'oxide',
    content_css: useDarkMode ? 'dark' : 'default',
    content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }'
  });

  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function(form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable, {
      perPageSelect: [150, 200, 300, ["All", -1]],
      columns: [
        {
          select: 4,
          cellClass: "green",
          headerClass: "red"
        }
      ]
    });
  })

  /**
   * Autoresize echart charts
   */
  const mainContainer = select('#main');
  if (mainContainer) {
    setTimeout(() => {
      new ResizeObserver(function() {
        select('.echart', true).forEach(getEchart => {
          echarts.getInstanceByDom(getEchart).resize();
        })
      }).observe(mainContainer);
    }, 200);
  }

})();

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
};

function openDeleteModal(id, name) {
  document.getElementById('itemName').textContent = name;
  const deleteUrl = `/admin/delete_product/${id}`;
  document.getElementById('confirmDeleteBtn').setAttribute('href', deleteUrl);

  document.getElementById('deleteConfirmModal').addEventListener('keydown', function(event) {
      if (event.key === 'Enter') {
          document.getElementById('confirmDeleteBtn').click();
      }
  });
};
function openDeleteAllModal() {
  document.getElementById('itemName').textContent = 'All Concepts';
  const deleteUrl = `/admin/delete_all_product`;
  document.getElementById('confirmDeleteBtn').setAttribute('href', deleteUrl);

  document.getElementById('deleteConfirmModal').addEventListener('keydown', function(event) {
      if (event.key === 'Enter') {
          document.getElementById('confirmDeleteBtn').click();
      }
  });
};

function openEditUserModal(id) {
  var editUserId = document.getElementById('editUserId');
  var editUserName = document.getElementById('editUserName');

  editUserId.value = id;
  editUserName.value = id;
};

function openDeleteUserModal(id) {
  document.getElementById('itemName').textContent = id;
  const deleteUrl = `/admin/delete_user/${id}`;
  document.getElementById('confirmDeleteBtn').setAttribute('href', deleteUrl);

  document.getElementById('deleteConfirmModal').addEventListener('keydown', function(event) {
      if (event.key === 'Enter') {
          document.getElementById('confirmDeleteBtn').click();
      }
  });
};

function openDeleteAllUserModal() {
  document.getElementById('itemName').textContent = 'All Users';
  const deleteUrl = `/admin/delete_all_users`;
  document.getElementById('confirmDeleteBtn').setAttribute('href', deleteUrl);

  document.getElementById('deleteConfirmModal').addEventListener('keydown', function(event) {
      if (event.key === 'Enter') {
          document.getElementById('confirmDeleteBtn').click();
      }
  });
};

var socket = io();

socket.on('update_measure_concepts', function(data) {
  var tableBody = document.getElementById("measureconceptstable");
  var tableBodymodel = document.getElementById("measureconceptstablemodel");
  var tbody = tableBody.querySelector('tbody');
  var tbodymodel = tableBodymodel.querySelector('tbody');

  // Xóa các hàng cũ
  while (tbody.firstChild) {
    tbody.removeChild(tbody.firstChild);
  }
  while (tbodymodel.firstChild) {
      tbodymodel.removeChild(tbodymodel.firstChild);
  }

  data.forEach(function(product, index) {
    var row = tbody.insertRow();
    row.dataset.index = index;

    var cell1 = row.insertCell(0);
    cell1.innerText = product.product_name;

    var cell2 = row.insertCell(1);
    cell2.style.textAlign = "center";
    cell2.style.verticalAlign = "middle";
    cell2.innerText = product.Rating;

    var cell3 = row.insertCell(2);
    cell3.style.textAlign = "center";
    cell3.style.verticalAlign = "middle";
    cell3.innerText = product.WRating;

    var cell4 = row.insertCell(3);
    cell4.style.textAlign = "center";
    cell4.style.verticalAlign = "middle";
    cell4.innerText = product.Participation;

    var cell5 = row.insertCell(4);
    cell5.style.textAlign = "center";
    cell5.style.verticalAlign = "middle";
    cell5.className = "green";
    cell5.innerText = product.Average_interested_lanched;

    var cell6 = row.insertCell(5);
    cell6.style.textAlign = "center";
    cell6.style.verticalAlign = "middle";
    cell6.innerText = product.Average_path_to_market;

    var cell7 = row.insertCell(6);
    cell7.style.textAlign = "center";
    cell7.style.verticalAlign = "middle";
    cell7.innerText = product.Average_pull_sales;

    // Thêm dòng vào tbodymodel tương tự
    var rowModel = tbodymodel.insertRow();
    rowModel.innerHTML = row.innerHTML; // Sao chép nội dung
    rowModel.dataset.index = index;
  });
});

socket.on('update_total_user', function(data) {
  var tuser = document.getElementById("totaluser");
  tuser.innerText = data;
});

socket.on('update_total_survey', function(data) {
  var tsurvey = document.getElementById("totalsurvey");
  tsurvey.innerText = data;
});
