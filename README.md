# Anime-Downloader

Downloads the anime from .m3u8 file by scrapping animeheaven.pro using the episode url and ffmpeg.

### USAGE-

Run main.py and paste url

## TODO

*    change headers.py to headers.txt or json
*    optimize
*    all in one
*    Add progress bar for downloading
*    Add log file per episode/season
*    Add cli arguments for season|episode|perticular episodes, capture output, use perticular server|resolution, custom name for dir|episode, 
*    Add changelog
*    check server|resolution availability and switch ot other server|resolution for perticular server|resolution given by user
*    change multithreading to 20 at a time at max
*    Add option to download episode or not if already one exist of same name ( use -y )
*    Add more websites.

## Requirements

`selenium`
    
    pip install selenium
or
[Download From here](https://pypi.org/project/selenium/), unzip and run
    
    python setup.py install
