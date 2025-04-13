// js/login.js
import { login } from './auth.js';

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const data = await login(username, password);
            // Chuyển hướng dựa trên role
            if (data.role === 'admin') {
                window.location.href = 'admin/index.html';
            } else if (data.role === 'staff') {
                window.location.href = 'staff/index.html';
            } else {
                // Mặc định quay về trang khách hàng
                window.location.href = 'customer/index.html';
            }
        } catch (error) {
            alert(error.message);
        }
    });
});