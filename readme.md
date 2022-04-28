# ASCII Art Video : Bad Apple

This repository was forked from (Chion82/ASCII_bad_apple)[https://github.com/Chion82/ASCII_bad_apple]

## Play ASCII Art Video

```
$ python run.py -i path/to/video_dir
# ex:
$ python run.py -i sample/bad_apple/
```

## Generate ASCII Art Video

```
# Download mp4 file and rename to "video.mp4"

$ python generate generate_ascii_art.py -i path/to/video_dir
# ex:
$ python generate generate_ascii_art.py -i sample/bad_apple/
```

##Dependencies

* To simply run the demo with sound effects, you need ```mplayer``` installed.

* To re-generate the ascii art video source which is ```play.txt```, the following Python dependencies are needed:

> OpenCV with python package installed and well configured.  
> pip package: ```image```
