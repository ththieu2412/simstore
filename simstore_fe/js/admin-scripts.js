// js/admin-scripts.js
import { fetchEmployees, searchEmployees } from './employee-scripts.js';
import { apiClient } from './api.js';

// Load Page Content
export function loadPage(page) {
    console.log(`Attempting to load page: ${page}`);

    // Ẩn tất cả các nội dung trang
    const allContents = document.querySelectorAll('.page-content');
    allContents.forEach((content) => {
        content.classList.remove('active');
    });

    // Hiển thị nội dung trang được chọn
    const contentArea = document.getElementById(page);
    if (contentArea) {
        contentArea.classList.add('active');
        console.log(`Showing: ${contentArea.id}`);
    } else {
        console.error(`Page ${page} not found`);
    }
}

// Gắn sự kiện cho sidebar
function initSidebar() {
    const links = document.querySelectorAll('.sidebar a[data-load]');
    console.log(`Found ${links.length} sidebar links`);
    links.forEach((link) => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.getAttribute('data-load');
            console.log(`Sidebar clicked: ${page}`);
            loadPage(page);
        });
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing sidebar');
    initSidebar();
    loadPage('dashboard');
});