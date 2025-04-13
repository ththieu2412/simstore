// js/api.js
import { API_CONFIG } from './config.js';
import { getToken, refreshAccessToken, logout } from './auth.js';

class ApiClient {
    async request(method, endpoint, data = null, requiresAuth = false) {
        const url = `${API_CONFIG.BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json'
        };

        if (requiresAuth) {
            const token = getToken();
            if (!token) {
                logout();
                throw new Error('No access token found. Please login.');
            }
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            method,
            headers,
            timeout: API_CONFIG.TIMEOUT
        };

        if (data) {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, config);

            if (requiresAuth && response.status === 401) {
                const newToken = await refreshAccessToken();
                if (newToken) {
                    headers['Authorization'] = `Bearer ${newToken}`;
                    const retryResponse = await fetch(url, { ...config, headers });
                    return await retryResponse.json();
                }
                logout();
                throw new Error('Unable to refresh token.');
            }

            if (response.status === 403) {
                throw new Error('Access denied. Insufficient permissions.');
            }

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.errorMessage || 'API request failed');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    get(endpoint, requiresAuth = false) {
        return this.request('GET', endpoint, null, requiresAuth);
    }

    post(endpoint, data, requiresAuth = false) {
        return this.request('POST', endpoint, data, requiresAuth);
    }

    put(endpoint, data, requiresAuth = false) {
        return this.request('PUT', endpoint, data, requiresAuth);
    }

    delete(endpoint, requiresAuth = false) {
        return this.request('DELETE', endpoint, null, requiresAuth);
    }
}

export const apiClient = new ApiClient();