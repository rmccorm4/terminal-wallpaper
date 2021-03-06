# terminal-wallpaper
Change your desktop wallpaper to a random 1080p background from google images with optional search term

## Requirements
* Python3
* Pip3

## Setup
To install necessary python3 libraries, run:

```
pip3 install -r requirements.txt
```

## Execution
### Random Wallpaper
To get a random wallpaper from your terminal, run:

```
python3 wallpaper.py
```

![Alt Text](images/random.gif?raw=true "Random Example")

### Search for Specific Wallpaper
To get a wallpaper based on a specified search term, run:

```
python3 wallpaper.py -s <search_term>
```

or

```
python3 wallpaper.py --search <search_term>
```

![Alt Text](images/search-term.gif?raw=true "Search Term Example")

### Choosing Which Search Result

By default, the script will choose one of the first 30 results from
the image search. To manually choose which search result to make your
background, such as always choosing the 1st result to get the most
relevant result, run:

```
python3 wallpaper.py --search <search_term> -n <result_number>
```

To get the first result, run:

```
python3 wallpaper.py --search <search_term> -n 0
```

![Alt Text](images/result-number.gif?raw=true "Result Number Example")

### Fun Flag

For those who are trying to find funny wallpapers that might not
necessarily be 1080p, there is a '-f' or '--fun' flag to do so. Run:

```
python3 wallpaper.py --search <search_term> -f
```

or

```
python3 wallpaper.py --search <search_term> --fun
```

![Alt Text](images/fun-flag.gif?raw=true "Fun Flag Example")
