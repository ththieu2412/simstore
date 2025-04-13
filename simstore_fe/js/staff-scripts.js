// js/staff-scripts.js
import { apiClient, getRole } from './api.js';
import { isLoggedIn, logout } from './auth.js';

document.addEventListener('DOMContentLoaded', async () => {
    if (!isLoggedIn() || getRole() !== 'staff') {
        window.location.href = '../../login.html';
    }

    const username = localStorage.getItem('username');
    if (username) {
        const userInfo = document.querySelector('.user-info span');
        if (userInfo) userInfo.textContent = username;
    }

    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar ul li a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath.split('/').pop()) {
            link.parentElement.classList.add('active');
        }
    });

    if (currentPath.includes('index.html')) {
        try {
            const stats = await apiClient.get('/staff/dashboard', true);
            document.querySelector('.stats .card:nth-child(1) p').textContent = stats.data.today_orders || '15';
            document.querySelector('.stats .card:nth-child(2) p').textContent = stats.data.out_of_stock || '10';
            document.querySelector('.stats .card:nth-child(3) p').textContent = stats.data.support_requests || '5';

            const orders = await apiClient.get('/orders/recent', true);
            const tbody = document.querySelector('.table-container tbody');
            tbody.innerHTML = orders.data.map(order => `
                <tr>
                    <td>${order.id}</td>
                    <td>${order.customer_name}</td>
                    <td>${order.sim_number}</td>
                    <td>${order.total.toLocaleString()}</td>
                    <td>${order.status}</td>
                </tr>
            `).join('');
        } catch (error) {
            alert('Không thể tải dữ liệu: ' + error.message);
        }
    }
});