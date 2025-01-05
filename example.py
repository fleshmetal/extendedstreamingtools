import argparse
import os
import sys
import utils.SESHtools as SESHtools




########################### CHANGE YOUR STUFF HERE! ######################################

MyPickleDirectory = '' # if you have an existing pickle file, set its directory here
MyDataDirectory = ''  # set the path of where your raw data is here

# for this example, we produce two lifetime plots. choose the size, top_n items you would like to observe and the type of item
top_n = 10 
item_type = 'album' # this is between 'album', 'track', and 'artist'

##############################################################################


def main(
    my_pickle_directory = '',
    my_data_directory = '',
    data_exists = False,
    self_directory = os.path.dirname(os.path.realpath(__file__)),  # need a default folder path directory
    pickle_name = None,
    data_directory = None,
    ):


    if my_pickle_directory == '':
        pickle_files = [f for f in os.listdir(self_directory) if f.endswith('.pkl')]
        if pickle_files:
            data_exists = True
            pickle_name = os.path.join(self_directory, pickle_files[0])
            print('Pickled data found in current directory! Generating dataframe from existing pickle.')
    else:
        if os.path.isdir(my_pickle_directory):
            pickle_files = [f for f in os.listdir(my_pickle_directory) if f.endswith('.pkl')]
            if pickle_files:
                data_exists = True
                pickle_name = os.path.join(my_pickle_directory, pickle_files[0])
                print('Pickled data found in specified directory! Generating dataframe from existing pickle.')

    if data_exists == False:
        if my_data_directory == '':
            json_files = [file for file in os.listdir(self_directory) if file.lower().endswith('.json')]
            if json_files:
                data_exists = True
                data_directory = self_directory
            else:
                raise ValueError('No raw data or pickle data found. Please specify file locations in this file.')
        else:
            if os.path.isdir(my_data_directory):
                json_files = [file for file in os.listdir(my_data_directory) if file.lower().endswith('.json')]
                if json_files:
                    data_directory = my_data_directory
                else:
                    raise ValueError('No data or pickle data found. Please specify file locations in this file.')
            else:
                raise ValueError('Specified data directory does not exist. Please check the path.')
    
            
    if pickle_name is not None or data_directory is not None:

        if pickle_name is None:
            print('No pickle found, so generating a default pickle')
            pickle_name = 'myextendedstreaminghistory.pkl'
        
        mydata = SESHtools.getData(data_directory, pickle_name)
        print('Success! Data is collected and stored at root folder.')

        podcasts, music = SESHtools.splitStreams(mydata)

        SESHtools.lifeTimePlot(music, 
                               item_type,
                               top_n, 
                               'count')
        
        SESHtools.lifeTimePlot(music, 
                               item_type,
                               top_n, 
                               'time')


    else:
        raise ValueError('No eligible history data or pickle file found. Please specify file locations in this file.')


if __name__ == "__main__":
    main(
            my_pickle_directory = MyPickleDirectory,
            my_data_directory = MyDataDirectory,
    )
