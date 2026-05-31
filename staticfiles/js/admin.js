document.addEventListener('DOMContentLoaded', function () {
    // Auto-close alerts after 5 seconds
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Toggle sidebar on mobile
    window.toggleSidebar = function () {
        const sidebar = document.querySelector('.admin-sidebar');
        sidebar.classList.toggle('show');
    };

    // Close sidebar when clicking outside (mobile)
    document.addEventListener('click', function (e) {
        const sidebar = document.querySelector('.admin-sidebar');
        const toggle = document.querySelector('.sidebar-toggle');
        if (window.innerWidth < 992) {
            if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        }
    });

    // Highlight current page in nav
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Confirm delete forms
    document.querySelectorAll('.confirm-delete').forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });

    // Image preview
    const imageInput = document.querySelector('input[type="file"]');
    if (imageInput) {
        imageInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const preview = document.querySelector('.image-preview');
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
});
