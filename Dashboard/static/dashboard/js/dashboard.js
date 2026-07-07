// ========================================
// DASHBOARD MAIN JAVASCRIPT
// ========================================

$(document).ready(function() {
    
    // ========================================
    // SIDEBAR TOGGLE
    // ========================================
    $('#mobileMenuToggle').on('click', function() {
        $('#sidebar').toggleClass('mobile-open');
    });
    
    // Close sidebar on overlay click (mobile)
    $(document).on('click', function(e) {
        if ($(window).width() <= 992) {
            if (!$(e.target).closest('#sidebar').length && 
                !$(e.target).closest('#mobileMenuToggle').length) {
                $('#sidebar').removeClass('mobile-open');
            }
        }
    });
    
    // ========================================
    // FULLSCREEN TOGGLE
    // ========================================
    $('#fullscreenToggle').on('click', function() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {});
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    });
    
    // Update fullscreen icon
    $(document).on('fullscreenchange', function() {
        const icon = $('#fullscreenToggle i');
        if (document.fullscreenElement) {
            icon.removeClass('fa-expand').addClass('fa-compress');
        } else {
            icon.removeClass('fa-compress').addClass('fa-expand');
        }
    });
    
    // ========================================
    // NOTIFICATION DROPDOWN
    // ========================================
    $('#notificationToggle').on('click', function(e) {
        e.stopPropagation();
        $('#notificationDropdown').toggleClass('active');
        $('#profileDropdown').removeClass('active');
    });
    
    // ========================================
    // PROFILE DROPDOWN
    // ========================================
    $('#profileToggle').on('click', function(e) {
        e.stopPropagation();
        $('#profileDropdown').toggleClass('active');
        $('#notificationDropdown').removeClass('active');
    });
    
    // ========================================
    // CLOSE DROPDOWNS ON CLICK OUTSIDE
    // ========================================
    $(document).on('click', function() {
        $('.notification-dropdown, .profile-dropdown').removeClass('active');
    });
    
    // ========================================
    // MARK ALL NOTIFICATIONS
    // ========================================
    $('.mark-all').on('click', function() {
        $('.notification-item').removeClass('unread');
        $('.notification-badge').text('0');
        $(this).text('همه خوانده شد');
    });
    
    // ========================================
    // TOAST NOTIFICATION SYSTEM
    // ========================================
    window.showToast = function(message, type = 'info', duration = 4000) {
        const container = document.getElementById('toastContainer') || createToastContainer();
        
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-times-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i class="fas ${icons[type] || icons.info} toast-icon"></i>
            <span class="toast-message">${message}</span>
            <button class="toast-close">&times;</button>
        `;
        
        container.appendChild(toast);
        
        // Auto remove
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(20px)';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, duration);
        
        // Close button
        toast.querySelector('.toast-close').addEventListener('click', function() {
            toast.remove();
        });
        
        return toast;
    };
    
    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    }
    
    // ========================================
    // SIDEBAR NAVIGATION ACTIVE STATE
    // ========================================
    $('.nav-link').on('click', function() {
        $('.nav-link').removeClass('active');
        $(this).addClass('active');
    });
    
    // ========================================
    // SEARCH FUNCTIONALITY (Demo)
    // ========================================
    $('.search-input').on('keyup', function() {
        const query = $(this).val().toLowerCase();
        // Implement search logic here if needed
        if (query.length > 2) {
            // console.log('Searching for:', query);
        }
    });
    
    // ========================================
    // STAT CARD ANIMATION ON HOVER
    // ========================================
    $('.stat-card').on('mouseenter', function() {
        $(this).find('.stat-number').css('color', 'var(--primary)');
    }).on('mouseleave', function() {
        $(this).find('.stat-number').css('color', '');
    });
    
    // ========================================
    // LIVE CLOCK IN HEADER (if needed)
    // ========================================
    function updateClock() {
        const now = new Date();
        const options = { 
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit',
            hour12: false
        };
        // Add clock element to header if needed
    }
    // setInterval(updateClock, 1000);
    
    console.log('✅ Dashboard initialized successfully');
});