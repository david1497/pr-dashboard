import plotly.express as px
import plotly.graph_objects as go

def build_area_chart(df, column_name, projects_name=None, level='global', lc='blue', fc='rgba(0, 100, 200, 0.5)'):
    if level == 'global':
        df['month'] = df['Date'].dt.month
        if column_name == 'Margin (%)':
            df = df.groupby('month').agg({column_name:'mean'})
        else:
            df = df.groupby('month').agg({column_name:'sum'})
        df = df.sort_values('month')
    else:
        df = df.where(df['Project Name'].isin(projects_name))
        df['month'] = df['Date'].dt.month
        if len(projects_name) > 1:
            if column_name == 'Margin (%)':
                df = df.groupby('month').agg({column_name:'mean'})
            else:
                df = df.groupby('month').agg({column_name:'sum'})
        else:
            df = df[df['Project Name'] == projects_name[0]]
        df = df.sort_values('month')
    df.reset_index(inplace=True)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df['month'], 
            y=df[column_name], 
            mode='lines', 
            name='Value',
            fill='tozeroy',
            fillcolor=fc,
            line=dict(color=lc)
        )
    )
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        title=None,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
        hovermode=False,
    )
    fig.update_layout(dragmode=False, hovermode='closest')
    return fig