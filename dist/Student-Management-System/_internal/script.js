// ==========================================
// 🧰 GLOBAL VARIABLES & ELEMENTS
// ==========================================
const studentForm = document.getElementById('studentForm');
const studentModal = document.getElementById('studentModal');
const modalTitle = document.getElementById('modalTitle');
const searchInput = document.getElementById('searchInput');
const studentsTableBody = document.getElementById('studentsTableBody');

// API URL - This connects our JavaScript to Python
const API_URL = 'http://localhost:5000/api/students';

// ==========================================
// 🚀 START THE APP
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    loadStudents();
    setupSearch();
});

// ==========================================
// 📂 FETCH ALL STUDENTS FROM PYTHON BACKEND
// ==========================================
async function loadStudents() {
    try {
        const response = await fetch(API_URL);
        const students = await response.json();
        
        displayStudents(students);
        updateStatistics(students);
    } catch (error) {
        showError('❌ Could not connect to server. Make sure Python is running!');
        console.error('Error:', error);
    }
}

// ==========================================
// 🖥️ DISPLAY STUDENTS IN THE TABLE
// ==========================================
function displayStudents(students) {
    studentsTableBody.innerHTML = '';

    // Show empty message if no students
    if (students.length === 0) {
        studentsTableBody.innerHTML = `
            <tr>
                <td colspan="7" class="empty-state">
                    <i class="fas fa-user-graduate fa-3x"></i>
                    <p>No students added yet. Click "Add New Student" to start!</p>
                </td>
            </tr>
        `;
        return;
    }

    // Create a row for each student
    students.forEach(student => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${student.admissionNo}</td>
            <td><strong>${student.fullName}</strong></td>
            <td>${student.studentClass}</td>
            <td>${student.age}</td>
            <td>
                <span class="gender-badge ${student.gender.toLowerCase()}">
                    ${student.gender === 'Male' ? '<i class="fas fa-male"></i>' : '<i class="fas fa-female"></i>'} 
                    ${student.gender}
                </span>
            </td>
            <td>${student.contact}</td>
            <td class="action-buttons">
                <button class="btn edit-btn" onclick="openEditForm('${student.id}')" title="Edit Student">
                    <i class="fas fa-pen"></i>
                </button>
                <button class="btn delete-btn" onclick="deleteStudent('${student.id}')" title="Delete Student">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        studentsTableBody.appendChild(row);
    });
}

// ==========================================
// 📊 UPDATE STATISTICS CARDS
// ==========================================
function updateStatistics(students) {
    const totalStudents = students.length;
    const maleCount = students.filter(s => s.gender === 'Male').length;
    const femaleCount = students.filter(s => s.gender === 'Female').length;
    
    // Count unique classes
    const uniqueClasses = [...new Set(students.map(s => s.studentClass))].length;

    // Update numbers on screen
    document.getElementById('totalStudents').textContent = totalStudents;
    document.getElementById('maleCount').textContent = maleCount;
    document.getElementById('femaleCount').textContent = femaleCount;
    document.getElementById('classesCount').textContent = uniqueClasses;
}

// ==========================================
// ➕ OPEN ADD STUDENT FORM
// ==========================================
function openAddStudentForm() {
    modalTitle.innerHTML = '<i class="fas fa-user-plus"></i> Add New Student';
    studentForm.reset();
    document.getElementById('studentId').value = '';
    studentModal.style.display = 'block';
}

// ==========================================
// ✏️ OPEN EDIT STUDENT FORM
// ==========================================
async function openEditForm(studentId) {
    try {
        // Get student data from Python
        const response = await fetch(`${API_URL}/${studentId}`);
        const student = await response.json();

        // Fill form with existing data
        document.getElementById('studentId').value = student.id;
        document.getElementById('fullName').value = student.fullName;
        document.getElementById('admissionNo').value = student.admissionNo;
        document.getElementById('studentClass').value = student.studentClass;
        document.getElementById('age').value = student.age;
        document.getElementById('contact').value = student.contact;
        document.getElementById('address').value = student.address;

        // Set gender radio button
        document.querySelectorAll('input[name="gender"]').forEach(radio => {
            if (radio.value === student.gender) {
                radio.checked = true;
            }
        });

        modalTitle.innerHTML = '<i class="fas fa-edit"></i> Edit Student Details';
        studentModal.style.display = 'block';

    } catch (error) {
        showError('❌ Failed to load student data!');
        console.error('Error:', error);
    }
}

// ==========================================
// 💾 SAVE STUDENT (ADD OR UPDATE)
// ==========================================
studentForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Collect all data from form
    const studentData = {
        fullName: document.getElementById('fullName').value.trim(),
        admissionNo: document.getElementById('admissionNo').value.trim(),
        studentClass: document.getElementById('studentClass').value,
        age: parseInt(document.getElementById('age').value),
        gender: document.querySelector('input[name="gender"]:checked').value,
        contact: document.getElementById('contact').value.trim(),
        address: document.getElementById('address').value.trim()
    };

    const studentId = document.getElementById('studentId').value;

    try {
        let response;
        
        if (studentId) {
            // UPDATE existing student
            response = await fetch(`${API_URL}/${studentId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(studentData)
            });
            showSuccess('✅ Student updated successfully!');
        } else {
            // ADD new student
            response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(studentData)
            });
            showSuccess('✅ New student added successfully!');
        }

        if (response.ok) {
            closeModal();
            loadStudents(); // Refresh table
        }
    } catch (error) {
        showError('❌ Failed to save student!');
        console.error('Error:', error);
    }
});

// ==========================================
// ❌ DELETE STUDENT
// ==========================================
async function deleteStudent(studentId) {
    if (confirm('🗑️ Are you sure you want to delete this student record?\nThis cannot be undone!')) {
        try {
            await fetch(`${API_URL}/${studentId}`, { method: 'DELETE' });
            showSuccess('✅ Student deleted successfully!');
            loadStudents(); // Refresh table
        } catch (error) {
            showError('❌ Failed to delete student!');
            console.error('Error:', error);
        }
    }
}

// ==========================================
// 🔍 SEARCH FUNCTION
// ==========================================
function setupSearch() {
    searchInput.addEventListener('input', async (e) => {
        const searchTerm = e.target.value.trim().toLowerCase();
        
        try {
            const response = await fetch(API_URL);
            const students = await response.json();

            // Filter students based on search
            const filteredStudents = students.filter(student => 
                student.fullName.toLowerCase().includes(searchTerm) ||
                student.admissionNo.toLowerCase().includes(searchTerm) ||
                student.studentClass.toLowerCase().includes(searchTerm)
            );

            displayStudents(filteredStudents);
            updateStatistics(filteredStudents);

        } catch (error) {
            console.error('Search error:', error);
        }
    });
}

// ==========================================
// 🚪 CLOSE MODAL
// ==========================================
function closeModal() {
    studentModal.style.display = 'none';
    studentForm.reset();
}

// Close if click outside form
window.onclick = (event) => {
    if (event.target === studentModal) {
        closeModal();
    }
};

// ==========================================
// 💬 NOTIFICATION MESSAGES
// ==========================================
function showSuccess(message) {
    // You can replace this with a nice popup later
    alert(message);
}

function showError(message) {
    alert(message);
}