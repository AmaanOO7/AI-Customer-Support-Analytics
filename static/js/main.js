/**
 * AI Customer Support Analytics - Main JavaScript
 * Handles file upload and initial interactions
 */

// Global variables
let selectedFile = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeUpload();
    initializeDarkMode();
});

/**
 * Initialize file upload functionality
 */
function initializeUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const uploadBtn = document.getElementById('uploadBtn');
    
    if (!uploadArea || !fileInput || !uploadForm) {
        return; // Not on upload page
    }
    
    // Drag and drop handlers
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#8E44AD';
        uploadArea.style.background = 'rgba(142, 68, 173, 0.1)';
    });
    
    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#2980B9';
        uploadArea.style.background = 'rgba(255, 255, 255, 0.5)';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#2980B9';
        uploadArea.style.background = 'rgba(255, 255, 255, 0.5)';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
    
    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
    
    // Form submission
    uploadForm.addEventListener('submit', (e) => {
        e.preventDefault();
        uploadFile();
    });
}

/**
 * Handle file selection
 */
function handleFileSelect(file) {
    // Validate file type
    const allowedTypes = ['text/csv', 'application/vnd.ms-excel', 
                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
    const allowedExtensions = ['.csv', '.xlsx', '.xls'];
    
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedExtensions.includes(fileExtension)) {
        showAlert('Invalid file type. Please upload CSV, XLSX, or XLS files only.', 'danger');
        return;
    }
    
    // Validate file size (20 MB)
    const maxSize = 20 * 1024 * 1024;
    if (file.size > maxSize) {
        showAlert('File size exceeds 20 MB limit.', 'danger');
        return;
    }
    
    selectedFile = file;
    
    // Update UI
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileInfo').style.display = 'block';
    document.getElementById('uploadBtn').disabled = false;
}

/**
 * Clear selected file
 */
function clearFile() {
    selectedFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('uploadBtn').disabled = true;
}

/**
 * Upload file to server
 */
async function uploadFile() {
    if (!selectedFile) {
        showAlert('Please select a file first.', 'warning');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    // Show progress
    showProgress(0, 'Uploading file...');
    
    try {
        // Upload file
        const uploadResponse = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const uploadResult = await uploadResponse.json();
        
        if (!uploadResponse.ok) {
            throw new Error(uploadResult.error || 'Upload failed');
        }
        
        showProgress(50, 'File uploaded. Starting AI analysis...');
        
        // Start analysis
        const analyzeResponse = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sample_size: null,
                max_workers: 5
            })
        });
        
        const analyzeResult = await analyzeResponse.json();
        
        if (!analyzeResponse.ok) {
            throw new Error(analyzeResult.error || 'Analysis failed');
        }
        
        showProgress(100, 'Analysis complete! Redirecting...');
        
        // Redirect to dashboard
        setTimeout(() => {
            window.location.href = analyzeResult.redirect || '/dashboard';
        }, 1000);
        
    } catch (error) {
        console.error('Error:', error);
        hideProgress();
        showAlert(error.message, 'danger');
    }
}

/**
 * Show progress bar
 */
function showProgress(percentage, text) {
    const progressSection = document.getElementById('progressSection');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    
    if (progressSection && progressBar && progressText) {
        progressSection.style.display = 'block';
        progressBar.style.width = percentage + '%';
        progressBar.textContent = percentage + '%';
        progressText.textContent = text;
    }
}

/**
 * Hide progress bar
 */
function hideProgress() {
    const progressSection = document.getElementById('progressSection');
    if (progressSection) {
        progressSection.style.display = 'none';
    }
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

/**
 * Initialize dark mode toggle
 */
function initializeDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    
    if (!darkModeToggle) {
        return;
    }
    
    // Check saved preference
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
        darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    // Toggle dark mode
    darkModeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark);
        darkModeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    });
}

/**
 * Format number with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Get sentiment badge class
 */
function getSentimentBadgeClass(sentiment) {
    const classes = {
        'Positive': 'bg-success',
        'Neutral': 'bg-info',
        'Negative': 'bg-warning',
        'Very Negative': 'bg-danger'
    };
    return classes[sentiment] || 'bg-secondary';
}

/**
 * Get priority badge class
 */
function getPriorityBadgeClass(priority) {
    const classes = {
        'Low': 'bg-success',
        'Medium': 'bg-warning',
        'High': 'bg-danger',
        'Critical': 'bg-danger'
    };
    return classes[priority] || 'bg-secondary';
}

/**
 * Truncate text
 */
function truncateText(text, maxLength = 100) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

/**
 * Show loading spinner
 */
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
    }
}

/**
 * Export functions for use in other scripts
 */
window.AppUtils = {
    showAlert,
    formatNumber,
    formatDate,
    getSentimentBadgeClass,
    getPriorityBadgeClass,
    truncateText,
    showLoading
};
