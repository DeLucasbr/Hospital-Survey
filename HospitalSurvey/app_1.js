// Hospital Satisfaction Survey Application

// Survey data from the original React Native application
const SURVEY_DATA = {
    sections: [
        {
            title: "Seção 1: Atendimento",
            questions: [
                {
                    id: "q1_1",
                    text: "1. Como você avaliaria a qualidade do atendimento recebido no hospital?",
                    options: ["Muito satisfeito(a)", "Satisfeito(a)", "Neutro(a)", "Insatisfeito(a)", "Muito insatisfeito(a)"]
                },
                {
                    id: "q1_2", 
                    text: "2. Os profissionais de saúde foram atenciosos e respeitosos com você?",
                    options: ["Sim", "Não", "Em parte"]
                },
                {
                    id: "q1_3",
                    text: "3. Você sentiu que suas necessidades foram atendidas de forma eficaz?", 
                    options: ["Sim", "Não", "Em parte"]
                }
            ]
        },
        {
            title: "Seção 2: Instalações e recursos",
            questions: [
                {
                    id: "q2_1",
                    text: "1. Como você avaliaria as instalações do hospital (limpeza, conforto, etc.)?",
                    options: ["Muito satisfeito(a)", "Satisfeito(a)", "Neutro(a)", "Insatisfeito(a)", "Muito insatisfeito(a)"]
                },
                {
                    id: "q2_2",
                    text: "2. Os equipamentos e recursos disponíveis no hospital foram suficientes para o seu tratamento?",
                    options: ["Sim", "Não", "Em parte"]
                }
            ]
        },
        {
            title: "Seção 3: Comunicação", 
            questions: [
                {
                    id: "q3_1",
                    text: "1. Você sentiu que os profissionais de saúde explicaram claramente o seu diagnóstico e tratamento?",
                    options: ["Sim", "Não", "Em parte"]
                },
                {
                    id: "q3_2", 
                    text: "2. Você foi informado sobre os seus direitos e responsabilidades como paciente?",
                    options: ["Sim", "Não", "Em parte"]
                }
            ]
        },
        {
            title: "Seção 4: Filantropia e apoio",
            questions: [
                {
                    id: "q4_1",
                    text: "1. Você sabe que o hospital é filantrópico e que sua missão é ajudar aqueles que não têm recursos?",
                    options: ["Sim", "Não"]
                },
                {
                    id: "q4_2",
                    text: "2. Você sente que o hospital está fazendo uma diferença positiva na comunidade?", 
                    options: ["Sim", "Não", "Em parte"]
                }
            ]
        },
        {
            title: "Seção 5: Recomendação",
            questions: [
                {
                    id: "q5_1",
                    text: "1. Você recomendaria este hospital para amigos e familiares?",
                    options: ["Sim", "Não", "Em parte"]
                }
            ]
        }
    ],
    totalQuestions: 10
};

// Sample dashboard data
const DASHBOARD_DATA = {
    totalResponses: 1247,
    averageSatisfaction: 4.2,
    responseRate: 87.3,
    monthlyGrowth: 12.5,
    sectionScores: {
        "Atendimento": 4.3,
        "Instalações": 4.1, 
        "Comunicação": 3.9,
        "Filantropia": 4.6,
        "Recomendação": 4.2
    },
    recentResponses: [
        {id: 1, patient: "Maria S.", date: "2024-12-23", score: 5, section: "Atendimento"},
        {id: 2, patient: "Anônimo", date: "2024-12-23", score: 4, section: "Instalações"},
        {id: 3, patient: "João P.", date: "2024-12-22", score: 3, section: "Comunicação"},
        {id: 4, patient: "Ana L.", date: "2024-12-22", score: 5, section: "Recomendação"},
        {id: 5, patient: "Carlos M.", date: "2024-12-21", score: 4, section: "Filantropia"},
        {id: 6, patient: "Anônimo", date: "2024-12-21", score: 2, section: "Comunicação"},
    ],
    monthlyTrends: [3.8, 4.0, 4.1, 4.0, 4.2, 4.3, 4.2, 4.1, 4.0, 4.1, 4.2, 4.2]
};

// Application state
let surveyResponses = {};
let chartInstances = {};

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupNavigation();
    renderSurveySections();
    setupSurveyEventListeners();
    setupDashboard();
    updateProgress();
}

// Navigation functionality - FIXED
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const views = document.querySelectorAll('.view');
    
    navButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const targetView = this.getAttribute('data-view');
            console.log('Switching to view:', targetView); // Debug log
            
            // Update active nav button
            navButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Switch views
            views.forEach(view => {
                view.classList.remove('active');
                if (view.id === `${targetView}-view`) {
                    view.classList.add('active');
                    console.log('Activated view:', view.id); // Debug log
                }
            });
            
            // Initialize dashboard charts if switching to dashboard
            if (targetView === 'dashboard') {
                console.log('Initializing dashboard charts...'); // Debug log
                setTimeout(() => {
                    initializeDashboardCharts();
                }, 100);
            }
        });
    });
}

// Survey functionality
function renderSurveySections() {
    const sectionsContainer = document.getElementById('survey-sections');
    sectionsContainer.innerHTML = '';
    
    SURVEY_DATA.sections.forEach((section, sectionIndex) => {
        const sectionElement = document.createElement('div');
        sectionElement.className = 'survey-section';
        
        sectionElement.innerHTML = `
            <h3 class="section-title">${section.title}</h3>
            ${section.questions.map(question => `
                <div class="question">
                    <div class="question-text">${question.text}</div>
                    <div class="question-options">
                        ${question.options.map((option, optionIndex) => `
                            <label class="option-label" data-question="${question.id}" data-option="${option}">
                                <input type="radio" name="${question.id}" value="${option}">
                                <div class="radio-button"></div>
                                <span>${option}</span>
                            </label>
                        `).join('')}
                    </div>
                </div>
            `).join('')}
        `;
        
        sectionsContainer.appendChild(sectionElement);
    });
}

function setupSurveyEventListeners() {
    // Anonymous checkbox functionality
    const anonymousCheckbox = document.getElementById('anonymous-checkbox');
    const patientNameInput = document.getElementById('patient-name');
    
    anonymousCheckbox.addEventListener('change', function() {
        if (this.checked) {
            patientNameInput.value = '';
            patientNameInput.disabled = true;
            patientNameInput.placeholder = 'Anônimo';
        } else {
            patientNameInput.disabled = false;
            patientNameInput.placeholder = 'Nome do paciente';
        }
    });
    
    // Question option selection - FIXED to handle radio buttons properly
    document.addEventListener('click', function(e) {
        if (e.target.closest('.option-label')) {
            const label = e.target.closest('.option-label');
            const questionId = label.getAttribute('data-question');
            const option = label.getAttribute('data-option');
            const radioInput = label.querySelector('input[type="radio"]');
            
            // Remove selected class from other options for this question
            document.querySelectorAll(`[data-question="${questionId}"]`).forEach(el => {
                el.classList.remove('selected');
                el.querySelector('input[type="radio"]').checked = false;
            });
            
            // Add selected class to clicked option
            label.classList.add('selected');
            radioInput.checked = true;
            
            // Update survey responses
            surveyResponses[questionId] = option;
            console.log('Updated responses:', surveyResponses); // Debug log
            
            // Update progress
            updateProgress();
        }
    });
    
    // Submit button functionality
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.addEventListener('click', handleSubmit);
}

// FIXED - Updated progress tracking and submit button validation
function updateProgress() {
    const answeredQuestions = Object.keys(surveyResponses).length;
    const totalQuestions = SURVEY_DATA.totalQuestions;
    const percentage = (answeredQuestions / totalQuestions) * 100;
    
    console.log('Progress update:', answeredQuestions, 'of', totalQuestions, 'answered'); // Debug log
    
    // Update progress bar
    const progressBar = document.getElementById('progress-bar');
    progressBar.style.width = `${percentage}%`;
    
    // Update progress text
    const progressText = document.getElementById('progress-text');
    progressText.textContent = `${answeredQuestions}/${totalQuestions} questões respondidas`;
    
    // Update encouraging message
    const progressMessage = document.getElementById('progress-message');
    if (percentage === 100) {
        progressMessage.textContent = "Perfeito! Muito obrigado por concluir a pesquisa ❤️";
    } else if (percentage >= 71) {
        progressMessage.textContent = "Quase lá, obrigado por compartilhar sua experiência ✨";
    } else if (percentage >= 31) {
        progressMessage.textContent = "Você está indo muito bem, continue! 🙏";
    } else {
        progressMessage.textContent = "Estamos começando, sua opinião faz toda a diferença 💙";
    }
    
    // Enable/disable submit button - FIXED validation
    const submitBtn = document.getElementById('submit-btn');
    const allQuestionsAnswered = answeredQuestions === totalQuestions;
    
    if (allQuestionsAnswered) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('btn--disabled');
        console.log('Submit button enabled'); // Debug log
    } else {
        submitBtn.disabled = true;
        submitBtn.classList.add('btn--disabled');
        console.log('Submit button disabled - missing', totalQuestions - answeredQuestions, 'answers'); // Debug log
    }
}

function handleSubmit() {
    const patientName = document.getElementById('patient-name').value;
    const isAnonymous = document.getElementById('anonymous-checkbox').checked;
    const admissionDate = document.getElementById('admission-date').value;
    const dischargeDate = document.getElementById('discharge-date').value;
    const comments = document.getElementById('comments').value;
    
    // Validate required fields
    if (!isAnonymous && !patientName.trim()) {
        alert('Por favor, preencha o nome do paciente ou marque a opção anônimo.');
        return;
    }
    
    if (!admissionDate || !dischargeDate) {
        alert('Por favor, preencha as datas de internação e alta.');
        return;
    }
    
    // FIXED - Double check all questions are answered
    if (Object.keys(surveyResponses).length !== SURVEY_DATA.totalQuestions) {
        alert('Por favor, responda todas as questões antes de enviar.');
        console.log('Validation failed - responses:', Object.keys(surveyResponses).length, 'required:', SURVEY_DATA.totalQuestions);
        return;
    }
    
    // Simulate form submission
    const submitBtn = document.getElementById('submit-btn');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Enviando...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        // Show success message
        showSuccessMessage();
        
        // Reset form
        resetSurvey();
        
        submitBtn.textContent = originalText;
        updateProgress(); // This will properly set the submit button state
    }, 2000);
}

function showSuccessMessage() {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `
        <h3>✅ Pesquisa enviada com sucesso!</h3>
        <p>Muito obrigado por compartilhar sua experiência conosco. Seus comentários são muito valiosos para melhorarmos nossos serviços.</p>
    `;
    
    const surveyContainer = document.querySelector('.survey-container');
    surveyContainer.insertBefore(successDiv, surveyContainer.firstChild);
    
    // Remove success message after 5 seconds
    setTimeout(() => {
        successDiv.remove();
    }, 5000);
}

function resetSurvey() {
    // Reset form fields
    document.getElementById('patient-name').value = '';
    document.getElementById('patient-name').disabled = false;
    document.getElementById('patient-name').placeholder = 'Nome do paciente';
    document.getElementById('anonymous-checkbox').checked = false;
    document.getElementById('admission-date').value = '';
    document.getElementById('discharge-date').value = '';
    document.getElementById('comments').value = '';
    
    // Reset survey responses
    surveyResponses = {};
    
    // Clear selected options and radio buttons
    document.querySelectorAll('.option-label.selected').forEach(label => {
        label.classList.remove('selected');
        const radioInput = label.querySelector('input[type="radio"]');
        if (radioInput) radioInput.checked = false;
    });
    
    // Update progress
    updateProgress();
}

// Dashboard functionality
function setupDashboard() {
    renderRecentResponses();
    setupExportFunctionality();
}

function renderRecentResponses() {
    const tbody = document.getElementById('recent-responses-body');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    DASHBOARD_DATA.recentResponses.forEach(response => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${response.patient}</td>
            <td>${formatDate(response.date)}</td>
            <td>${response.section}</td>
            <td>${response.score}/5</td>
            <td><span class="status ${getStatusClass(response.score)}">${getStatusText(response.score)}</span></td>
        `;
        tbody.appendChild(row);
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

function getStatusClass(score) {
    if (score >= 4) return 'status--success';
    if (score >= 3) return 'status--warning';
    return 'status--error';
}

function getStatusText(score) {
    if (score >= 4) return 'Satisfeito';
    if (score >= 3) return 'Neutro';
    return 'Insatisfeito';
}

function initializeDashboardCharts() {
    // Destroy existing charts
    Object.values(chartInstances).forEach(chart => {
        if (chart) chart.destroy();
    });
    chartInstances = {};
    
    // Create sections chart
    const sectionsCtx = document.getElementById('sections-chart');
    if (sectionsCtx) {
        chartInstances.sections = new Chart(sectionsCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(DASHBOARD_DATA.sectionScores),
                datasets: [{
                    label: 'Pontuação Média',
                    data: Object.values(DASHBOARD_DATA.sectionScores),
                    backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F'],
                    borderColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F'],
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 5,
                        ticks: {
                            stepSize: 0.5
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: false
                    }
                }
            }
        });
    }
    
    // Create trends chart
    const trendsCtx = document.getElementById('trends-chart');
    if (trendsCtx) {
        const months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
        chartInstances.trends = new Chart(trendsCtx, {
            type: 'line',
            data: {
                labels: months,
                datasets: [{
                    label: 'Satisfação Média',
                    data: DASHBOARD_DATA.monthlyTrends,
                    borderColor: '#1FB8CD',
                    backgroundColor: 'rgba(31, 184, 205, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#1FB8CD',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 5,
                        ticks: {
                            stepSize: 0.5
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

function setupExportFunctionality() {
    const exportBtn = document.getElementById('export-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            // Simulate export functionality
            const csvContent = generateCSVReport();
            downloadCSV(csvContent, 'relatorio_satisfacao_pacientes.csv');
        });
    }
}

function generateCSVReport() {
    const headers = ['ID', 'Paciente', 'Data', 'Seção', 'Pontuação', 'Status'];
    const rows = DASHBOARD_DATA.recentResponses.map(response => [
        response.id,
        response.patient,
        response.date,
        response.section,
        response.score,
        getStatusText(response.score)
    ]);
    
    const csvContent = [headers, ...rows]
        .map(row => row.map(field => `"${field}"`).join(','))
        .join('\n');
    
    return csvContent;
}

function downloadCSV(content, filename) {
    const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Handle window resize for charts
window.addEventListener('resize', debounce(() => {
    Object.values(chartInstances).forEach(chart => {
        if (chart) chart.resize();
    });
}, 300));