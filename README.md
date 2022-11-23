# INIT

`````bash
git clone https://github.com/Drosscend/Mini-Box
cd Mini-Box
py -m venv Mémoire
.mémoire\Scripts\activate
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
cd ..
`````

# Run

`````python
python detect.py - -source 0

python detect.py - -weights yolov5x.pt - -source 0

python detect.py - -project OUTPUT - -name files - -classes 0 - -source 0 - -view - img - -exist - ok - -save - txt - -save - crop
`````