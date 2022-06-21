import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import flagpy as fp
import plotly.graph_objects as go

st.set_page_config(page_title='Fifa Word Cup History', page_icon=':soccer:', initial_sidebar_state='expanded',
                   layout="wide")
# matches = pd.read_csv('Data\matches.csv')
image = Image.open('word cup wallpaper.jpg')

st.image(image, caption='Word Cups History')

# leagues_stats = pd.read_csv('league_stats.csv')
# all_tables_data = pd.read_csv('all_tables.csv')
# st.markdown('# Select League ')
# selected_league = st.radio('', leagues_stats['League'], horizontal=True)
#
# row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3 = st.columns((1.6, .05, 1.6, .05, 1.6))
# with row2_1:
#     unique_games_in_df = leagues_stats.loc[leagues_stats['League'] == selected_league]['GP'].iloc[0]
#     str_games = "🏟️ " + str(unique_games_in_df) + " Matches"
#     st.markdown(str_games)
# with row2_2:
#     unique_teams_in_df = leagues_stats.loc[leagues_stats['League'] == selected_league]['Num_teams'].iloc[0]
#     t = " Teams"
#     if (unique_teams_in_df == 1):
#         t = " Team"
#     str_teams = "🏃‍♂️ " + str(unique_teams_in_df) + t
#     st.markdown(str_teams)
# with row2_3:
#     total_goals_in_df = leagues_stats.loc[leagues_stats['League'] == selected_league]['GF'].iloc[0]
#     str_goals = "🥅 " + str(total_goals_in_df) + " Goals"
#     st.markdown(str_goals)
#
# teams_in_league = all_tables_data.loc[all_tables_data['League'] == selected_league]
# teams = np.unique(teams_in_league['Team'])
# seasons = np.unique(teams_in_league['Year'])
# selected_team = st.radio('Pick a Team:', teams, horizontal=True)
# team_data = teams_in_league.loc[teams_in_league['Team'] == selected_team]
#
# selected_season = st.select_slider('Choose season', seasons)
# selected_team_season = team_data.loc[team_data['Year'] == selected_season]
#
#
# def thropy(place):
#     if place == 1:
#         return ':trophy:'
#     else:
#         return ''
#
#
# team_info = f' In season {selected_season}-{selected_season + 1} {selected_team} played '
#
# try:
#
#     games = int(selected_team_season['GP'])
#     str_games = str(games) + " Matches " + " 🏟️ "
#     team_info += str_games
#     wins = int(selected_team_season['W'])
#     str_teams = " and got " + str(wins) + " Wins, "
#     team_info += str_teams
#
#     draws = int(selected_team_season['D'])
#     str_teams = str(draws) + "  Draws and  "
#     team_info += str_teams
#
#     loss = int(selected_team_season['L'])
#     str_teams = str(loss) + "  Loses."
#     team_info += str_teams
#     st.write(team_info)
#     team_info = 'They Scored '
#     goals = int(selected_team_season['GF'])
#     str_teams = str(goals) + " Goals  🥅 and conceded "
#     team_info += str_teams
#
#     conc = int(selected_team_season['GA'])
#     str_teams = str(conc) + "  Goals and finish in "
#
#     team_info += str_teams
#     place_finshed = int(selected_team_season['Place'])
#     tro = thropy(place_finshed)
#     str_goals = ' ' + str(place_finshed) + 'th' + tro + " Place."
#     team_info += str_goals
#     st.write(team_info)
#     # if place_finshed == 1:
#     #     str_goals = ":trophy:  " + str(place_finshed) + 'th' + " Place"
#     # else:
#     #     str_goals = str(place_finshed) + 'th' + " Place"
# except:
#     st.write(f'Oops.. This team was not in this league this season')

# st.write(f'In season {selected_season}/{selected_season+1} ')

# # Set page config
#
# games_list = sorted(list(set(dataframe['player'])))
# players = pd.read_csv('players_details.csv')
# # Drop-down menu "Select Football Game"
# st.sidebar.markdown('## Select Player ')
# menu_game = st.sidebar.selectbox('Select a player at your choice', games_list, index=14)
#
# selected_player =players. loc[players['Player'] == menu_game]
# st.write(f'my name is {menu_game} i born in {selected_player["Nationality"].iloc[0]} in {selected_player["Birth_Date"].iloc[0]}  ')
import numpy as np

import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

# Reading sample data using pandas DataFrame
df = pd.read_csv('teams_goals.csv')
matches = pd.read_csv('WorldCupMatches.csv')
worlds = pd.read_csv('WorldCups.csv')
matches.dropna(how='all', inplace=True)
num_games = len(np.unique(matches['MatchID']))
num_goals = df['Total_goals'].sum()
countries = list(np.unique(df['Team Name']))
country_flag = {'All': 'global_flag.png', 'Germany FR': 'west germany.png', 'German DR': 'east germany.png',
                'United Kingdom': 'uk flag.png', 'Soviet Union': 'soviet flag.png', 'Czechoslovakia': 'czech.png',
                'Dutch East Indies': 'deind.png', 'Netherlands': 'nether.png',
                'USA': 'usa.png', 'United Arab Emirates': 'uae.png', 'Wales': 'wales.png'}

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
                list_flags.append(country_flag[flag])
            else:
                try:
                    img = fp.get_flag_img(flag)
                    list_flags.append(img)
                except:
                    pass
    else:
        list_flags.append('global_flag.png')
    st.image(list_flags, width=100)
if not selected_country:
    data_chosen = df.loc[df['Year'] == year_chosen]
    range_color = None
else:

    data_chosen = df.loc[(df['Year'] == year_chosen) & (df['Team Name'].isin(selected_country))]
    selected_country_df = df.loc[df['Team Name'].isin(selected_country)]

    range_color = (min(selected_country_df['Total_goals']), max(selected_country_df['Total_goals']))
if len(data_chosen) == 0:
    st.write(f"Oh no.. These countries weren't qualified for the World Cup this year")
    data_chosen = df.loc[(df['Year'] == 1938) & (df['Team Name'] == 'Dutch East Indies')]
    fig = px.choropleth(data_chosen, locations='Team Initials',
                        color="Total_goals", hover_name='Team Name', color_continuous_scale='Sunsetdark',
                        range_color=range_color)
    fig.update_layout(
        autosize=False,
        width=1600,
        height=920, margin=dict(l=0, r=0, t=0, b=0))

    st.plotly_chart(fig, use_container_width=False)
else:

    fig = px.choropleth(data_chosen, locations='Team Initials',
                        color="Total_goals", hover_name='Team Name', color_continuous_scale='Sunsetdark',
                        range_color=range_color)
    fig.update_layout(
        autosize=False,
        width=1600,
        height=920, margin=dict(l=0, r=0, t=0, b=0))

    st.plotly_chart(fig, use_container_width=False)
worlds['Attendance'] = worlds['Attendance'].map(lambda x: int(('').join(x.split('.'))))
# worlds['Attendance'] =np.log10( worlds['Attendance'].map(lambda x: int(('').join(x.split('.')))))
fig = px.line(worlds, x="Year", y="Attendance",text='Year',animation_frame='Year')
fig.update_traces(textposition="bottom right")
fig.update_layout(
    autosize=False,
    width=1600,
    height=920, margin=dict(l=0, r=0, t=0, b=0),
    font=dict(
        family="Calibri",
        size=18,
        color="RebeccaPurple"
    ))
# pick points that are special...
df2 = worlds.loc[worlds['Year'] == year_chosen]

# add special markers without hoverinfo
fig.add_traces(
go.Scatter(
    x=np.unique(df2['Year']), y=np.unique(df2["Attendance"]), mode="markers" ,name=f'Year {int(year_chosen)}')
)
fig.update_traces(marker=dict(size=18,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
st.plotly_chart(fig,use_container_width=False)

# images = list(country_flag.values())
# st.image(images,width=100)
