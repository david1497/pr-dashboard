import plotly.graph_objects as go # type: ignore

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


def get_nth_latest_record(df, n):
    # Function to get the nth latest record for each project
    # Sort by 'Project Name' and 'Date' in descending order
    df_sorted = df.sort_values(by=['Date'], ascending=[False])
    # Group by 'Project Name' and get the nth record (0-based index)
    nth_record = df_sorted.groupby('Project Name').nth(n-1)

    return nth_record.reset_index()


def get_nth_value_column(df, col_name, selected_projects=[], pos=1):
    df = get_nth_latest_record(df, pos)
    if len(selected_projects) == 0:
        nth_value = df[col_name].sum()
    else:
        nth_value = df[df['Project Name'].isin(selected_projects)][col_name].sum()
    
    return nth_value


def get_change_direction(df, col_name, selected_projects=[]):
    last_value = get_nth_value_column(df, col_name, selected_projects, 1)
    pre_last_value = get_nth_value_column(df, col_name, selected_projects, 2)

    change = last_value - pre_last_value
    
    return change