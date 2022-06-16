import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title='Soccer Players Stats', page_icon=':soccer:', initial_sidebar_state='expanded',
                   layout="wide")
# matches = pd.read_csv('Data\matches.csv')

leagues_stats = pd.read_csv('league_stats.csv')
all_tables_data = pd.read_csv('all_tables.csv')
st.markdown('# Select League ')
selected_league = st.radio('', leagues_stats['League'], horizontal=True)
row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3 = st.columns((1.6, .2, 1.6, .2, 1.6))
with row2_1:
    unique_games_in_df = leagues_stats.loc[leagues_stats['League'] == selected_league]['GP'].iloc[0]
    str_games = "🏟️ " + str(unique_games_in_df) + " Matches"
    st.markdown(str_games)
with row2_2:
    unique_teams_in_df = leagues_stats.loc[leagues_stats['League'] == selected_league]['Num_teams'].iloc[0]
    t = " Teams"
    if (unique_teams_in_df == 1):
        t = " Team"
    str_teams = "🏃‍♂️ " + str(unique_teams_in_df) + t
    st.markdown(str_teams)
with row2_3:
    total_goals_in_df = leagues_stats.loc[leagues_stats['League'] == selected_league]['GF'].iloc[0]
    str_goals = "🥅 " + str(total_goals_in_df) + " Goals"
    st.markdown(str_goals)

teams_in_league = all_tables_data.loc[all_tables_data['League'] == selected_league]
teams = np.unique(teams_in_league['Team'])
seasons = np.unique(teams_in_league['Year'])
selected_team = st.radio('Pick a Team:', teams, horizontal=True)
team_data = teams_in_league.loc[teams_in_league['Team'] == selected_team]

selected_season = st.select_slider('Choose season', seasons)
selected_team_season = team_data.loc[team_data['Year'] == selected_season]
def thropy(place):
    if place == 1:
        return ':trophy:'
    else:
        return ''

team_info =f' In season {selected_season}-{selected_season+1} {selected_team} played '

try:

    games = int(selected_team_season['GP'])
    str_games =  str(games) + " Matches " + " 🏟️ "
    team_info+=str_games
    wins = int(selected_team_season['W'])
    str_teams = " and got "+ str(wins)+ " Wins, "
    team_info+=str_teams

    draws = int(selected_team_season['D'])
    str_teams =str(draws)+ "  Draws and  "
    team_info+=str_teams

    loss = int(selected_team_season['L'])
    str_teams =str(loss) + "  Loses."
    team_info+=str_teams
    st.write(team_info)
    team_info = 'They Scored '
    goals = int(selected_team_season['GF'])
    str_teams = str(goals) +  " Goals  🥅 and conceded "
    team_info+=str_teams

    conc = int(selected_team_season['GA'])
    str_teams =str(conc) + "  Goals and finish in "

    team_info+=str_teams
    place_finshed = int(selected_team_season['Place'])
    tro = thropy(place_finshed)
    str_goals = tro + ' ' +'th' + " Place"+ str(place_finshed)
    team_info+=str_goals
    st.write(team_info)
    # if place_finshed == 1:
    #     str_goals = ":trophy:  " + str(place_finshed) + 'th' + " Place"
    # else:
    #     str_goals = str(place_finshed) + 'th' + " Place"
except:
    st.write(f'Oops.. This team was not in this league this season')
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
