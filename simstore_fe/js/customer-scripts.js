// js/customer-scripts.js
import { apiClient } from './api.js';
import { API_CONFIG } from './config.js';

// Toggle Mobile Menu
export function toggleMenu() {
    const menu = document.getElementById('mobileMenu');
    menu.classList.toggle('hidden');
}

// Smooth Scroll for Links
export function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
}

// Check Login Status and Update Navigation + Auth Section
export async function updateAuthSection() {
    const authSection = document.getElementById('authSection');
    const navMenu = document.getElementById('navMenu');
    const mobileMenu = document.getElementById('mobileMenu');
    const token = localStorage.getItem('access_token');
    const employeeId = localStorage.getItem('employee_id');

    // Reset menu
    navMenu.innerHTML = `
        <a href="#home" class="text-lg font-medium hover:text-yellow-300 transition">Trang chủ</a>
        <a href="#sim-hot" class="text-lg font-medium hover:text-yellow-300 transition">SIM Hot</a>
    `;
    mobileMenu.innerHTML = `
        <a href="#home" class="block px-4 py-3 hover:bg-gray-100">Trang chủ</a>
        <a href="#sim-hot" class="block px-4 py-3 hover:bg-gray-100">SIM Hot</a>
    `;

    if (token && employeeId) {
        try {
            const response = await apiClient.get(`/accounts/employees/${employeeId}/`, true);
            const employee = response.data;
            const avatarUrl = employee.avatar || `${API_CONFIG.BASE_URL}/media/image/avatar_default.png`;

            authSection.innerHTML = `
                <div class="relative group">
                    <div class="flex items-center space-x-2 cursor-pointer">
                        <img src="${avatarUrl}" alt="Avatar" class="w-10 h-10 rounded-full border-2 border-yellow-400">
                        <span class="text-white font-medium">${employee.full_name}</span>
                    </div>
                    <div class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg hidden group-hover:block user-menu">
                        <a href="#" class="block px-4 py-2 text-gray-700 hover:bg-gray-100 focus:outline-none">Thông tin cá nhân</a>
                        <button onclick="logout()" class="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 focus:outline-none">Đăng xuất</button>
                    </div>
                </div>
            `;

            navMenu.innerHTML += `
                <a href="#categories" class="text-lg font-medium hover:text-yellow-300 transition">Danh mục</a>
                <a href="../order/order_list.html" class="text-lg font-medium hover:text-yellow-300 transition">Đơn hàng</a>
            `;
            mobileMenu.innerHTML += `
                <a href="#categories" class="block px-4 py-3 hover:bg-gray-100">Danh mục</a>
                <a href="../order/order_list.html" class="block px-4 py-3 hover:bg-gray-100">Đơn hàng</a>
            `;
        } catch (error) {
            console.error(error);
            localStorage.clear();
            showLoginButton();
        }
    } else {
        showLoginButton();
    }
}

function showLoginButton() {
    const authSection = document.getElementById('authSection');
    authSection.innerHTML = `
        <button onclick="window.location.href='../login.html'" class="px-4 py-2 bg-yellow-400 text-gray-900 font-semibold rounded-full hover:bg-yellow-500 transition">Đăng nhập</button>
    `;
}

window.logout = function () {
    localStorage.clear();
    window.location.reload();
};

// Fetch SIM List with Filters
export async function fetchSims() {
    const simLoading = document.getElementById('simLoading');
    const simError = document.getElementById('simError');
    const simList = document.getElementById('simList');
    const phoneSearch = document.getElementById('phoneSearch').value;
    const priceFilter = document.getElementById('priceFilter').value;
    const networkFilter = document.getElementById('networkFilter').value;

    simLoading.classList.remove('hidden');
    simError.classList.add('hidden');
    simList.innerHTML = '';

    let endpoint = '/simcards/sims/?status=2';
    console.log(`Fetching SIMs with endpoint: ${endpoint}`);
    if (phoneSearch) endpoint += `&phone_number=${phoneSearch}`;
    if (priceFilter) {
        const [min, max] = priceFilter.split('-');
        endpoint += `&price_min=${min}&price_max=${max || ''}`;
    }
    if (networkFilter) endpoint += `&mobile_network=${networkFilter}`;

    try {
        const response = await apiClient.get(endpoint, false);
        simLoading.classList.add('hidden');

        // Kiểm tra nếu response là mảng rỗng
        if (!Array.isArray(response) || response.length === 0) {
            simList.innerHTML = '<p class="text-gray-600 text-center">Không tìm thấy SIM nào phù hợp.</p>';
            return;
        }

        response.forEach((sim, index) => {
            const borderColors = ['border-blue-500', 'border-purple-500', 'border-green-500', 'border-yellow-500'];
            const simCard = document.createElement('div');
            simCard.className = `sim-card bg-white p-6 rounded-xl shadow-md border-t-4 ${borderColors[index % 4]}`;
            simCard.innerHTML = `
                <div class="text-xl font-semibold text-gray-800">${sim.phone_number}</div>
                <div class="text-sm text-gray-600">${sim.mobile_network_operator.name}</div>
                <div class="text-2xl font-bold text-red-600 mt-3">${parseFloat(sim.export_price).toLocaleString('vi-VN')}đ</div>
                <button onclick="buySim(${sim.id})" class="mt-4 w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">Mua ngay</button>
            `;
            simList.appendChild(simCard);
        });
    } catch (error) {
        simLoading.classList.add('hidden');
        simError.classList.remove('hidden');
        simError.textContent = `Lỗi: ${error.message || 'Không thể tải danh sách SIM'}`;
    }
}

// Buy SIM Function (Placeholder)
window.buySim = async function (simId) {
    alert(`Chức năng mua SIM ${simId} chưa được triển khai. Vui lòng cung cấp API đặt hàng!`);
    // Ví dụ logic (khi có API):
    /*
    try {
        const response = await apiClient.post('/orders/create/', { sim_id: simId }, true);
        alert('Đặt hàng thành công!');
        fetchSims(); // Tải lại danh sách SIM
    } catch (error) {
        alert(`Lỗi khi đặt hàng: ${error.message}`);
    }
    */
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    updateAuthSection();
    fetchSims();
    initSmoothScroll();
});