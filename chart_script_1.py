import plotly.graph_objects as go

# Data for satisfaction by section
sections = ["Atendimento", "Instalações", "Comunicação", "Filantropia", "Recomendação"]
scores = [4.3, 4.1, 3.9, 4.6, 4.2]

# Hospital-appropriate colors (blues, greens, light grays)
colors = ['#1FB8CD', '#2E8B57', '#5D878F', '#D2BA4C', '#DB4545']

# Create bar chart
fig = go.Figure(data=[go.Bar(
    x=sections,
    y=scores,
    marker_color=colors,
    hovertemplate='%{x}: %{y}/5.0<extra></extra>',
    text=[f'{score}/5.0' for score in scores],
    textposition='outside'
)])

# Update layout with hospital dashboard styling
fig.update_layout(
    title='Satisfação por Seção - Hospital Santa Clara',
    xaxis_title='Seções',
    yaxis_title='Pontuação',
    yaxis=dict(range=[0, 5], tickformat='.1f'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False
)

# Update traces for better appearance
fig.update_traces(cliponaxis=False)

# Save as both PNG and SVG
fig.write_image("section_satisfaction.png")
fig.write_image("section_satisfaction.svg", format="svg")