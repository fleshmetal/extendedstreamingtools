# Spotify Extended Streaming History Dataset Utils

As most major billion dollar tech companies do in some capacity, the Spotify music streaming platform has been collecting your usage of their service at an extremely granular level. This is, they track each instance of when you start to stream i.e. play a song. Each instance of this play contains a ton of metrics. This utility library is designed to enable users to manipulate and observe this data

## A package for aggregating, analyzing, and preparing your music history.

This is a utility library of functions for handling your data produced from Spotify's Extended Streaming History dataset they produce for you. At this time, 4 major functions are ready to public use. A full pipeline example is also provided with a resultant demonstration. 

## Tools 

1. **getData**: This utility imports, cleans, and pickles your data for future use.
2. **splitStreams**: This utility splits streams between podcasts and music.
3. **lifeTimePlot**: A plotting utility for a lifetime observation of the top-n specified items, be it artists, albums, tracks. This also takes an additional parameters to switch between y-value play counts and play time (currently in hours).  
4. **historicalListeningPlot**:  A plotting utility for a windowed observation of listening trends, be it artists, albums, tracks. This also takes an additional parameters to switch y-value output play counts and play time (currently in hours).  

Visualization utilities depend on the `splitStreams` output of podcasts and songs. Future improvements will ensure visualization arguments are properly met before executing. Given this projects infancy, please be cautious of input requirements and ouput states of these utils.

## Enviroment Setup

This repo requires a few libraries. A requirements.txt file is provided to generate an Nenviroment. To produce your enviroment, run this:

```bash
conda create --name seshenv --file requirements.txt
```
Note that there are a bunch of unused libaries not used in this repo. This is to be cleaned up later.

After you have created the enviroment, activate it:

```bash
conda activate seshenv
```

Finally, navigate to this repos directory on your computer. 

## Example Usage

A demonstration file, `example.py` is is provided to prepare the data for you but also provide two Life Time Plot analytics. By default, it is set to 'albums', but you can change this to in the above in its configuration. 

To run it, run this in a shell inside the folder:

```bash
python example.py 
```

This will also produce a pickle file with default name *myextendedstreaminghistory.pkl*. This pickle file will be default referenced from the root folder of the util repo. Another example will be provided later to demonstrate the historical listening plot, from import to read out.

## Upcoming utils

Additional utils are being tuned up to observe genre, in a similar capacity to the Historical Listening Plot. 