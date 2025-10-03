# Criando a estrutura completa da aplicação FastAPI para pesquisa de satisfação hospitalar

# Primeiro, vou criar o arquivo principal com toda a estrutura

main_py_content = '''
"""
Sistema de Pesquisa de Satisfação - Hospital Santa Clara
Aplicação FastAPI completa com MySQL, templates HTML e dashboard de insights
"""

from datetime import datetime, date
from typing import Optional, List
import json
import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
import uvicorn
from contextlib import asynccontextmanager


# ====== CONFIGURAÇÕES DE BANCO DE DADOS ======

DATABASE_URL = "mysql+pymysql://user:password@localhost/hospital_satisfaction"
# Para desenvolvimento local com SQLite:
# DATABASE_URL = "sqlite:///./hospital_satisfaction.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ====== MODELOS DO BANCO DE DADOS ======

class Survey(Base):
    """Tabela principal das pesquisas"""
    __tablename__ = "surveys"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(255), nullable=True)  # Pode ser nulo se anônimo
    is_anonymous = Column(Boolean, default=False)
    admission_date = Column(String(50))
    discharge_date = Column(String(50))
    observations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
    satisfaction_score = Column(Float, nullable=True)  # Score médio calculado
    
    # Relacionamentos
    responses = relationship("SurveyResponse", back_populates="survey")


class Question(Base):
    """Tabela de perguntas do questionário"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(String(10), unique=True, index=True)  # q1_1, q1_2, etc
    section_title = Column(String(255))
    question_text = Column(Text)
    question_type = Column(String(50))  # satisfaction_scale, yes_no_partial
    section_order = Column(Integer)
    question_order = Column(Integer)
    
    # Relacionamentos
    responses = relationship("SurveyResponse", back_populates="question")
    options = relationship("QuestionOption", back_populates="question")


class QuestionOption(Base):
    """Opções de resposta para cada pergunta"""
    __tablename__ = "question_options"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    option_text = Column(String(255))
    option_value = Column(Integer)  # Valor numérico para cálculos
    option_order = Column(Integer)
    
    # Relacionamentos
    question = relationship("Question", back_populates="options")


class SurveyResponse(Base):
    """Respostas individuais para cada pergunta"""
    __tablename__ = "survey_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    response_value = Column(String(255))  # Resposta textual
    response_score = Column(Integer, nullable=True)  # Score numérico
    
    # Relacionamentos
    survey = relationship("Survey", back_populates="responses")
    question = relationship("Question", back_populates="responses")


# ====== MODELOS PYDANTIC ======

class SurveyCreate(BaseModel):
    patient_name: Optional[str] = None
    is_anonymous: bool = False
    admission_date: str
    discharge_date: str
    responses: dict
    observations: Optional[str] = None


class SurveyResponse(BaseModel):
    id: int
    patient_name: Optional[str]
    is_anonymous: bool
    admission_date: str
    discharge_date: str
    created_at: datetime
    satisfaction_score: Optional[float]
    
    class Config:
        from_attributes = True


# ====== DEPENDÊNCIAS ======

def get_db():
    """Dependência para obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ====== INICIALIZAÇÃO DOS DADOS ======

def init_questions(db: Session):
    """Inicializa as perguntas no banco de dados"""
    
    # Verifica se já existem perguntas
    if db.query(Question).count() > 0:
        return
    
    sections_data = [
        {
            "title": "Seção 1: Atendimento",
            "questions": [
                {
                    "id": "q1_1",
                    "text": "1. Como você avaliaria a qualidade do atendimento recebido no hospital?",
                    "options": [
                        ("Muito satisfeito(a)", 5),
                        ("Satisfeito(a)", 4),
                        ("Neutro(a)", 3),
                        ("Insatisfeito(a)", 2),
                        ("Muito insatisfeito(a)", 1)
                    ],
                    "type": "satisfaction_scale"
                },
                {
                    "id": "q1_2",
                    "text": "2. Os profissionais de saúde foram atenciosos e respeitosos com você?",
                    "options": [("Sim", 5), ("Não", 1), ("Em parte", 3)],
                    "type": "yes_no_partial"
                },
                {
                    "id": "q1_3",
                    "text": "3. Você sentiu que suas necessidades foram atendidas de forma eficaz?",
                    "options": [("Sim", 5), ("Não", 1), ("Em parte", 3)],
                    "type": "yes_no_partial"
                }
            ]
        },
        {
            "title": "Seção 2: Instalações e recursos",
            "questions": [
                {
                    "id": "q2_1",
                    "text": "1. Como você avaliaria as instalações do hospital (limpeza, conforto, etc.)?",
                    "options": [
                        ("Muito satisfeito(a)", 5),
                        ("Satisfeito(a)", 4),
                        ("Neutro(a)", 3),
                        ("Insatisfeito(a)", 2),
                        ("Muito insatisfeito(a)", 1)
                    ],
                    "type": "satisfaction_scale"
                },
                {
                    "id": "q2_2",
                    "text": "2. Os equipamentos e recursos disponíveis no hospital foram suficientes para o seu tratamento?",
                    "options": [("Sim", 5), ("Não", 1), ("Em parte", 3)],
                    "type": "yes_no_partial"
                }
            ]
        },
        {
            "title": "Seção 3: Comunicação",
            "questions": [
                {
                    "id": "q3_1",
                    "text": "1. Você sentiu que os profissionais de saúde explicaram claramente o seu diagnóstico e tratamento?",
                    "options": [("Sim", 5), ("Não", 1), ("Em parte", 3)],
                    "type": "yes_no_partial"
                },
                {
                    "id": "q3_2",
                    "text": "2. Você foi informado sobre os seus direitos e responsabilidades como paciente?",
                    "options": [("Sim", 5), ("Não", 1), ("Em parte", 3)],
                    "type": "yes_no_partial"
                }
            ]
        },
        {
            "title": "Seção 4: Filantropia e apoio",
            "questions": [
                {
                    "id": "q4_1",
                    "text": "1. Você sabe que o hospital é filantrópico e que sua missão é ajudar aqueles que não têm recursos?",
                    "options": [("Sim", 5), ("Não", 1)],
                    "type": "yes_no"
                },
                {
                    "id": "q4_2",
                    "text": "2. Você sente que o hospital está fazendo uma diferença positiva na comunidade?",
                    "options": [("Sim", 5), ("Não", 1), ("Em parte", 3)],
                    "type": "yes_no_partial"
                }
            ]
        },
        {
            "title": "Seção 5: Recomendação",
            "questions": [
                {
                    "id": "q5_1",
                    "text": "1. Você recomendaria este hospital para amigos e familiares?",
                    "options": [("Sim", 5), ("Não", 1), ("Em parte", 3)],
                    "type": "yes_no_partial"
                }
            ]
        }
    ]
    
    for section_order, section in enumerate(sections_data, 1):
        for question_order, question_data in enumerate(section["questions"], 1):
            # Criar pergunta
            question = Question(
                question_id=question_data["id"],
                section_title=section["title"],
                question_text=question_data["text"],
                question_type=question_data["type"],
                section_order=section_order,
                question_order=question_order
            )
            db.add(question)
            db.flush()  # Para obter o ID
            
            # Criar opções
            for option_order, (option_text, option_value) in enumerate(question_data["options"], 1):
                option = QuestionOption(
                    question_id=question.id,
                    option_text=option_text,
                    option_value=option_value,
                    option_order=option_order
                )
                db.add(option)
    
    db.commit()


# ====== APLICAÇÃO FASTAPI ======

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Configuração de inicialização e finalização da aplicação"""
    # Startup
    Base.metadata.create_all(bind=engine)
    
    # Inicializar dados
    db = SessionLocal()
    try:
        init_questions(db)
    finally:
        db.close()
    
    yield
    
    # Shutdown
    pass


app = FastAPI(
    title="Sistema de Pesquisa de Satisfação - Hospital Santa Clara",
    description="Sistema completo para coleta e análise de pesquisas de satisfação de pacientes",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ====== ROTAS PRINCIPAIS ======

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Página inicial com a pesquisa"""
    return templates.TemplateResponse("survey.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Dashboard de insights para diretoria"""
    
    # Calcular métricas principais
    total_surveys = db.query(Survey).filter(Survey.completed == True).count()
    avg_satisfaction = db.query(Survey).filter(Survey.satisfaction_score.isnot(None)).with_entities(
        db.func.avg(Survey.satisfaction_score)
    ).scalar() or 0
    
    # Buscar pesquisas recentes
    recent_surveys = db.query(Survey).filter(Survey.completed == True).order_by(
        Survey.created_at.desc()
    ).limit(10).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_surveys": total_surveys,
        "avg_satisfaction": round(avg_satisfaction, 2),
        "recent_surveys": recent_surveys
    })


@app.post("/api/submit-survey")
async def submit_survey(
    patient_name: str = Form(None),
    is_anonymous: bool = Form(False),
    admission_date: str = Form(...),
    discharge_date: str = Form(...),
    observations: str = Form(""),
    request: Request = Form(...),
    db: Session = Depends(get_db)
):
    """API para submeter uma nova pesquisa"""
    
    try:
        # Coletar todas as respostas do formulário
        form_data = await request.form()
        responses = {}
        
        for key, value in form_data.items():
            if key.startswith('q') and '_' in key:  # Perguntas no formato q1_1, q2_1, etc
                responses[key] = value
        
        # Calcular score de satisfação
        total_score = 0
        total_questions = 0
        
        for question_id, response_text in responses.items():
            question = db.query(Question).filter(Question.question_id == question_id).first()
            if question:
                option = db.query(QuestionOption).filter(
                    QuestionOption.question_id == question.id,
                    QuestionOption.option_text == response_text
                ).first()
                
                if option:
                    total_score += option.option_value
                    total_questions += 1
        
        satisfaction_score = total_score / total_questions if total_questions > 0 else 0
        
        # Criar registro da pesquisa
        survey = Survey(
            patient_name=patient_name if not is_anonymous else None,
            is_anonymous=is_anonymous,
            admission_date=admission_date,
            discharge_date=discharge_date,
            observations=observations,
            completed=True,
            satisfaction_score=satisfaction_score
        )
        
        db.add(survey)
        db.flush()  # Para obter o ID
        
        # Salvar respostas individuais
        for question_id, response_text in responses.items():
            question = db.query(Question).filter(Question.question_id == question_id).first()
            if question:
                option = db.query(QuestionOption).filter(
                    QuestionOption.question_id == question.id,
                    QuestionOption.option_text == response_text
                ).first()
                
                response = SurveyResponse(
                    survey_id=survey.id,
                    question_id=question.id,
                    response_value=response_text,
                    response_score=option.option_value if option else None
                )
                db.add(response)
        
        db.commit()
        
        return JSONResponse({
            "status": "success",
            "message": "Pesquisa enviada com sucesso!",
            "survey_id": survey.id
        })
        
    except Exception as e:
        db.rollback()
        return JSONResponse({
            "status": "error",
            "message": f"Erro ao salvar pesquisa: {str(e)}"
        }, status_code=500)


@app.get("/api/dashboard-data")
async def get_dashboard_data(db: Session = Depends(get_db)):
    """API para dados do dashboard"""
    
    try:
        # Métricas principais
        total_surveys = db.query(Survey).filter(Survey.completed == True).count()
        avg_satisfaction = db.query(Survey).filter(Survey.satisfaction_score.isnot(None)).with_entities(
            db.func.avg(Survey.satisfaction_score)
        ).scalar() or 0
        
        # Satisfação por seção
        section_scores = {}
        sections = db.query(Question.section_title).distinct().all()
        
        for section in sections:
            section_name = section[0]
            section_questions = db.query(Question).filter(Question.section_title == section_name).all()
            
            if section_questions:
                question_ids = [q.id for q in section_questions]
                section_avg = db.query(SurveyResponse).filter(
                    SurveyResponse.question_id.in_(question_ids),
                    SurveyResponse.response_score.isnot(None)
                ).with_entities(
                    db.func.avg(SurveyResponse.response_score)
                ).scalar() or 0
                
                section_scores[section_name] = round(section_avg, 2)
        
        # Tendência mensal (simulada para demonstração)
        monthly_trend = [3.8, 4.0, 4.1, 4.0, 4.2, 4.3, 4.2, 4.1, 4.0, 4.1, 4.2, round(avg_satisfaction, 1)]
        
        # Pesquisas recentes
        recent_surveys = []
        recent_data = db.query(Survey).filter(Survey.completed == True).order_by(
            Survey.created_at.desc()
        ).limit(5).all()
        
        for survey in recent_data:
            recent_surveys.append({
                "id": survey.id,
                "patient": survey.patient_name if not survey.is_anonymous else "Anônimo",
                "date": survey.created_at.strftime("%Y-%m-%d"),
                "score": round(survey.satisfaction_score, 1) if survey.satisfaction_score else 0
            })
        
        return JSONResponse({
            "totalSurveys": total_surveys,
            "avgSatisfaction": round(avg_satisfaction, 2),
            "sectionScores": section_scores,
            "monthlyTrend": monthly_trend,
            "recentSurveys": recent_surveys
        })
        
    except Exception as e:
        return JSONResponse({
            "error": str(e)
        }, status_code=500)


@app.get("/api/questions")
async def get_questions(db: Session = Depends(get_db)):
    """API para obter todas as perguntas e opções"""
    
    try:
        sections = {}
        questions = db.query(Question).order_by(Question.section_order, Question.question_order).all()
        
        for question in questions:
            section_title = question.section_title
            
            if section_title not in sections:
                sections[section_title] = {
                    "title": section_title,
                    "questions": []
                }
            
            options = db.query(QuestionOption).filter(
                QuestionOption.question_id == question.id
            ).order_by(QuestionOption.option_order).all()
            
            question_data = {
                "id": question.question_id,
                "text": question.question_text,
                "type": question.question_type,
                "options": [opt.option_text for opt in options]
            }
            
            sections[section_title]["questions"].append(question_data)
        
        return JSONResponse(list(sections.values()))
        
    except Exception as e:
        return JSONResponse({
            "error": str(e)
        }, status_code=500)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''

# Salvar o arquivo main.py
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(main_py_content)

print("✅ Arquivo main.py criado com sucesso!")
print("Tamanho do arquivo:", len(main_py_content), "caracteres")