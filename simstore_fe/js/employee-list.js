// js/employee-scripts.js (giữ nguyên)
import { apiClient } from './api.js';
import { API_CONFIG } from './config.js';

let allEmployees = [];

export async function fetchEmployees() {
    const tableContainer = document.getElementById('employeeTable');
    tableContainer.innerHTML = '<div class="spinner"></div>';
    try {
        const response = await apiClient.get('/accounts/employees/', true);
        allEmployees = response;
        displayEmployees(allEmployees);
    } catch (error) {
        tableContainer.innerHTML = `<p class="error">Lỗi: ${error.message}</p>`;
    }
}

export function displayEmployees(employees) {
    let tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Họ tên</th>
                    <th>Ngày sinh</th>
                    <th>Giới tính</th>
                    <th>Email</th>
                    <th>Trạng thái</th>
                </tr>
            </thead>
            <tbody>
    `;

    employees.forEach((employee) => {
        tableHTML += `
            <tr onclick="window.location.href='employee_detail.html?id=${employee.id}'">
                <td>${employee.id}</td>
                <td>${employee.full_name}</td>
                <td>${employee.date_of_birth}</td>
                <td>${employee.gender ? 'Nam' : 'Nữ'}</td>
                <td>${employee.email}</td>
                <td>${employee.status ? 'Đang làm việc' : 'Đã nghỉ việc'}</td>
            </tr>
        `;
    });

    tableHTML += `</tbody></table>`;
    document.getElementById('employeeTable').innerHTML = tableHTML;
}

export function searchEmployees() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filteredEmployees = allEmployees.filter((employee) =>
        employee.full_name.toLowerCase().includes(searchTerm)
    );
    displayEmployees(filteredEmployees);
}