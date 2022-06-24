import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import flagpy as fp
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title='Fifa Word Cup History', page_icon=':soccer:', initial_sidebar_state='expanded',
                   layout="wide")
st.title('World Cup History')
st.markdown(
    'The FIFA World Cup Qatar2022 is just around the corner!😱 Here you can view the evolution of the world cup tournament over the years.'
    ' You can also compare any country at your leisure and View the performance of countries in each world cup tournament. Also, see which country'
    'has participated the most times at the world cup. Just choose your country,  Select a year to view some soccer data ⚽🥅')
image = Image.open('world cup images/word cup wallpaper.jpg')
st.image(image, caption='World Cups History')
st.markdown(f'You can view how many goals each of the participating countries scored in a particular year of the world cup.'
            f' Then, you can choose the countries and compare the number of goals they scored in each world cup.')

data = pd.read_csv('Data/data.csv')
df = pd.read_csv('Data/teams_goals.csv')
matches = pd.read_csv('Data/WorldCupMatches.csv')
worlds = pd.read_csv('Data/WorldCups.csv')
matches.dropna(how='all', inplace=True)
num_games = len(np.unique(matches['MatchID']))
num_goals = df['Total_goals'].sum()
countries = list(np.unique(df['Team Name']))
country_flag = {'All': 'global_flag.png', 'Germany FR': 'west germany.png', 'German DR': 'east germany.png',
                'United Kingdom': 'uk flag.png', 'Soviet Union': 'soviet flag.png', 'Czechoslovakia': 'czech.png',
                'Dutch East Indies': 'deind.png', 'Netherlands': 'nether.png',
                'USA': 'usa.png', 'United Arab Emirates': 'uae.png', 'Wales': 'wales.png'}
goals = pd.read_csv('Data/goals_scoring.csv')

years = list(np.unique(df['Year']))
year_chosen = st.select_slider('Choose Year', years)

row2_1, row2_spacer2, row2_2 = st.columns((1.6, .05, 1.6))
with row2_1:
    selected_country = st.multiselect(
        'Choose a Country', countries
    )
    s = 'You selected'
    for country in selected_country:
        s += f' {country},'
    st.write(s)
with row2_2:
    list_flags = []
    if selected_country:
        for flag in selected_country:
            if flag in country_flag:
                list_flags.append(f'world cup images/{country_flag[flag]}')
            else:
                try:
                    img = fp.get_flag_img(flag)
                    list_flags.append(img)
                except:
                    pass
    else:
        list_flags.append('world cup images/global_flag.png')
    st.image(list_flags, width=100)
if not selected_country:
    # data_chosen = df.loc[df['Year'] == year_chosen]
    data_chosen = data.loc[data['Year'] == year_chosen]

    data_goals = goals[:15]
    range_color = None
else:

    # data_chosen = df.loc[(df['Year'] == year_chosen) & (df['Team Name'].isin(selected_country))]
    data_chosen = data.loc[(data['Year'] == year_chosen) & (data['Team Name'].isin(selected_country))]

    selected_country_df = df.loc[df['Team Name'].isin(selected_country)]

    data_goals = goals.loc[goals['Team Name'].isin(selected_country)]
    range_color = (min(selected_country_df['Total_goals']), max(selected_country_df['Total_goals']))
row3_1, row3_spacer2, row3_2 = st.columns((5, .05, 4))
with row3_1:
    if len(data_chosen) == 0:
        st.write(f"Oh no.. These countries weren't qualified for the World Cup this year")
        data_chosen = df.loc[(df['Year'] == 1938) & (df['Team Name'] == 'Dutch East Indies')]

        fig = px.choropleth(data_chosen, locations='Team Initials',
                            color="Total_goals", hover_name='Team Name',
                            color_continuous_scale='Sunsetdark',
                            range_color=range_color,title=f'Number of goals scored by the country in {year_chosen} World Cup')
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0))

        st.plotly_chart(fig, use_container_width=True)
    else:

        fig = px.choropleth(data_chosen, locations='Team Initials',
                            color="Total_goals", hover_name='Team Name', hover_data=['Player Name', 'Goals Scored'],
                            color_continuous_scale='Sunsetdark',
                            range_color=range_color,title=f'Number of goals scored by the country in {year_chosen} World Cup')
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

with row3_2:
    attribute = st.radio(
        "Select Attribute",
        ('Attendance', 'QualifiedTeams', 'GoalsScored'), horizontal=True)
    if attribute == 'Attendance':
        worlds['Attendance'] = worlds['Attendance'].map(lambda x: int(('').join(x.split('.'))))

    worlds['Year'] = worlds['Year'].astype('int')

    worlds = worlds.loc[worlds['Year'] <= year_chosen]
    # worlds['Attendance'] =np.log10( worlds['Attendance'].map(lambda x: int(('').join(x.split('.')))))
    fig = px.line(worlds, x="Year", y=attribute, range_x=[1930, 2018], template="simple_white",title=f'Number of goals scored by the country in {year_chosen} World Cup')
    fig.update_traces(textposition="bottom right")
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(
            family="Calibri",
            size=18,
            color="RebeccaPurple"),
        xaxis=dict(
            tickmode='linear',
            tick0=1930,
            dtick=4
        ))

    # pick points that are special...
    df2 = worlds.loc[worlds['Year'] == year_chosen]

    # add special markers without hoverinfo
    fig.add_traces(
        go.Scatter(
            x=np.unique(df2['Year']), y=np.unique(df2[attribute]), mode="markers", name=f'Year {int(year_chosen)}')
    )
    fig.update_traces(marker=dict(size=18,
                                  line=dict(width=2,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    st.plotly_chart(fig, use_container_width=True)
if not selected_country:
    qualified_team = df.loc[df['Year'] <= year_chosen] \
                         .groupby(['Team Name'])['Year'] \
                         .count().reset_index().sort_values(by='Year', ascending=False)[:15]

else:
    qualified_team = df.loc[(df['Year'] <= year_chosen) & (df['Team Name'].isin(selected_country))] \
                         .groupby(['Team Name'])['Year'] \
                         .count().reset_index().sort_values(by='Year', ascending=False)[:15]

fig = px.bar(qualified_team, 'Team Name', 'Year', template="simple_white")
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    font=dict(
        family="Calibri",
        size=18,
        color="RebeccaPurple"),
    xaxis=dict(
        tickmode='linear'
    ))
st.plotly_chart(fig, use_container_width=True)
