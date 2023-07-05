import os
import json

def rename_file(filename):
    idx = filename.find('frameC')
    if idx != -1:
        idx += len('frameC')
        next_idx = filename.find('A', idx)
        if next_idx != -1:
            new_filename = filename[:next_idx] + 'B' + filename[next_idx+1:]
            return new_filename
    return filename

def convert_to_coco_format(jsons_folder, output_filename, description):
    coco_dict = {
        "info": {"description": description},
        "licenses": [{"id": 1, "name": "Unknown License"}],
        "images": [],
        "annotations": [],
        "categories": [{"id": 1, "name": "car"}, {"id": 2, "name": "truck"}, {"id": 3, "name": "bus"}]
    }

    image_id = 1
    annotation_id = 1

    for filename in os.listdir(jsons_folder):
        if not filename.endswith(".json"):
            continue
        
        with open(os.path.join(jsons_folder, filename), "r") as f:
            data = json.load(f)
        
        # Add image data to COCO dict
        coco_dict["images"].append({
            "id": image_id,
            "file_name": rename_file(data["images"]["file_name"]),
            "width": data["images"]["width"],
            "height": data["images"]["height"]
        })
        
        # Add annotation data to COCO dict
        for annotation in data["annotations"]:
            coco_dict["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": annotation["category_id"],
                "bbox": annotation["bbox"],
                "area": annotation["area"]
            })
            annotation_id += 1
        
        image_id += 1

    with open(output_filename, "w") as f:
        json.dump(coco_dict, f, indent=4)

database_folder = "database7/"
datasets = ['A', 'B', 'C']
data_types = ['train', 'test']
description_map = {'A': 'Dataset A, teren 1,2,6', 'B': 'Dataset B, teren 1,3,4,6', 'C': 'Dataset C, teren 3,4'}

for dataset in datasets:
    for data_type in data_types:
        jsons_folder = os.path.join(database_folder, f"{dataset}_jsons_{data_type}")
        output_filename = os.path.join(database_folder, f"{dataset}_COCO_{data_type}.json")
        description = f"{description_map[dataset]} {data_type}"
        convert_to_coco_format(jsons_folder, output_filename, description)
