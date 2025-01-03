import argparse
import os
import sys
from SpotifyPreprocessor import SpotifyPreprocessor

def main():

    script_dir = os.path.dirname(os.path.realpath(__file__)) # need a default folder path directory

    parser = argparse.ArgumentParser(description="Process Spotify Extended Streaming History.") # parser for main

    # arg for extended data folder path. defaults to self
    parser.add_argument(
        "folder_path",
        nargs='?',
        default=script_dir,
        help="Path to the folder containing JSON files. Defaults to the script's directory."
    )

    # optional arg for  the pickle location
    parser.add_argument(
        "--pickle_path",
        help="Path to the folder for the pickle file. Defaults to the script's directory if not provided."
    )

    # optional arg for pickle name
    parser.add_argument(
        "--pickle_name",
        default="mycombinedstreaminghistory.pkl",
        help='Name of the pickle file. Defaults to "mycombinedstreaminghistory.pkl".'
    )

    args = parser.parse_args()

    # check if the folder path is real
    if not os.path.isdir(args.folder_path):
        print(f"Error: The folder path '{args.folder_path}' does not exist or is not a directory.")
        sys.exit(1)


    # still no pickles!
    if args.pickle_path:
        if os.path.isdir(args.pickle_path):
            pickle_full_path = os.path.join(args.pickle_path, args.pickle_name)
        else:
            pickle_full_path = args.pickle_path
    else:
        pickle_full_path = os.path.join(script_dir, args.pickle_name)

    # check for the json files in the selected folder path
    json_files = [file for file in os.listdir(args.folder_path) if file.lower().endswith('.json')]
    if not json_files:
        print(f"No JSON files found in the specified folder: '{args.folder_path}'.")
        sys.exit(1)

    # finally process the data
    df = SpotifyPreprocessor(args.folder_path, pickle_full_path)
    print("DataFrame processing complete. Shape:", df.shape)

if __name__ == "__main__":
    main()
