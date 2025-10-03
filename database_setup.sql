-- Script de criação do banco de dados MySQL
-- Sistema de Pesquisa de Satisfação - Hospital Santa Clara

-- Criar banco de dados
<<<<<<< HEAD

USE hospital_db;
=======
CREATE DATABASE IF NOT EXISTS hospital_satisfaction 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE hospital_satisfaction;
>>>>>>> 19d46c379748bbd568b8fbacd2fd278cd518370a

-- Tabela de pesquisas principais
CREATE TABLE surveys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255) NULL COMMENT 'Nome do paciente (NULL se anônimo)',
    is_anonymous BOOLEAN DEFAULT FALSE COMMENT 'Se a pesquisa é anônima',
    admission_date VARCHAR(50) NOT NULL COMMENT 'Data de internação',
    discharge_date VARCHAR(50) NOT NULL COMMENT 'Data de alta',
    observations TEXT NULL COMMENT 'Observações e comentários',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de criação da pesquisa',
    completed BOOLEAN DEFAULT FALSE COMMENT 'Se a pesquisa foi concluída',
    satisfaction_score DECIMAL(3,2) NULL COMMENT 'Pontuação média de satisfação',

    INDEX idx_created_at (created_at),
    INDEX idx_completed (completed),
    INDEX idx_satisfaction_score (satisfaction_score)
) COMMENT = 'Pesquisas de satisfação dos pacientes';

-- Tabela de perguntas do questionário
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id VARCHAR(10) UNIQUE NOT NULL COMMENT 'ID da pergunta (q1_1, q1_2, etc)',
    section_title VARCHAR(255) NOT NULL COMMENT 'Título da seção',
    question_text TEXT NOT NULL COMMENT 'Texto da pergunta',
    question_type VARCHAR(50) NOT NULL COMMENT 'Tipo da pergunta (satisfaction_scale, yes_no_partial, yes_no)',
    section_order INT NOT NULL COMMENT 'Ordem da seção',
    question_order INT NOT NULL COMMENT 'Ordem da pergunta na seção',

    INDEX idx_question_id (question_id),
    INDEX idx_section_order (section_order, question_order)
) COMMENT = 'Perguntas do questionário de satisfação';

-- Tabela de opções de resposta para cada pergunta
CREATE TABLE question_options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_text VARCHAR(255) NOT NULL COMMENT 'Texto da opção',
    option_value INT NOT NULL COMMENT 'Valor numérico para cálculos',
    option_order INT NOT NULL COMMENT 'Ordem da opção',

    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    INDEX idx_question_id (question_id),
    INDEX idx_option_order (option_order)
) COMMENT = 'Opções de resposta para cada pergunta';

-- Tabela de respostas individuais
CREATE TABLE survey_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    survey_id INT NOT NULL,
    question_id INT NOT NULL,
    response_value VARCHAR(255) NOT NULL COMMENT 'Resposta textual',
    response_score INT NULL COMMENT 'Pontuação numérica da resposta',

    FOREIGN KEY (survey_id) REFERENCES surveys(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    INDEX idx_survey_id (survey_id),
    INDEX idx_question_id (question_id),
    INDEX idx_response_score (response_score),

    UNIQUE KEY unique_survey_question (survey_id, question_id)
) COMMENT = 'Respostas individuais para cada pergunta da pesquisa';

-- Inserir perguntas padrão do questionário
INSERT INTO questions (question_id, section_title, question_text, question_type, section_order, question_order) VALUES
-- Seção 1: Atendimento
('q1_1', 'Seção 1: Atendimento', '1. Como você avaliaria a qualidade do atendimento recebido no hospital?', 'satisfaction_scale', 1, 1),
('q1_2', 'Seção 1: Atendimento', '2. Os profissionais de saúde foram atenciosos e respeitosos com você?', 'yes_no_partial', 1, 2),
('q1_3', 'Seção 1: Atendimento', '3. Você sentiu que suas necessidades foram atendidas de forma eficaz?', 'yes_no_partial', 1, 3),

-- Seção 2: Instalações e recursos
('q2_1', 'Seção 2: Instalações e recursos', '1. Como você avaliaria as instalações do hospital (limpeza, conforto, etc.)?', 'satisfaction_scale', 2, 1),
('q2_2', 'Seção 2: Instalações e recursos', '2. Os equipamentos e recursos disponíveis no hospital foram suficientes para o seu tratamento?', 'yes_no_partial', 2, 2),

-- Seção 3: Comunicação
('q3_1', 'Seção 3: Comunicação', '1. Você sentiu que os profissionais de saúde explicaram claramente o seu diagnóstico e tratamento?', 'yes_no_partial', 3, 1),
('q3_2', 'Seção 3: Comunicação', '2. Você foi informado sobre os seus direitos e responsabilidades como paciente?', 'yes_no_partial', 3, 2),

-- Seção 4: Filantropia e apoio
('q4_1', 'Seção 4: Filantropia e apoio', '1. Você sabe que o hospital é filantrópico e que sua missão é ajudar aqueles que não têm recursos?', 'yes_no', 4, 1),
('q4_2', 'Seção 4: Filantropia e apoio', '2. Você sente que o hospital está fazendo uma diferença positiva na comunidade?', 'yes_no_partial', 4, 2),

-- Seção 5: Recomendação
('q5_1', 'Seção 5: Recomendação', '1. Você recomendaria este hospital para amigos e familiares?', 'yes_no_partial', 5, 1);

-- Inserir opções de resposta para as perguntas
-- Perguntas de escala de satisfação (q1_1, q2_1)
INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Muito satisfeito(a)', 5, 1 FROM questions q WHERE q.question_id IN ('q1_1', 'q2_1');

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Satisfeito(a)', 4, 2 FROM questions q WHERE q.question_id IN ('q1_1', 'q2_1');

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Neutro(a)', 3, 3 FROM questions q WHERE q.question_id IN ('q1_1', 'q2_1');

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Insatisfeito(a)', 2, 4 FROM questions q WHERE q.question_id IN ('q1_1', 'q2_1');

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Muito insatisfeito(a)', 1, 5 FROM questions q WHERE q.question_id IN ('q1_1', 'q2_1');

-- Perguntas Sim/Não/Em parte (q1_2, q1_3, q2_2, q3_1, q3_2, q4_2, q5_1)
INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Sim', 5, 1 FROM questions q WHERE q.question_id IN ('q1_2', 'q1_3', 'q2_2', 'q3_1', 'q3_2', 'q4_2', 'q5_1');

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Não', 1, 2 FROM questions q WHERE q.question_id IN ('q1_2', 'q1_3', 'q2_2', 'q3_1', 'q3_2', 'q4_2', 'q5_1');

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Em parte', 3, 3 FROM questions q WHERE q.question_id IN ('q1_2', 'q1_3', 'q2_2', 'q3_1', 'q3_2', 'q4_2', 'q5_1');

-- Pergunta apenas Sim/Não (q4_1)
INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Sim', 5, 1 FROM questions q WHERE q.question_id = 'q4_1';

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Não', 1, 2 FROM questions q WHERE q.question_id = 'q4_1';

-- Criar views para facilitar consultas analíticas

-- View de satisfação por seção
CREATE VIEW satisfaction_by_section AS
SELECT 
    q.section_title,
    AVG(sr.response_score) as avg_satisfaction,
    COUNT(sr.id) as total_responses,
    COUNT(DISTINCT sr.survey_id) as unique_surveys
FROM questions q
JOIN survey_responses sr ON q.id = sr.question_id
WHERE sr.response_score IS NOT NULL
GROUP BY q.section_title
ORDER BY avg_satisfaction DESC;

-- View de tendência mensal
CREATE VIEW monthly_satisfaction AS
SELECT 
    DATE_FORMAT(s.created_at, '%Y-%m') as month,
    AVG(s.satisfaction_score) as avg_satisfaction,
    COUNT(s.id) as survey_count
FROM surveys s
WHERE s.completed = TRUE AND s.satisfaction_score IS NOT NULL
GROUP BY DATE_FORMAT(s.created_at, '%Y-%m')
ORDER BY month;

-- View de detalhes completos das pesquisas
CREATE VIEW survey_details AS
SELECT 
    s.id,
    s.patient_name,
    s.is_anonymous,
    s.admission_date,
    s.discharge_date,
    s.observations,
    s.created_at,
    s.satisfaction_score,
    COUNT(sr.id) as total_responses
FROM surveys s
LEFT JOIN survey_responses sr ON s.id = sr.survey_id
WHERE s.completed = TRUE
GROUP BY s.id, s.patient_name, s.is_anonymous, s.admission_date, 
         s.discharge_date, s.observations, s.created_at, s.satisfaction_score
ORDER BY s.created_at DESC;

-- Inserir dados de exemplo para demonstração
INSERT INTO surveys (patient_name, is_anonymous, admission_date, discharge_date, observations, completed, satisfaction_score, created_at) VALUES
('Maria Silva', FALSE, '2025-09-20', '2025-09-22', 'Excelente atendimento da equipe de enfermagem!', TRUE, 4.8, '2025-09-23 10:30:00'),
(NULL, TRUE, '2025-09-19', '2025-09-21', '', TRUE, 3.2, '2025-09-23 14:15:00'),
('João Pereira', FALSE, '2025-09-18', '2025-09-20', 'Poderiam melhorar a comunicação sobre os procedimentos.', TRUE, 3.8, '2025-09-22 16:45:00'),
(NULL, TRUE, '2025-09-17', '2025-09-19', 'Hospital muito limpo e organizado.', TRUE, 4.5, '2025-09-22 09:20:00'),
('Ana Costa', FALSE, '2025-09-16', '2025-09-18', '', TRUE, 4.2, '2025-09-21 11:10:00');

COMMIT;

-- Criar usuário específico para a aplicação (opcional)
-- CREATE USER 'hospital_app'@'localhost' IDENTIFIED BY 'secure_password_2025';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON hospital_satisfaction.* TO 'hospital_app'@'localhost';
-- FLUSH PRIVILEGES;

SELECT 'Banco de dados criado com sucesso!' as status;
