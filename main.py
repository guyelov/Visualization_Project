import streamlit as st
import numpy as np
import pandas as pd
st.set_page_config(page_title='Soccer Players Stats', page_icon=':soccer:', initial_sidebar_state='expanded',layout="wide")
# matches = pd.read_csv('Data\matches.csv')
leagues_stats = pd.read_csv('league_stats.csv')
teams_stats = pd.read_csv('teams_players.csv')
leagues = np.unique(teams_stats['League'])
st.markdown('## Select League ')
selected_league = st.radio( leagues_stats['League'], horizontal=True)
# teams_in_league= teams_stats.loc[teams_stats['League'] == selected_league]
# teams = np.unique(teams_in_league['Team'])
# seasons = np.unique(teams_in_league['Season'])
# selected_team = st.radio('Pick a Team:', teams, horizontal=True)
# selected_season = st.select_slider('Choose season', seasons)
#
#
# dataframe = pd.read_csv('player_stats_dataset.csv')
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
