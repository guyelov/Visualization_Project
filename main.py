import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import flagpy as fp
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title='Fifa Word Cup History', page_icon=':soccer:', initial_sidebar_state='expanded',
                   layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("style.css")

### Data Import ###
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


####################
### INTRODUCTION ###
####################

_, row_1, _, row_2, _ = st.columns((.1, 2.3, .1, 1.3, .1))
with row_1:
    st.title('The Evolution Of The *FIFA* World Cup')
with row_2:
    st.text("")
    st.subheader('Streamlit App by Omer Idgar and Guy Elovici')
_, row_1, _ = st.columns((.1, 3.2, .1))
with row_1:
    st.markdown(
        'The FIFA World Cup Qatar2022 is just around the corner!😱 Here you can view the evolution of the world cup tournament over the years.'
        ' You can also compare any country at your leisure and View the performance of countries in each world cup tournament. Also, see which country'
        'has participated the most times at the world cup. Just choose your country,  Select a year to view some soccer data ⚽🥅')
    st.markdown("You can find the source code in the [Project GitHub Repository](https://github.com/guyelov/Visualization_Project)")

# image = Image.open('world cup images/word cup wallpaper.jpg')
# st.image(image, caption='World Cups History')


#####################################
### Analysis per Country and Year ###
#####################################
_, row_1, _ = st.columns((.1, 3.2, .1))
with row_1:
    st.subheader('Analysis per Country and Year')
    st.markdown(
        f'You can view how many goals each of the participating countries scored in a particular year of the world cup.'
        f' Then, you can choose the countries and compare the number of goals they scored in each world cup.')


##############
### Slider ###
##############
_, row_1, _ = st.columns((.1, 3.2, .1))
with row_1:
    year_chosen = st.select_slider('Drag the slider to change the year:', years)

_, row2_1, _, row2_2, _ = st.columns((.1, 1.6, .05, 1.6, .1))
with row2_1:
    selected_country = st.multiselect('Select some Countries:', options=countries)
    s = 'You selected'
    if not selected_country:
        s += ' no specific country'
    else:
        for country in selected_country:
            s += f' {country},'
        s = s.strip(',')
    st.markdown(s+'.')
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
    data_chosen = data.loc[data['Year'] == year_chosen]

    data_goals = goals[:15]
    range_color = None
else:
    data_chosen = data.loc[(data['Year'] == year_chosen) & (data['Team Name'].isin(selected_country))]

    selected_country_df = df.loc[df['Team Name'].isin(selected_country)]

    data_goals = goals.loc[goals['Team Name'].isin(selected_country)]
    range_color = (0, max(selected_country_df['Total_goals']))

#############
### Plots ###
#############
_, row_1, _, row_2, _ = st.columns((.1, 5, .05, 4, .1))

# MAP
with row_1:
    st.markdown(f'##### Number of goals scored by the countries in {int(year_chosen)} World Cup')
    if len(data_chosen) == 0:
        st.info(f"Oh no.. Your selected countries weren't qualified for the World Cup this year")
        data_chosen = df.loc[(df['Year'] == 1938) & (df['Team Name'] == 'Dutch East Indies')]

        fig = px.choropleth(data_chosen, locations='Team Initials',
                            color="Total_goals", hover_name='Team Name',
                            color_continuous_scale='Sunsetdark',
                            range_color=range_color)
    else:
        fig = px.choropleth(data_chosen, locations='Team Initials',
                            color="Total_goals", hover_name='Team Name', hover_data=['Player Name', 'Goals Scored'],
                            color_continuous_scale='Sunsetdark',
                            range_color=range_color)
    fig.layout.coloraxis.colorbar.title = 'Total Goals'
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), dragmode=False)
    st.plotly_chart(fig, use_container_width=True)

# Line Plot
with row_2:
    st.markdown(f'##### Number of *#Attribute* over the years up to {int(year_chosen)} World Cup')
    attribute = st.radio(
        "Select Attribute",
        ('Attendance', 'QualifiedTeams', 'GoalsScored'), horizontal=True)
    if attribute == 'Attendance':
        worlds['Attendance'] = worlds['Attendance'].map(lambda x: int(('').join(x.split('.'))))

    worlds['Year'] = worlds['Year'].astype('int')

    worlds = worlds.loc[worlds['Year'] <= year_chosen]
    fig = px.line(worlds, x="Year", y=attribute, range_x=[1930, 2018], template="simple_white")
    fig.update_traces(textposition="bottom right")
    fig.update_layout(
        plot_bgcolor ='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(
            family="Calibri",
            size=14,
            color="#ffa600"),
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


# Bar Plot
_, row_1, _ = st.columns((.1, 3.2, .1))
with row_1:
    st.markdown(f'##### Total Qualifications of each country up to year {int(year_chosen)} in the World Cup')
    fig = px.bar(qualified_team, x='Team Name', y='Year', template="simple_white")
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Qualifications",
        plot_bgcolor='rgba(255, 255, 255 50)',
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(
            family="Calibri",
            size=18,
            color="#ffa600"),
        xaxis=dict(
            tickmode='linear'
        ))
    st.plotly_chart(fig, use_container_width=True)