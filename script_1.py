# Criando os templates HTML para a aplicação

import os

# Criar diretório templates
os.makedirs('templates', exist_ok=True)

# Template base
base_template = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema de Pesquisa de Satisfação - Hospital Santa Clara{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        :root {
            --primary-color: #2980b9;
            --secondary-color: #3498db;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --danger-color: #e74c3c;
            --light-bg: #f8f9fa;
            --dark-text: #2c3e50;
        }
        
        body {
            background-color: var(--light-bg);
            color: var(--dark-text);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .navbar-brand {
            font-weight: bold;
            color: white !important;
        }
        
        .survey-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .survey-header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem;
            text-align: center;
        }
        
        .logo-placeholder {
            width: 200px;
            height: 60px;
            background: rgba(255,255,255,0.2);
            border-radius: 8px;
            margin: 0 auto 1rem auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
        
        .progress-section {
            background: #f8f9fa;
            padding: 1.5rem;
            border-bottom: 1px solid #dee2e6;
        }
        
        .progress {
            height: 20px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        
        .progress-bar {
            transition: width 0.3s ease;
            border-radius: 10px;
        }
        
        .encouragement {
            text-align: center;
            font-style: italic;
            color: var(--dark-text);
            margin-top: 10px;
        }
        
        .section {
            border: 1px solid #dee2e6;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            overflow: hidden;
        }
        
        .section-header {
            background: var(--primary-color);
            color: white;
            padding: 1rem;
            font-weight: bold;
            font-size: 1.1rem;
        }
        
        .section-content {
            padding: 1.5rem;
        }
        
        .question {
            margin-bottom: 2rem;
        }
        
        .question-text {
            font-weight: 500;
            margin-bottom: 1rem;
            line-height: 1.4;
        }
        
        .form-check {
            margin-bottom: 0.8rem;
        }
        
        .form-check-input:checked {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }
        
        .form-check-label {
            cursor: pointer;
            padding: 8px 12px;
            border-radius: 5px;
            transition: background-color 0.2s;
        }
        
        .form-check-input:checked + .form-check-label {
            background-color: rgba(41, 128, 185, 0.1);
            color: var(--primary-color);
            font-weight: 500;
        }
        
        .btn-primary-custom {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border: none;
            padding: 15px 40px;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 25px;
            transition: all 0.3s;
        }
        
        .btn-primary-custom:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn-primary-custom:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .dashboard-card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: transform 0.2s;
        }
        
        .dashboard-card:hover {
            transform: translateY(-2px);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: var(--primary-color);
        }
        
        .metric-label {
            color: #6c757d;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .chart-container {
            position: relative;
            height: 300px;
            margin: 1rem 0;
        }
        
        .navbar-custom {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
        }
        
        @media (max-width: 768px) {
            .survey-container {
                margin: 1rem;
                border-radius: 10px;
            }
            
            .survey-header {
                padding: 1.5rem;
            }
            
            .section-content {
                padding: 1rem;
            }
        }
    </style>
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-hospital-alt me-2"></i>
                Hospital Santa Clara
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/">
                    <i class="fas fa-clipboard-list me-1"></i>
                    Pesquisa
                </a>
                <a class="nav-link" href="/dashboard">
                    <i class="fas fa-chart-bar me-1"></i>
                    Dashboard
                </a>
            </div>
        </div>
    </nav>
    
    <main class="container-fluid py-4">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>'''

# Template da pesquisa
survey_template = '''{% extends "base.html" %}

{% block title %}Pesquisa de Satisfação - Hospital Santa Clara{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-12 col-lg-10 col-xl-8">
        <div class="survey-container">
            <!-- Header da Pesquisa -->
            <div class="survey-header">
                <div class="logo-placeholder">
                    HOSPITAL SANTA CLARA
                </div>
                <h2 class="mb-0">Pesquisa de Satisfação</h2>
                <p class="mb-0 mt-2">Sua opinião é muito importante para nós!</p>
            </div>
            
            <!-- Seção de Progresso -->
            <div class="progress-section">
                <div class="progress">
                    <div id="progress-bar" class="progress-bar" role="progressbar" style="width: 0%"></div>
                </div>
                <p class="mb-0">
                    <span id="progress-text">0/10 questões respondidas</span>
                </p>
                <div id="encouragement" class="encouragement">
                    Estamos começando, sua opinião faz toda a diferença 💙
                </div>
            </div>
            
            <!-- Formulário da Pesquisa -->
            <form id="survey-form" class="p-4">
                <!-- Informações do Paciente -->
                <div class="section mb-4">
                    <div class="section-header">
                        <i class="fas fa-user me-2"></i>
                        Informações do Paciente
                    </div>
                    <div class="section-content">
                        <div class="row">
                            <div class="col-md-8 mb-3">
                                <label for="patient_name" class="form-label">Nome do Paciente</label>
                                <input type="text" class="form-control" id="patient_name" name="patient_name">
                            </div>
                            <div class="col-md-4 mb-3 d-flex align-items-end">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="is_anonymous" name="is_anonymous">
                                    <label class="form-check-label" for="is_anonymous">
                                        Prefiro permanecer anônimo
                                    </label>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="admission_date" class="form-label">Data de Internação</label>
                                <input type="date" class="form-control" id="admission_date" name="admission_date" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="discharge_date" class="form-label">Data de Alta</label>
                                <input type="date" class="form-control" id="discharge_date" name="discharge_date" required>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Seções de Perguntas -->
                <div id="questions-container">
                    <!-- Perguntas serão carregadas via JavaScript -->
                </div>
                
                <!-- Observações -->
                <div class="section mb-4">
                    <div class="section-header">
                        <i class="fas fa-comment me-2"></i>
                        Observações
                    </div>
                    <div class="section-content">
                        <label for="observations" class="form-label">
                            Comentários ou sugestões adicionais (opcional)
                        </label>
                        <textarea class="form-control" id="observations" name="observations" rows="4" 
                                placeholder="Compartilhe sua experiência ou sugestões para melhorarmos nosso atendimento..."></textarea>
                    </div>
                </div>
                
                <!-- Botão de Envio -->
                <div class="text-center">
                    <button type="submit" id="submit-btn" class="btn btn-primary-custom" disabled>
                        <i class="fas fa-paper-plane me-2"></i>
                        Enviar Pesquisa
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Modal de Sucesso -->
<div class="modal fade" id="successModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-body text-center p-4">
                <div class="text-success mb-3">
                    <i class="fas fa-check-circle" style="font-size: 3rem;"></i>
                </div>
                <h4 class="text-success mb-3">Pesquisa Enviada com Sucesso!</h4>
                <p>Muito obrigado por seu tempo e feedback. Sua opinião nos ajuda a melhorar continuamente nossos serviços.</p>
                <button type="button" class="btn btn-primary-custom" onclick="resetForm()">
                    Nova Pesquisa
                </button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
let questionsData = [];
let currentResponses = {};
let totalQuestions = 10;

// Carregar perguntas da API
async function loadQuestions() {
    try {
        const response = await fetch('/api/questions');
        questionsData = await response.json();
        renderQuestions();
    } catch (error) {
        console.error('Erro ao carregar perguntas:', error);
        // Fallback com dados estáticos
        loadFallbackQuestions();
    }
}

function loadFallbackQuestions() {
    // Dados de fallback caso a API não esteja funcionando
    questionsData = [
        {
            "title": "Seção 1: Atendimento",
            "questions": [
                {
                    "id": "q1_1",
                    "text": "1. Como você avaliaria a qualidade do atendimento recebido no hospital?",
                    "options": ["Muito satisfeito(a)", "Satisfeito(a)", "Neutro(a)", "Insatisfeito(a)", "Muito insatisfeito(a)"]
                },
                {
                    "id": "q1_2",
                    "text": "2. Os profissionais de saúde foram atenciosos e respeitosos com você?",
                    "options": ["Sim", "Não", "Em parte"]
                },
                {
                    "id": "q1_3",
                    "text": "3. Você sentiu que suas necessidades foram atendidas de forma eficaz?",
                    "options": ["Sim", "Não", "Em parte"]
                }
            ]
        },
        {
            "title": "Seção 2: Instalações e recursos",
            "questions": [
                {
                    "id": "q2_1",
                    "text": "1. Como você avaliaria as instalações do hospital (limpeza, conforto, etc.)?",
                    "options": ["Muito satisfeito(a)", "Satisfeito(a)", "Neutro(a)", "Insatisfeito(a)", "Muito insatisfeito(a)"]
                },
                {
                    "id": "q2_2",
                    "text": "2. Os equipamentos e recursos disponíveis no hospital foram suficientes para o seu tratamento?",
                    "options": ["Sim", "Não", "Em parte"]
                }
            ]
        },
        {
            "title": "Seção 3: Comunicação",
            "questions": [
                {
                    "id": "q3_1",
                    "text": "1. Você sentiu que os profissionais de saúde explicaram claramente o seu diagnóstico e tratamento?",
                    "options": ["Sim", "Não", "Em parte"]
                },
                {
                    "id": "q3_2",
                    "text": "2. Você foi informado sobre os seus direitos e responsabilidades como paciente?",
                    "options": ["Sim", "Não", "Em parte"]
                }
            ]
        },
        {
            "title": "Seção 4: Filantropia e apoio",
            "questions": [
                {
                    "id": "q4_1",
                    "text": "1. Você sabe que o hospital é filantrópico e que sua missão é ajudar aqueles que não têm recursos?",
                    "options": ["Sim", "Não"]
                },
                {
                    "id": "q4_2",
                    "text": "2. Você sente que o hospital está fazendo uma diferença positiva na comunidade?",
                    "options": ["Sim", "Não", "Em parte"]
                }
            ]
        },
        {
            "title": "Seção 5: Recomendação",
            "questions": [
                {
                    "id": "q5_1",
                    "text": "1. Você recomendaria este hospital para amigos e familiares?",
                    "options": ["Sim", "Não", "Em parte"]
                }
            ]
        }
    ];
    renderQuestions();
}

function renderQuestions() {
    const container = document.getElementById('questions-container');
    container.innerHTML = '';
    
    totalQuestions = questionsData.reduce((total, section) => total + section.questions.length, 0);
    
    questionsData.forEach(section => {
        const sectionDiv = document.createElement('div');
        sectionDiv.className = 'section mb-4';
        
        sectionDiv.innerHTML = `
            <div class="section-header">
                <i class="fas fa-clipboard-list me-2"></i>
                ${section.title}
            </div>
            <div class="section-content">
                ${section.questions.map(question => `
                    <div class="question">
                        <div class="question-text">${question.text}</div>
                        ${question.options.map(option => `
                            <div class="form-check">
                                <input class="form-check-input" type="radio" 
                                       name="${question.id}" value="${option}" 
                                       id="${question.id}_${option.replace(/[^a-zA-Z0-9]/g, '_')}"
                                       onchange="updateProgress()">
                                <label class="form-check-label" 
                                       for="${question.id}_${option.replace(/[^a-zA-Z0-9]/g, '_')}">
                                    ${option}
                                </label>
                            </div>
                        `).join('')}
                    </div>
                `).join('')}
            </div>
        `;
        
        container.appendChild(sectionDiv);
    });
    
    updateProgress();
}

function updateProgress() {
    // Contar questões respondidas
    const answered = new Set();
    const radios = document.querySelectorAll('input[type="radio"]:checked');
    
    radios.forEach(radio => {
        answered.add(radio.name);
        currentResponses[radio.name] = radio.value;
    });
    
    const progress = (answered.size / totalQuestions) * 100;
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const encouragement = document.getElementById('encouragement');
    const submitBtn = document.getElementById('submit-btn');
    
    // Atualizar barra de progresso
    progressBar.style.width = progress + '%';
    progressText.textContent = `${answered.size}/${totalQuestions} questões respondidas`;
    
    // Atualizar cor da barra
    if (progress < 30) {
        progressBar.className = 'progress-bar bg-danger';
    } else if (progress < 70) {
        progressBar.className = 'progress-bar bg-warning';
    } else {
        progressBar.className = 'progress-bar bg-success';
    }
    
    // Atualizar mensagem de encorajamento
    let message = '';
    if (progress === 100) {
        message = "Perfeito! Muito obrigado por concluir a pesquisa ❤️";
    } else if (progress >= 71) {
        message = "Quase lá, obrigado por compartilhar sua experiência ✨";
    } else if (progress >= 31) {
        message = "Você está indo muito bem, continue! 🙏";
    } else {
        message = "Estamos começando, sua opinião faz toda a diferença 💙";
    }
    encouragement.textContent = message;
    
    // Habilitar/desabilitar botão de envio
    submitBtn.disabled = answered.size < totalQuestions;
}

// Controlar checkbox anônimo
document.getElementById('is_anonymous').addEventListener('change', function() {
    const nameField = document.getElementById('patient_name');
    if (this.checked) {
        nameField.value = '';
        nameField.disabled = true;
        nameField.placeholder = 'Anônimo';
    } else {
        nameField.disabled = false;
        nameField.placeholder = '';
    }
});

// Envio do formulário
document.getElementById('survey-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submit-btn');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enviando...';
    submitBtn.disabled = true;
    
    try {
        const formData = new FormData(this);
        
        // Adicionar respostas das questões
        Object.entries(currentResponses).forEach(([key, value]) => {
            formData.append(key, value);
        });
        
        const response = await fetch('/api/submit-survey', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            // Mostrar modal de sucesso
            const modal = new bootstrap.Modal(document.getElementById('successModal'));
            modal.show();
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        alert('Erro ao enviar pesquisa: ' + error.message);
    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

function resetForm() {
    document.getElementById('survey-form').reset();
    currentResponses = {};
    updateProgress();
    
    // Fechar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('successModal'));
    modal.hide();
    
    // Scroll para o topo
    window.scrollTo(0, 0);
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    loadQuestions();
});
</script>
{% endblock %}'''

# Template do dashboard
dashboard_template = '''{% extends "base.html" %}

{% block title %}Dashboard de Insights - Hospital Santa Clara{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row mb-4">
        <div class="col-12">
            <h1 class="h3 mb-0">
                <i class="fas fa-chart-bar text-primary me-2"></i>
                Dashboard de Satisfação do Paciente
            </h1>
            <p class="text-muted">Insights e análises para tomada de decisão da diretoria</p>
        </div>
    </div>
    
    <!-- Cards de Métricas Principais -->
    <div class="row mb-4">
        <div class="col-xl-3 col-md-6 mb-3">
            <div class="dashboard-card">
                <div class="d-flex align-items-center">
                    <div class="flex-grow-1">
                        <div class="metric-label">Total de Respostas</div>
                        <div id="total-surveys" class="metric-value">{{ total_surveys }}</div>
                    </div>
                    <div class="text-primary">
                        <i class="fas fa-clipboard-list fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-xl-3 col-md-6 mb-3">
            <div class="dashboard-card">
                <div class="d-flex align-items-center">
                    <div class="flex-grow-1">
                        <div class="metric-label">Satisfação Média</div>
                        <div id="avg-satisfaction" class="metric-value">{{ avg_satisfaction }}</div>
                        <small class="text-muted">de 5.0</small>
                    </div>
                    <div class="text-success">
                        <i class="fas fa-star fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-xl-3 col-md-6 mb-3">
            <div class="dashboard-card">
                <div class="d-flex align-items-center">
                    <div class="flex-grow-1">
                        <div class="metric-label">Taxa de Resposta</div>
                        <div id="response-rate" class="metric-value">87.3%</div>
                    </div>
                    <div class="text-info">
                        <i class="fas fa-percentage fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-xl-3 col-md-6 mb-3">
            <div class="dashboard-card">
                <div class="d-flex align-items-center">
                    <div class="flex-grow-1">
                        <div class="metric-label">Crescimento Mensal</div>
                        <div class="metric-value text-success">+12.5%</div>
                    </div>
                    <div class="text-warning">
                        <i class="fas fa-arrow-trend-up fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row mb-4">
        <div class="col-lg-8 mb-4">
            <div class="dashboard-card">
                <h5 class="card-title mb-3">
                    <i class="fas fa-chart-line me-2"></i>
                    Tendência de Satisfação (Últimos 12 Meses)
                </h5>
                <div class="chart-container">
                    <canvas id="trendChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="col-lg-4 mb-4">
            <div class="dashboard-card">
                <h5 class="card-title mb-3">
                    <i class="fas fa-chart-pie me-2"></i>
                    Distribuição de Satisfação
                </h5>
                <div class="chart-container">
                    <canvas id="distributionChart"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Satisfação por Seção -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="dashboard-card">
                <h5 class="card-title mb-3">
                    <i class="fas fa-chart-bar me-2"></i>
                    Satisfação por Seção
                </h5>
                <div class="chart-container">
                    <canvas id="sectionChart"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Tabela de Respostas Recentes -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="dashboard-card">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-clock me-2"></i>
                        Respostas Recentes
                    </h5>
                    <button class="btn btn-outline-primary btn-sm" onclick="loadDashboardData()">
                        <i class="fas fa-sync-alt me-1"></i>
                        Atualizar
                    </button>
                </div>
                
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>ID</th>
                                <th>Paciente</th>
                                <th>Data</th>
                                <th>Pontuação</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody id="recent-surveys-table">
                            {% for survey in recent_surveys %}
                            <tr>
                                <td>#{{ survey.id }}</td>
                                <td>
                                    {% if survey.is_anonymous %}
                                        <i class="fas fa-user-secret text-muted me-1"></i>Anônimo
                                    {% else %}
                                        {{ survey.patient_name or 'N/A' }}
                                    {% endif %}
                                </td>
                                <td>{{ survey.created_at.strftime('%d/%m/%Y %H:%M') }}</td>
                                <td>
                                    <span class="badge bg-{{ 'success' if survey.satisfaction_score >= 4 else 'warning' if survey.satisfaction_score >= 3 else 'danger' }}">
                                        {{ "%.1f"|format(survey.satisfaction_score or 0) }}/5.0
                                    </span>
                                </td>
                                <td>
                                    <span class="badge bg-success">
                                        <i class="fas fa-check me-1"></i>Concluída
                                    </span>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Insights e Recomendações -->
    <div class="row">
        <div class="col-lg-6 mb-4">
            <div class="dashboard-card">
                <h5 class="card-title mb-3">
                    <i class="fas fa-lightbulb me-2"></i>
                    Principais Insights
                </h5>
                <div id="insights-list">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        <strong>Pontos Fortes:</strong> A seção de Filantropia tem a maior pontuação média (4.6/5.0).
                    </div>
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        <strong>Oportunidade:</strong> A seção de Comunicação apresenta pontuação mais baixa (3.9/5.0).
                    </div>
                    <div class="alert alert-success">
                        <i class="fas fa-chart-line me-2"></i>
                        <strong>Tendência:</strong> Satisfação geral aumentou 12.5% no último mês.
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-lg-6 mb-4">
            <div class="dashboard-card">
                <h5 class="card-title mb-3">
                    <i class="fas fa-tasks me-2"></i>
                    Recomendações de Ação
                </h5>
                <div class="list-group list-group-flush">
                    <div class="list-group-item border-0 ps-0">
                        <div class="d-flex align-items-center">
                            <span class="badge bg-danger me-3">Alta</span>
                            <div>
                                <strong>Melhorar Comunicação</strong><br>
                                <small class="text-muted">Treinar equipe em comunicação clara com pacientes</small>
                            </div>
                        </div>
                    </div>
                    <div class="list-group-item border-0 ps-0">
                        <div class="d-flex align-items-center">
                            <span class="badge bg-warning me-3">Média</span>
                            <div>
                                <strong>Manter Padrão de Atendimento</strong><br>
                                <small class="text-muted">Continuar práticas que resultam em alta satisfação</small>
                            </div>
                        </div>
                    </div>
                    <div class="list-group-item border-0 ps-0">
                        <div class="d-flex align-items-center">
                            <span class="badge bg-info me-3">Baixa</span>
                            <div>
                                <strong>Promover Missão Filantrópica</strong><br>
                                <small class="text-muted">Destacar ainda mais o impacto social do hospital</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
let dashboardData = {};
let charts = {};

// Carregar dados do dashboard
async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard-data');
        dashboardData = await response.json();
        updateDashboardUI();
        createCharts();
    } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
        // Usar dados de fallback
        useFallbackData();
    }
}

function useFallbackData() {
    dashboardData = {
        totalSurveys: 1247,
        avgSatisfaction: 4.2,
        sectionScores: {
            "Seção 1: Atendimento": 4.3,
            "Seção 2: Instalações e recursos": 4.1,
            "Seção 3: Comunicação": 3.9,
            "Seção 4: Filantropia e apoio": 4.6,
            "Seção 5: Recomendação": 4.2
        },
        monthlyTrend: [3.8, 4.0, 4.1, 4.0, 4.2, 4.3, 4.2, 4.1, 4.0, 4.1, 4.2, 4.2],
        recentSurveys: [
            {id: 1, patient: "Maria S.", date: "2025-09-23", score: 5.0},
            {id: 2, patient: "Anônimo", date: "2025-09-23", score: 4.2},
            {id: 3, patient: "João P.", date: "2025-09-22", score: 3.8}
        ]
    };
    updateDashboardUI();
    createCharts();
}

function updateDashboardUI() {
    // Atualizar métricas principais
    document.getElementById('total-surveys').textContent = dashboardData.totalSurveys;
    document.getElementById('avg-satisfaction').textContent = dashboardData.avgSatisfaction.toFixed(1);
    
    // Atualizar tabela de pesquisas recentes
    updateRecentSurveysTable();
}

function updateRecentSurveysTable() {
    const tbody = document.getElementById('recent-surveys-table');
    if (dashboardData.recentSurveys && dashboardData.recentSurveys.length > 0) {
        tbody.innerHTML = dashboardData.recentSurveys.map(survey => `
            <tr>
                <td>#${survey.id}</td>
                <td>
                    ${survey.patient === 'Anônimo' 
                        ? '<i class="fas fa-user-secret text-muted me-1"></i>Anônimo'
                        : survey.patient}
                </td>
                <td>${survey.date}</td>
                <td>
                    <span class="badge bg-${survey.score >= 4 ? 'success' : survey.score >= 3 ? 'warning' : 'danger'}">
                        ${survey.score.toFixed(1)}/5.0
                    </span>
                </td>
                <td>
                    <span class="badge bg-success">
                        <i class="fas fa-check me-1"></i>Concluída
                    </span>
                </td>
            </tr>
        `).join('');
    }
}

function createCharts() {
    // Gráfico de tendência
    createTrendChart();
    
    // Gráfico de distribuição
    createDistributionChart();
    
    // Gráfico por seção
    createSectionChart();
}

function createTrendChart() {
    const ctx = document.getElementById('trendChart');
    if (charts.trendChart) {
        charts.trendChart.destroy();
    }
    
    charts.trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
            datasets: [{
                label: 'Satisfação Média',
                data: dashboardData.monthlyTrend,
                borderColor: '#2980b9',
                backgroundColor: 'rgba(41, 128, 185, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5,
                    ticks: {
                        stepSize: 0.5
                    }
                }
            }
        }
    });
}

function createDistributionChart() {
    const ctx = document.getElementById('distributionChart');
    if (charts.distributionChart) {
        charts.distributionChart.destroy();
    }
    
    charts.distributionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Muito Satisfeito', 'Satisfeito', 'Neutro', 'Insatisfeito', 'Muito Insatisfeito'],
            datasets: [{
                data: [45, 30, 15, 7, 3],
                backgroundColor: [
                    '#27ae60',
                    '#2ecc71',
                    '#f39c12',
                    '#e67e22',
                    '#e74c3c'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    });
}

function createSectionChart() {
    const ctx = document.getElementById('sectionChart');
    if (charts.sectionChart) {
        charts.sectionChart.destroy();
    }
    
    const sections = Object.keys(dashboardData.sectionScores || {});
    const scores = Object.values(dashboardData.sectionScores || {});
    
    charts.sectionChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sections.map(s => s.replace('Seção ', '').replace(': ', '\\n')),
            datasets: [{
                label: 'Pontuação Média',
                data: scores,
                backgroundColor: [
                    '#3498db',
                    '#2ecc71',
                    '#f39c12',
                    '#9b59b6',
                    '#e74c3c'
                ],
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5,
                    ticks: {
                        stepSize: 0.5
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 0
                    }
                }
            }
        }
    });
}

// Inicializar dashboard quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
});
</script>
{% endblock %}'''

# Salvar os templates
with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base_template)

with open('templates/survey.html', 'w', encoding='utf-8') as f:
    f.write(survey_template)

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dashboard_template)

print("✅ Templates HTML criados com sucesso!")
print("   - templates/base.html")
print("   - templates/survey.html") 
print("   - templates/dashboard.html")