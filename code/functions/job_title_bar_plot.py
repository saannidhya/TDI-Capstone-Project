try:
    import plotly.graph_objs as go
    import plotly.offline as pyo
except Exception as e:
    print(f"Some Modules are Missing {e}")

def job_title_bar_plot(df, city_bool, title_bool):
    df_plot = df.loc[(city_bool) & (title_bool), :][['id', 'Job_Title']].groupby('Job_Title').agg(
        'count').reset_index().rename(columns={'id': 'frequency'})
    fig = go.Figure([go.Bar(x=df_plot['Job_Title'], y=df_plot['frequency'], marker=dict(color='#FF7F0E'), width=0.05)])
    fig.layout.template = 'plotly_white'
    pyo.plot(fig)
