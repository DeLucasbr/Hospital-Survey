# Create the mermaid flowchart for Hospital Santa Clara Patient Satisfaction Survey System
diagram_code = """
flowchart TD
    subgraph PL["🏥 PRESENTATION LAYER"]
        tablet["📱 Interface Tablet<br/>(Pesquisa)"]
        dashboard["📊 Dashboard Admin<br/>(Diretoria)"]
    end
    
    subgraph AL["⚙️ APPLICATION LAYER"]
        fastapi["🚀 FastAPI<br/>Application"]
        sqlalchemy["🔧 SQLAlchemy<br/>ORM"]
        pydantic["✅ Pydantic<br/>Models"]
    end
    
    subgraph DL["💾 DATA LAYER"]
        mysql["🗄️ MySQL<br/>Database"]
        tables["📋 Tables:<br/>surveys, questions,<br/>question_options,<br/>survey_responses"]
        views["📈 Analytical<br/>Views"]
        backup["💿 Backup<br/>System"]
    end
    
    %% Connections
    tablet -->|Submit Survey| fastapi
    dashboard -->|Get Analytics| fastapi
    fastapi -->|Data Operations| sqlalchemy
    fastapi -->|Validation| pydantic
    sqlalchemy -->|SQL Queries| mysql
    mysql -->|Store Data| tables
    mysql -->|Generate Views| views
    mysql -->|Auto Backup| backup
    
    %% Technology stack annotations
    subgraph TECH["🛠️ KEY TECHNOLOGIES"]
        frontend["Frontend:<br/>HTML5, CSS3,<br/>JavaScript, Bootstrap"]
        backend["Backend:<br/>Python, FastAPI,<br/>SQLAlchemy, Pydantic"]
        database["Database:<br/>MySQL, Docker,<br/>phpMyAdmin"]
    end
    
    %% Styling
    classDef presentationClass fill:#E3F2FD,stroke:#1976D2,stroke-width:2px
    classDef applicationClass fill:#E8F5E8,stroke:#388E3C,stroke-width:2px
    classDef dataClass fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px
    classDef techClass fill:#FFF3E0,stroke:#F57C00,stroke-width:2px
    
    class tablet,dashboard presentationClass
    class fastapi,sqlalchemy,pydantic applicationClass
    class mysql,tables,views,backup dataClass
    class frontend,backend,database techClass
"""

# Create the mermaid diagram using the helper function
png_path, svg_path = create_mermaid_diagram(
    diagram_code, 
    png_filepath='hospital_architecture.png',
    svg_filepath='hospital_architecture.svg',
    width=1400, 
    height=1000
)

print(f"Flowchart saved as: {png_path} and {svg_path}")