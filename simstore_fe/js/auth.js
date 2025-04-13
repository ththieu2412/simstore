// js/auth.js
import { apiClient } from './api.js';

// Lưu thông tin đăng nhập
export function saveAuthData(authData) {
    localStorage.setItem('access_token', authData.access_token);
    localStorage.setItem('refresh_token', authData.refresh_token);
    localStorage.setItem('username', authData.username);
    localStorage.setItem('role', authData.role);
    localStorage.setItem('employee_id', authData.employee_id);
}

// Lấy access token
export function getToken() {
    return localStorage.getItem('access_token');
}

// Lấy refresh token
export function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}

// Kiểm tra đăng nhập
export function isLoggedIn() {
    return !!getToken();
}

// Lấy vai trò
export function getRole() {
    return localStorage.getItem('role');
}

// Đăng xuất
export function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    localStorage.removeItem('role');
    localStorage.removeItem('employee_id');
    window.location.href = '../login.html';
}

// Làm mới token
export async function refreshAccessToken() {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
        logout();
        return null;
    }

    try {
        const response = await apiClient.post('/auth/refresh', { refresh_token: refreshToken }, false);
        if (response.status === 'success') {
            saveAuthData(response.data);
            return response.data.access_token;
        }
        return null;
    } catch (error) {
        console.error('Refresh token failed:', error);
        logout();
        return null;
    }
}

// Đăng nhập
export async function login(username, password) {
    try {
        const response = await apiClient.post('/accounts/accounts/login/', { username, password }, false);
        if (response.status === 'success' && response.statuscode === 200) {
            saveAuthData(response.data);
            return response.data;
        }
        throw new Error(response.errorMessage || 'Đăng nhập thất bại!');
    } catch (error) {
        throw error;
    }
}