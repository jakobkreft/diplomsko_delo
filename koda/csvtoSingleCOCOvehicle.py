import json

imgHeight = 1180 # t2A sizes
imgWidth = 1576

def makejson(imgWidth, imgHeight, data):
    # create JSON object
    coco_dict = {
        'images': [],
        'categories': [
            {
                'id': 1,
                'name': 'car'
            },
            {
                'id': 2,
                'name': 'truck'
            },
            {
                'id': 3,
                'name': 'bus'
            }
        ],

        'annotations': []
    }

    # add multiple images and annotations to respective lists
    current_img_id = 1
    for current_frame in range(len(data)):
        current_img = {
            'height': imgHeight,
            'width': imgWidth,
            'id': current_img_id,
            'file_name': f'../images/frameCt2A{current_frame+1}.jpg'
        }
        coco_dict['images'].append(current_img)

        # add annotations for the current image
        for i in range(len(data[current_frame])):
            category_id = None
            if data[current_frame][i][1] == "car":
                category_id = 1
            elif data[current_frame][i][1] == "truck":
                category_id = 2
            elif data[current_frame][i][1] == "bus":
                category_id = 3

            if category_id is not None:
                annotation_dict = {
                    'id': len(coco_dict['annotations']) + 1,
                    'image_id': current_img_id,
                    'category_id': category_id,
                    'bbox': [
                        float(data[current_frame][i][3]),
                        float(data[current_frame][i][4]),
                        float(data[current_frame][i][5]) - float(data[current_frame][i][3]),
                        float(data[current_frame][i][6]) - float(data[current_frame][i][4])
                    ],
                    'area': (float(data[current_frame][i][5]) - float(data[current_frame][i][3])) * (float(data[current_frame][i][6]) - float(data[current_frame][i][4]))
                }
                coco_dict['annotations'].append(annotation_dict)

        current_img_id += 1

    # write JSON file
    with open('posnetki/teren3AB/t3ACOCOvehicle.json', 'w') as f:
        json.dump(coco_dict, f, indent=4)

import csv

csv_filename = 'posnetki/teren3AB/t3A_boundingbox.csv'

# Open the CSV file and create a reader object
with open(csv_filename, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Create an empty list to store the data
    data = []

    # Loop over the remaining rows and append to the list
    for row in csv_reader:
        data.append(row)

# get indexes, used to get labels for one picture
newImgStart = []
for x in range(len(data)):
    if data[x][0] == "image":
        newImgStart.append(x + 1)

#print(newImgStart)

groupedData = []

for x in range(len(newImgStart) - 1):
    groupedData.append(data[newImgStart[x]:newImgStart[x+1] - 1])

#print(groupedData[0])
#print(len(groupedData[0]))

# vse slike so tukaj enake velikosti (1562, 1201) 
"""
import os
from PIL import Image

image_folder = "posnetki/teren2AB/t2A"
image_filenames = [f"frameCt2A{i}.jpg" for i in range(1, 7509)]
image_sizes = []

for filename in image_filenames:
    image_path = os.path.join(image_folder, filename)
    with Image.open(image_path) as img:
        image_sizes.append((img.size[0], img.size[1]))

print(image_sizes)
"""

for x in range(len(groupedData)):
    st = int(groupedData[x][0][0][6:])
    print(st, str(x+1))

    if st == x + 1:
        makejson( imgWidth, imgHeight, groupedData[x])
        print("done frame: ", x + 1)
    else:
        print("error, at number:", x + 1)
        break


# """