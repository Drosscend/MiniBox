import time
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

type_to_detect = 0  # 0 = personne, 1 = vélo
model.classes = [type_to_detect]

results = model('OUTPUT/photo.jpg')

data = results.pandas().xyxy[0]

data = data.drop(columns=['name', 'confidence', 'class'])

date = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
tab_of_positions = data.values.tolist()
nb_personnes = len(tab_of_positions)

with open('OUTPUT/data.csv', 'a') as f:
    # si le fichier est vide, on écrit l'entête
    if f.tell() == 0:
        f.write("date,occurence,type,positions\n")
    f.write(date + ',' + str(nb_personnes) + ',' + str(type_to_detect) + ',' + str(tab_of_positions) + '\r')
