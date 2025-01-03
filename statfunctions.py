import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def split_streams(df):
    """
    This utility is designed to split the processed Extended Steaming History data into two dataframes: 
    1. Podcasts 
    2. Music

    This split is done by checking for rows with the 'episode_name' column either being NaN. If the episode is 'NaN' it is assumed to
    be a podcast. If it is a pod

    Parameters:
        df (pd.DataFrame): The original processed Extended Steaming History dataframe.

    Returns:
        tuple: Two DataFrames, one for Podcasts another for Music
    """
    # first podcasts
    df_not_none = df[df["episode_name"].notna()] # get the rows 
    podcasts = df_not_none.drop(["master_metadata_track_name", "master_metadata_album_artist_name", "master_metadata_album_album_name", "spotify_track_uri"], axis=1) # clean it up

    # then music
    df_none = df[df["episode_name"].isna()] # get the
    music = df_none.drop(["episode_name", "episode_show_name", "spotify_episode_uri"], axis=1) # clean it up

    return podcasts, music


def histogramstats(df: pd.DataFrame, type: str, length: int = 10, stat: str = 'count'):

    select = None
    if type == 'album':
        select = 'master_metadata_album_album_name'
        label = 'Albums'
    elif type == 'artist':
        select = 'master_metadata_album_artist_name'
        label = 'Artists'
    elif type == 'track' or type == 'song':
        select = 'master_metadata_track_name'
        label = 'Tracks'
    else:
        print('Not a proper selection. ')
        return
    

    if stat == 'time':
            
        agg_data = df.groupby(select)['ms_played'].sum().sort_values(ascending=False)
        agg_data = agg_data / (1000 * 60 * 60)  # Convert milliseconds to minutes

        plt.figure(figsize=(12, 6), dpi=400)
        agg_data.head(length).plot(kind='bar')
        plt.title(f'Total Play Time for Your Top {length} {label}')
        plt.xlabel(f'{label} Name')
        plt.ylabel('Total Play Time (hours)')
        plt.xticks(rotation=90)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    else:

        artist_occurances = df[select].value_counts().head(length)

        plt.figure(figsize=(12, 6), dpi=400)
        artist_occurances.plot(kind='bar')
        plt.title(f'Number of Plays for Your Top {length} {label}')
        plt.xlabel(f'{label} Name')
        plt.ylabel('Number of times played')
        plt.xticks(rotation=90)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()


    return 


def historicallisteningplot(
    df = None,
    start_date = None,
    end_date = None,
    selection = None,
    metric_selection = None,
    topn = 5
    ):
    
    style_dict = {
        'master_metadata_track_name': 'Track',
        'master_metadata_album_album_name': 'Album',
        'master_metadata_album_artist_name': 'Artist',
        'daily_count': 'Plays',
        'daily_runtime': 'Listening Time (min)'
    }
    
    # WHAT IF IT WAS PURPLE!!
    colors = ['mediumpurple', 'lightgreen', 'skyblue', 'tomato', 'lightpink'] 

    
    df['date'] = pd.to_datetime(df['ts'])

    # first get the items in the selected window
    windowed_data = df[(df['ts'] >= start_date) & (df['ts'] <= end_date)]

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # generating aggregated data. this will be functionaized later. 
    # this is to produce a 'count' and 'time' feature to search against.
    windowed_aggregated_data = windowed_data.groupby(selection).agg(
        daily_count=(selection, 'size'),
        daily_runtime=('ms_played', 'sum')
    ).reset_index()

    # get the top grouped items given a sort against our metric selection
    top_grouped = windowed_aggregated_data.sort_values(by=metric_selection, ascending=False).head(topn)
    top_grouped_list = top_grouped[selection].tolist()

    # get the data of the top_n artists in the windowed_data thats in our top grouped list 
    top_n_windowed_data = windowed_data[windowed_data[selection].isin(top_grouped_list)]

    # calculate individual date times 
    top_n_windowed_data['date'] = top_n_windowed_data['ts'].dt.date
    top_n_windowed_data_daily = top_n_windowed_data.groupby([selection, 'date']).agg(
        daily_count=(selection, 'size'),
        daily_runtime=('ms_played', 'sum')
    ).reset_index()

    # convert daily_runtime 
    top_n_windowed_data_daily['daily_runtime'] = top_n_windowed_data_daily['daily_runtime'] / (1000 * 60)

    plt.figure(figsize=(12, 6), dpi=400)
    for i, track in enumerate(top_grouped_list):

        track_data = top_n_windowed_data_daily[top_n_windowed_data_daily[selection] == track] # get data for the current item
        
        track_data_within_window = track_data[(track_data['date'] >= start_date.date()) & (track_data['date'] <= end_date.date())] #filter data within the window
        
        # plot the basic stuff.
        plt.plot(track_data_within_window['date'], track_data_within_window[metric_selection], color=colors[i], label=f"{track}") 
        
        # put a scatter point on the end points of the data ranges
        if not track_data_within_window.empty:
            plt.scatter([track_data_within_window['date'].iloc[0], track_data_within_window['date'].iloc[-1]], 
                        [track_data_within_window[metric_selection].iloc[0], track_data_within_window[metric_selection].iloc[-1]], 
                        color=colors[i],
                        zorder=5)
            
        
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Now showing out of bounds connections 
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # get the nearest available datapoints before the search window
        track_data_before_window = df[
            (df[selection] == track) &
            (df['date'] < start_date)
        ].groupby([selection, df['date'].dt.date]).agg(
            daily_count=(selection, 'size'),
            daily_runtime=('ms_played', 'sum')
        ).reset_index()

        track_data_before_window['daily_runtime'] = track_data_before_window['daily_runtime'] / (1000 * 60)

        # this draws a line to the nearest available datapoint outside (before) the window. this is designed to show 
        # a connection that has been generated over time 
        if not track_data_before_window.empty:
            plt.plot(
                [track_data_before_window['date'].iloc[-1], track_data_within_window['date'].iloc[0]],
                [track_data_before_window[metric_selection].iloc[-1], track_data_within_window[metric_selection].iloc[0]],
                linestyle='--', color='gray', alpha=0.6
            )

        # get the nearest available datapoints after the search window
        track_data_after_window = df[
            (df[selection] == track) &
            (df['date'] > end_date)
        ].groupby([selection, df['date'].dt.date]).agg(
            daily_count=(selection, 'size'),
            daily_runtime=('ms_played', 'sum')
        ).reset_index()

        track_data_after_window['daily_runtime'] = track_data_after_window['daily_runtime'] / (1000 * 60)

        # this draws a line to the nearest available datapoint outside (after) the window. this is designed to show 
        # a connection that has been generated over time 
        if not track_data_after_window.empty:
            plt.plot(
                [track_data_within_window['date'].iloc[-1], track_data_after_window['date'].iloc[0]],
                [track_data_within_window[metric_selection].iloc[-1], track_data_after_window[metric_selection].iloc[0]],
                linestyle=':', color='gray', alpha=0.6
            )

    plt.xlabel('Date')
    plt.ylabel(f'{style_dict[metric_selection]}')
    plt.title(f'Daily {style_dict[metric_selection]} for Your Top {topn} {style_dict[selection]}(s)')
    plt.xlim(start_date, end_date)
    plt.xticks(rotation=50)
    plt.legend()
    plt.grid(True)
    plt.show()
