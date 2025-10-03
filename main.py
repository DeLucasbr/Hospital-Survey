
"""
Sistema de Pesquisa de Satisfação - Hospital Santa Clara
Aplicação FastAPI completa com MySQL, templates HTML e dashboard de insights
"""

from datetime import datetime, date
from typing import Optional, List
import json
import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey, func, text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
import uvicorn
from contextlib import asynccontextmanager
import io
import csv
import hashlib
import secrets
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# ====== CONFIGURAÇÕES DE BANCO DE DADOS ======

# DATABASE_URL padrão para desenvolvimento local com SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hospital_satisfaction.db")

# Configuração do engine conforme o dialeto
engine_kwargs = {"pool_pre_ping": True}

if DATABASE_URL.startswith("sqlite"):
    # Melhor compatibilidade com SQLite em ambientes multi-thread
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # Para MySQL, reciclar conexões antigas
    engine_kwargs["pool_recycle"] = 3600

engine = create_engine(DATABASE_URL, **engine_kwargs)
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
    city = Column(String(255), nullable=True)
    ward = Column(String(100), nullable=True)

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


class User(Base):
    """Tabela de usuários para autenticação"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ====== MODELOS PYDANTIC ======

class SurveyCreate(BaseModel):
    patient_name: Optional[str] = None
    is_anonymous: bool = False
    admission_date: str
    discharge_date: str
    responses: dict
    observations: Optional[str] = None


class SurveyResponseModel(BaseModel):
    id: int
    patient_name: Optional[str]
    is_anonymous: bool
    admission_date: str
    discharge_date: str
    created_at: datetime
    satisfaction_score: Optional[float]

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool
    created_at: datetime

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


# ====== FUNÇÕES DE AUTENTICAÇÃO ======

def hash_password(password: str) -> str:
    """Cria hash da senha usando SHA-256 com salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    try:
        salt, hash_part = hashed_password.split(':')
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return password_hash == hash_part
    except:
        return False


def create_default_user(db: Session):
    """Cria usuário padrão se não existir nenhum"""
    if db.query(User).count() == 0:
        default_user = User(
            username="admin",
            password_hash=hash_password("admin123"),
            is_active=True
        )
        db.add(default_user)
        db.commit()
        print("Usuário padrão criado: admin / admin123")


def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """Obtém o usuário atual da sessão"""
    username = request.session.get("username")
    if username:
        user = db.query(User).filter(User.username == username, User.is_active == True).first()
        return user
    return None


def require_auth(current_user: Optional[User] = Depends(get_current_user)):
    """Dependência que exige autenticação"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autorizado"
        )
    return current_user


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

    # Migração leve: garantir colunas 'city' e 'ward' na tabela surveys (cross-database)
    try:
        inspector = inspect(engine)
        existing_columns = {col["name"] for col in inspector.get_columns("surveys")}
        with engine.connect() as conn:
            if "city" not in existing_columns:
                conn.execute(text("ALTER TABLE surveys ADD COLUMN city VARCHAR(255)"))
            if "ward" not in existing_columns:
                conn.execute(text("ALTER TABLE surveys ADD COLUMN ward VARCHAR(100)"))
    except Exception:
        # Evitar quebra de startup por falha de migração; logs podem ser adicionados conforme necessário
        pass

    # Inicializar dados
    db = SessionLocal()
    try:
        init_questions(db)
        create_default_user(db)
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

# Adicionar middleware de sessão
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="hospital-santa-clara-secret-key-2024")

# Configurar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ====== ROTAS PRINCIPAIS ======

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Página inicial com a pesquisa"""
    return templates.TemplateResponse("survey.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de login"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Processar login do usuário"""
    user = db.query(User).filter(User.username == username, User.is_active == True).first()
    
    if user and verify_password(password, user.password_hash):
        request.session["username"] = user.username
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Usuário ou senha incorretos"
        })


@app.get("/logout")
async def logout(request: Request):
    """Fazer logout do usuário"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(require_auth)):
    """Dashboard de insights para diretoria"""

    # Calcular métricas principais
    total_surveys = db.query(Survey).filter(Survey.completed == True).count()
    avg_satisfaction = db.query(Survey).filter(Survey.satisfaction_score.isnot(None)).with_entities(
        func.avg(Survey.satisfaction_score)
    ).scalar() or 0

    # Buscar pesquisas recentes
    recent_surveys = db.query(Survey).filter(Survey.completed == True).order_by(
        Survey.created_at.desc()
    ).limit(10).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_surveys": total_surveys,
        "avg_satisfaction": round(avg_satisfaction, 2),
        "recent_surveys": recent_surveys,
        "current_user": current_user
    })


@app.post("/api/submit-survey")
async def submit_survey(
    request: Request,
    patient_name: str = Form(None),
    is_anonymous: bool = Form(False),
    admission_date: str = Form(...),
    discharge_date: str = Form(...),
    observations: str = Form(""),
    city: str = Form(""),
    ward: str = Form(""),
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
            satisfaction_score=satisfaction_score,
            city=city or None,
            ward=ward or None
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
async def get_dashboard_data(db: Session = Depends(get_db), current_user: User = Depends(require_auth)):
    """API para dados do dashboard"""

    try:
        # Métricas principais
        total_surveys = db.query(Survey).filter(Survey.completed == True).count()
        avg_satisfaction = db.query(Survey).filter(Survey.satisfaction_score.isnot(None)).with_entities(
            func.avg(Survey.satisfaction_score)
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
                    func.avg(SurveyResponse.response_score)
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
                "score": round(survey.satisfaction_score, 1) if survey.satisfaction_score else 0,
                "observations": survey.observations or "",
                "city": survey.city or "",
                "ward": survey.ward or ""
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


@app.get("/api/surveys/{survey_id}")
async def get_survey_details(survey_id: int, db: Session = Depends(get_db)):
    """Retorna detalhes completos de uma pesquisa: dados do paciente e todas as respostas.
    """
    try:
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        if not survey:
            raise HTTPException(status_code=404, detail="Pesquisa não encontrada")

        # Buscar respostas com perguntas e opções
        responses = db.query(SurveyResponse).join(Question, SurveyResponse.question_id == Question.id) \
            .filter(SurveyResponse.survey_id == survey_id) \
            .order_by(Question.section_order, Question.question_order).all()

        # Estruturar por seção
        sections: dict[str, dict] = {}
        for resp in responses:
            section_title = resp.question.section_title
            if section_title not in sections:
                sections[section_title] = {"title": section_title, "items": []}
            sections[section_title]["items"].append({
                "questionId": resp.question.question_id,
                "question": resp.question.question_text,
                "answer": resp.response_value,
                "score": resp.response_score
            })

        payload = {
            "id": survey.id,
            "patient": None if survey.is_anonymous else (survey.patient_name or ""),
            "isAnonymous": survey.is_anonymous,
            "admissionDate": survey.admission_date,
            "dischargeDate": survey.discharge_date,
            "city": survey.city or "",
            "ward": survey.ward or "",
            "observations": survey.observations or "",
            "createdAt": survey.created_at.isoformat(),
            "satisfactionScore": survey.satisfaction_score or 0,
            "sections": list(sections.values())
        }

        return JSONResponse(payload)

    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/api/export-csv")
async def export_csv(db: Session = Depends(get_db), current_user: User = Depends(require_auth)):
    """Exporta todas as respostas das pesquisas em formato CSV (long format).

    Colunas: survey_id, created_at, patient, is_anonymous, city, ward,
    satisfaction_score, question_id, section_title, question_text,
    response_value, response_score
    """
    try:
        # Consultar respostas com joins necessários
        query = (
            db.query(
                Survey.id.label("survey_id"),
                Survey.created_at.label("created_at"),
                Survey.patient_name.label("patient_name"),
                Survey.is_anonymous.label("is_anonymous"),
                Survey.city.label("city"),
                Survey.ward.label("ward"),
                Survey.satisfaction_score.label("satisfaction_score"),
                Question.question_id.label("question_id"),
                Question.section_title.label("section_title"),
                Question.question_text.label("question_text"),
                SurveyResponse.response_value.label("response_value"),
                SurveyResponse.response_score.label("response_score"),
            )
            .join(SurveyResponse, SurveyResponse.survey_id == Survey.id)
            .join(Question, SurveyResponse.question_id == Question.id)
            .order_by(Survey.created_at.desc(), Survey.id, Question.section_order, Question.question_order)
        )

        # Construir CSV em memória
        output = io.StringIO()
        writer = csv.writer(output)
        header = [
            "survey_id",
            "created_at",
            "patient",
            "is_anonymous",
            "city",
            "ward",
            "satisfaction_score",
            "question_id",
            "section_title",
            "question_text",
            "response_value",
            "response_score",
        ]
        writer.writerow(header)

        for row in query.all():
            writer.writerow([
                row.survey_id,
                row.created_at.strftime("%Y-%m-%d %H:%M:%S") if row.created_at else "",
                "" if row.is_anonymous else (row.patient_name or ""),
                1 if row.is_anonymous else 0,
                row.city or "",
                row.ward or "",
                f"{row.satisfaction_score:.2f}" if row.satisfaction_score is not None else "",
                row.question_id,
                row.section_title,
                row.question_text,
                row.response_value,
                row.response_score if row.response_score is not None else "",
            ])

        output.seek(0)

        # Preparar resposta de streaming
        filename = f"survey_responses_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            },
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/api/export-json")
async def export_json(db: Session = Depends(get_db), current_user: User = Depends(require_auth)):
    """Exporta todas as pesquisas concluídas em JSON (estrutura aninhada por pesquisa)."""
    try:
        surveys = db.query(Survey).filter(Survey.completed == True).order_by(Survey.created_at.desc()).all()

        export_payload = []
        for survey in surveys:
            # Obter respostas da pesquisa com perguntas ordenadas por seção e ordem
            responses = (
                db.query(SurveyResponse).join(Question, SurveyResponse.question_id == Question.id)
                .filter(SurveyResponse.survey_id == survey.id)
                .order_by(Question.section_order, Question.question_order)
                .all()
            )

            sections: dict[str, dict] = {}
            for resp in responses:
                section_title = resp.question.section_title
                if section_title not in sections:
                    sections[section_title] = {"title": section_title, "items": []}
                sections[section_title]["items"].append({
                    "questionId": resp.question.question_id,
                    "question": resp.question.question_text,
                    "answer": resp.response_value,
                    "score": resp.response_score,
                })

            export_payload.append({
                "id": survey.id,
                "createdAt": survey.created_at.isoformat() if survey.created_at else "",
                "patient": None if survey.is_anonymous else (survey.patient_name or ""),
                "isAnonymous": survey.is_anonymous,
                "admissionDate": survey.admission_date,
                "dischargeDate": survey.discharge_date,
                "city": survey.city or "",
                "ward": survey.ward or "",
                "observations": survey.observations or "",
                "satisfactionScore": survey.satisfaction_score or 0,
                "sections": list(sections.values()),
            })

        # Serializar para JSON e retornar como download
        json_str = json.dumps(export_payload, ensure_ascii=False, indent=2)
        buffer = io.BytesIO(json_str.encode("utf-8"))
        filename = f"surveys_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        return StreamingResponse(
            buffer,
            media_type="application/json; charset=utf-8",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            },
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
