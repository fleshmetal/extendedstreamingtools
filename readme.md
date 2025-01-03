# extendedstreamingtools

## A package for aggregating, analyzing, and preparing your music history.

This is a library of functions for handling your data produced from Spotify's Extended Streaming History dataset for you. 

## Importing Files & Processing 

A utility for file importing is designed to prepare the data in a manner that tabulates all Extended Streaming History Data into a single Pandas DataFrame. This utility is the first step in the `main.py` file. A required `folder_path` argument is required to point the program towards your data. There are additional arguments, please see the help of the argument for more detail.

An example usage is the following:

```bash
python main.py /Users/fleshmetal/Documents/Datasets/extendedstreaminghistory
```

This will produce a pickle file with default name *myextendedstreaminghistory.pkl*. This pickle file will be default referenced from the root folder of the util repo. However, data observation utilities will allow for specific location referencing, if you choose to move the dataset around. 

To process the output pickle, you will need to unpickle the dataframe and feed it into `splitstreams()` function. This function is designed to split the dataframe between podcasts and music. Once the data has been split, it will be ready to feed into the availabile utilities. 

## Available Tools 

There are two initial visualization utilities available to observe your Spotify data. These utilities can be found in `statfunctions.py`. Each utilitie serves a specific function.  
