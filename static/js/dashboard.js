/**
 * AI Customer Support Analytics - Dashboard JavaScript
 * Handles dashboard interactions, charts, filters, and ticket management
 */

// Global variables
let currentPage = 1;
let currentFilters = {};
let allCharts = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    initializeFilters();
    loadTickets();
    initializeDarkMode();
});

/**
 * Initialize all Chart.js charts
 */
function initializeCharts() {
    if (typeof chartData === 'undefined') {
        console.error('Chart data not available');
        return;
    }
    
    // Sentiment Chart
    if (chartData.sentiment && document.getElementById('sentimentChart')) {
        allCharts.sentiment = new Chart(
            document.getElementById('sentimentChart'),
            chartData.sentiment
        );
    }
    
    // Emotion Chart
    if (chartData.emotion && document.getElementById('emotionChart')) {
        allCharts.emotion = new Chart(
            document.getElementById('emotionChart'),
            chartData.emotion
        );
    }
    
    // Category Chart
    if (chartData.category && document.getElementById('categoryChart')) {
        allCharts.category = new Chart(
            document.getElementById('categoryChart'),
            chartData.category
        );
    }
    
    // Priority Chart
    if (chartData.priority && document.getElementById('priorityChart')) {
        allCharts.priority = new Chart(
            document.getElementById('priorityChart'),
            chartData.priority
        );
    }
    
    // Satisfaction Chart
    if (chartData.satisfaction && document.getElementById('satisfactionChart')) {
        allCharts.satisfaction = new Chart(
            document.getElementById('satisfactionChart'),
            chartData.satisfaction
        );
    }
    
    // Agent Performance Chart
    if (chartData.agent_performance && document.getElementById('agentChart')) {
        allCharts.agent = new Chart(
            document.getElementById('agentChart'),
            chartData.agent_performance
        );
    }
}

/**
 * Initialize filter functionality
 */
async function initializeFilters() {
    try {
        // Load filter options
        const response = await fetch('/api/filters');
        const filters = await response.json();
        
        // Populate filter dropdowns
        populateSelect('filterSentiment', filters.sentiments);
        populateSelect('filterEmotion', filters.emotions);
        populateSelect('filterPriority', filters.priorities);
        populateSelect('filterCategory', filters.categories);
        
        // Apply filters button
        document.getElementById('applyFilters').addEventListener('click', () => {
            applyFilters();
        });
        
        // Clear filters button
        document.getElementById('clearFilters').addEventListener('click', () => {
            clearFilters();
        });
        
        // Enter key on keyword search
        document.getElementById('filterKeyword').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                applyFilters();
            }
        });
        
    } catch (error) {
        console.error('Error loading filters:', error);
    }
}

/**
 * Populate select dropdown
 */
function populateSelect(selectId, options) {
    const select = document.getElementById(selectId);
    if (!select) return;
    
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        select.appendChild(optionElement);
    });
}

/**
 * Apply filters
 */
function applyFilters() {
    currentFilters = {
        sentiment: document.getElementById('filterSentiment').value,
        emotion: document.getElementById('filterEmotion').value,
        priority: document.getElementById('filterPriority').value,
        category: document.getElementById('filterCategory').value,
        keyword: document.getElementById('filterKeyword').value
    };
    
    // Remove empty filters
    Object.keys(currentFilters).forEach(key => {
        if (!currentFilters[key]) {
            delete currentFilters[key];
        }
    });
    
    currentPage = 1;
    loadTickets();
}

/**
 * Clear all filters
 */
function clearFilters() {
    document.getElementById('filterSentiment').value = '';
    document.getElementById('filterEmotion').value = '';
    document.getElementById('filterPriority').value = '';
    document.getElementById('filterCategory').value = '';
    document.getElementById('filterKeyword').value = '';
    
    currentFilters = {};
    currentPage = 1;
    loadTickets();
}

/**
 * Load tickets with pagination and filters
 */
async function loadTickets(page = 1) {
    currentPage = page;
    
    try {
        // Build query string
        const params = new URLSearchParams({
            page: currentPage,
            per_page: 20,
            ...currentFilters
        });
        
        // Show loading
        const tbody = document.getElementById('ticketsTableBody');
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </td>
            </tr>
        `;
        
        // Fetch tickets
        const response = await fetch(`/api/tickets?${params}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to load tickets');
        }
        
        // Render tickets
        renderTickets(data.tickets);
        
        // Render pagination
        renderPagination(data.page, data.total_pages);
        
    } catch (error) {
        console.error('Error loading tickets:', error);
        const tbody = document.getElementById('ticketsTableBody');
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center text-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Error loading tickets: ${error.message}
                </td>
            </tr>
        `;
    }
}

/**
 * Render tickets table
 */
function renderTickets(tickets) {
    const tbody = document.getElementById('ticketsTableBody');
    
    if (!tickets || tickets.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center text-muted">
                    <i class="fas fa-inbox me-2"></i>
                    No tickets found
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = tickets.map(ticket => `
        <tr>
            <td><strong>${escapeHtml(ticket.ticket_id || 'N/A')}</strong></td>
            <td>${escapeHtml(ticket.customer_name || 'N/A')}</td>
            <td>
                <span class="badge ${getSentimentBadgeClass(ticket.sentiment)}">
                    ${escapeHtml(ticket.sentiment || 'N/A')}
                </span>
            </td>
            <td>
                <span class="badge bg-info">
                    ${escapeHtml(ticket.emotion || 'N/A')}
                </span>
            </td>
            <td>
                <span class="badge ${getPriorityBadgeClass(ticket.priority)}">
                    ${escapeHtml(ticket.priority || 'N/A')}
                </span>
            </td>
            <td>${escapeHtml(ticket.issue_category || 'N/A')}</td>
            <td>
                <strong>${ticket.customer_satisfaction_score || 'N/A'}</strong>
                ${ticket.customer_satisfaction_score ? '%' : ''}
            </td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="viewTicketDetail('${escapeHtml(ticket.ticket_id)}')">
                    <i class="fas fa-eye me-1"></i>View
                </button>
            </td>
        </tr>
    `).join('');
}

/**
 * Render pagination
 */
function renderPagination(currentPage, totalPages) {
    const pagination = document.getElementById('pagination');
    
    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }
    
    let html = '';
    
    // Previous button
    html += `
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="loadTickets(${currentPage - 1}); return false;">
                <i class="fas fa-chevron-left"></i>
            </a>
        </li>
    `;
    
    // Page numbers
    const maxPages = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxPages / 2));
    let endPage = Math.min(totalPages, startPage + maxPages - 1);
    
    if (endPage - startPage < maxPages - 1) {
        startPage = Math.max(1, endPage - maxPages + 1);
    }
    
    for (let i = startPage; i <= endPage; i++) {
        html += `
            <li class="page-item ${i === currentPage ? 'active' : ''}">
                <a class="page-link" href="#" onclick="loadTickets(${i}); return false;">
                    ${i}
                </a>
            </li>
        `;
    }
    
    // Next button
    html += `
        <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="loadTickets(${currentPage + 1}); return false;">
                <i class="fas fa-chevron-right"></i>
            </a>
        </li>
    `;
    
    pagination.innerHTML = html;
}

/**
 * View ticket detail
 */
async function viewTicketDetail(ticketId) {
    try {
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('ticketModal'));
        modal.show();
        
        // Show loading
        document.getElementById('ticketDetailContent').innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
        
        // Fetch ticket details
        const response = await fetch(`/api/ticket/${encodeURIComponent(ticketId)}`);
        const ticket = await response.json();
        
        if (!response.ok) {
            throw new Error(ticket.error || 'Failed to load ticket details');
        }
        
        // Render ticket details
        renderTicketDetail(ticket);
        
    } catch (error) {
        console.error('Error loading ticket detail:', error);
        document.getElementById('ticketDetailContent').innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Error loading ticket details: ${error.message}
            </div>
        `;
    }
}

/**
 * Render ticket detail
 */
function renderTicketDetail(ticket) {
    const agentAnalysis = ticket.agent_analysis || {};
    
    const html = `
        <div class="ticket-detail">
            <!-- Basic Info -->
            <div class="row mb-4">
                <div class="col-md-6">
                    <h6 class="text-muted">Ticket ID</h6>
                    <p><strong>${escapeHtml(ticket.ticket_id || 'N/A')}</strong></p>
                </div>
                <div class="col-md-6">
                    <h6 class="text-muted">Customer</h6>
                    <p>${escapeHtml(ticket.customer_name || 'N/A')}</p>
                </div>
                <div class="col-md-6">
                    <h6 class="text-muted">Agent</h6>
                    <p>${escapeHtml(ticket.agent_name || 'N/A')}</p>
                </div>
                <div class="col-md-6">
                    <h6 class="text-muted">Date</h6>
                    <p>${escapeHtml(ticket.date || 'N/A')}</p>
                </div>
            </div>
            
            <!-- Customer Message -->
            <div class="mb-4">
                <h5><i class="fas fa-comment me-2 text-primary"></i>Customer Message</h5>
                <div class="p-3 bg-light rounded">
                    ${escapeHtml(ticket.customer_message || 'N/A')}
                </div>
            </div>
            
            <!-- Agent Response -->
            ${ticket.agent_response ? `
                <div class="mb-4">
                    <h5><i class="fas fa-reply me-2 text-success"></i>Agent Response</h5>
                    <div class="p-3 bg-light rounded">
                        ${escapeHtml(ticket.agent_response)}
                    </div>
                </div>
            ` : ''}
            
            <!-- AI Analysis -->
            <div class="mb-4">
                <h5><i class="fas fa-brain me-2 text-info"></i>AI Analysis</h5>
                <div class="row g-3">
                    <div class="col-md-6">
                        <div class="p-3 bg-light rounded">
                            <h6 class="text-muted mb-2">Sentiment</h6>
                            <span class="badge ${getSentimentBadgeClass(ticket.sentiment)} fs-6">
                                ${escapeHtml(ticket.sentiment || 'N/A')}
                            </span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-3 bg-light rounded">
                            <h6 class="text-muted mb-2">Emotion</h6>
                            <span class="badge bg-info fs-6">
                                ${escapeHtml(ticket.emotion || 'N/A')}
                            </span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-3 bg-light rounded">
                            <h6 class="text-muted mb-2">Priority</h6>
                            <span class="badge ${getPriorityBadgeClass(ticket.priority)} fs-6">
                                ${escapeHtml(ticket.priority || 'N/A')}
                            </span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-3 bg-light rounded">
                            <h6 class="text-muted mb-2">Urgency</h6>
                            <span class="badge bg-warning fs-6">
                                ${escapeHtml(ticket.urgency || 'N/A')}
                            </span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-3 bg-light rounded">
                            <h6 class="text-muted mb-2">Intent</h6>
                            <p class="mb-0">${escapeHtml(ticket.intent || 'N/A')}</p>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-3 bg-light rounded">
                            <h6 class="text-muted mb-2">Issue Category</h6>
                            <p class="mb-0">${escapeHtml(ticket.issue_category || 'N/A')}</p>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-3 bg-light rounded">
                            <h6 class="text-muted mb-2">Customer Satisfaction</h6>
                            <p class="mb-0"><strong>${ticket.customer_satisfaction_score || 'N/A'}</strong>${ticket.customer_satisfaction_score ? '%' : ''}</p>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-3 bg-light rounded">
                            <h6 class="text-muted mb-2">Churn Risk</h6>
                            <span class="badge ${ticket.churn_risk === 'High' ? 'bg-danger' : ticket.churn_risk === 'Medium' ? 'bg-warning' : 'bg-success'} fs-6">
                                ${escapeHtml(ticket.churn_risk || 'N/A')}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Complaint Summary -->
            ${ticket.complaint_summary ? `
                <div class="mb-4">
                    <h5><i class="fas fa-file-alt me-2 text-warning"></i>Complaint Summary</h5>
                    <div class="p-3 bg-light rounded">
                        ${escapeHtml(ticket.complaint_summary)}
                    </div>
                </div>
            ` : ''}
            
            <!-- Root Cause -->
            ${ticket.root_cause ? `
                <div class="mb-4">
                    <h5><i class="fas fa-search me-2 text-danger"></i>Root Cause</h5>
                    <div class="p-3 bg-light rounded">
                        ${escapeHtml(ticket.root_cause)}
                    </div>
                </div>
            ` : ''}
            
            <!-- Keywords -->
            ${ticket.keywords && ticket.keywords.length > 0 ? `
                <div class="mb-4">
                    <h5><i class="fas fa-tags me-2 text-info"></i>Keywords</h5>
                    <div>
                        ${ticket.keywords.map(keyword => `
                            <span class="badge bg-secondary me-2 mb-2">${escapeHtml(keyword)}</span>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
            
            <!-- Escalation -->
            ${ticket.escalation_needed ? `
                <div class="mb-4">
                    <h5><i class="fas fa-arrow-up me-2 text-warning"></i>Escalation</h5>
                    <div class="p-3 ${ticket.escalation_needed === 'Yes' ? 'bg-warning' : 'bg-success'} bg-opacity-10 rounded">
                        <p class="mb-2"><strong>Escalation Needed:</strong> ${escapeHtml(ticket.escalation_needed)}</p>
                        ${ticket.escalation_reason ? `<p class="mb-0"><strong>Reason:</strong> ${escapeHtml(ticket.escalation_reason)}</p>` : ''}
                    </div>
                </div>
            ` : ''}
            
            <!-- Agent Performance -->
            ${agentAnalysis.overall_score ? `
                <div class="mb-4">
                    <h5><i class="fas fa-user-tie me-2 text-primary"></i>Agent Performance</h5>
                    <div class="row g-3">
                        <div class="col-md-4">
                            <div class="p-3 bg-light rounded text-center">
                                <h6 class="text-muted mb-2">Overall Score</h6>
                                <h3 class="mb-0 text-primary">${agentAnalysis.overall_score}%</h3>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="p-3 bg-light rounded text-center">
                                <h6 class="text-muted mb-2">Professionalism</h6>
                                <h3 class="mb-0">${agentAnalysis.professionalism_score || 'N/A'}%</h3>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="p-3 bg-light rounded text-center">
                                <h6 class="text-muted mb-2">Empathy</h6>
                                <h3 class="mb-0">${agentAnalysis.empathy_score || 'N/A'}%</h3>
                            </div>
                        </div>
                    </div>
                    
                    ${agentAnalysis.strengths && agentAnalysis.strengths.length > 0 ? `
                        <div class="mt-3">
                            <h6 class="text-success"><i class="fas fa-check-circle me-2"></i>Strengths</h6>
                            <ul>
                                ${agentAnalysis.strengths.map(s => `<li>${escapeHtml(s)}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${agentAnalysis.improvements && agentAnalysis.improvements.length > 0 ? `
                        <div class="mt-3">
                            <h6 class="text-warning"><i class="fas fa-lightbulb me-2"></i>Improvements</h6>
                            <ul>
                                ${agentAnalysis.improvements.map(i => `<li>${escapeHtml(i)}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${agentAnalysis.improved_response ? `
                        <div class="mt-3">
                            <h6 class="text-info"><i class="fas fa-magic me-2"></i>AI-Improved Response</h6>
                            <div class="p-3 bg-info bg-opacity-10 rounded">
                                ${escapeHtml(agentAnalysis.improved_response)}
                            </div>
                        </div>
                    ` : ''}
                </div>
            ` : ''}
        </div>
    `;
    
    document.getElementById('ticketDetailContent').innerHTML = html;
}

/**
 * Initialize dark mode
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
 * Utility functions
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function getSentimentBadgeClass(sentiment) {
    const classes = {
        'Positive': 'bg-success',
        'Neutral': 'bg-info',
        'Negative': 'bg-warning',
        'Very Negative': 'bg-danger'
    };
    return classes[sentiment] || 'bg-secondary';
}

function getPriorityBadgeClass(priority) {
    const classes = {
        'Low': 'bg-success',
        'Medium': 'bg-warning',
        'High': 'bg-danger',
        'Critical': 'bg-danger'
    };
    return classes[priority] || 'bg-secondary';
}

// Make functions globally accessible
window.loadTickets = loadTickets;
window.viewTicketDetail = viewTicketDetail;
