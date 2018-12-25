cd "$1"
ffmpeg -framerate 30 -i %03d.png -r 30 -pix_fmt yuv420p "$1".mp4
cd ..
