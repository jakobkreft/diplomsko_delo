import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import csv
import json
import shutil



class ImageSequenceViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Sequence Viewer")
        self.image_list = []
        self.current_index = 0

        #bbox
        self.handbbox = [[0,0],[0,0]]
        self.handbb_index = 0
        
        # Create canvas for displaying images
        self.canvas = tk.Canvas(self.master, width=1300, height=1000, cursor="plus")
        self.canvas.pack(side=tk.LEFT)
        
        # Create buttons for navigation and saving
        self.frame = tk.Frame(self.master)
        self.frame.pack(side=tk.RIGHT, padx=10)



        style = ttk.Style()
        style.configure('Custom.TButton', foreground='#000000', background='#f1c232', font=('Calibri', 12))
        
        self.prev_button = ttk.Button(self.frame, text="Jump To Frame", command=self.jump_to_frame, style='Custom.TButton')
        self.prev_button.pack(pady=10)

        
        self.prev_button = ttk.Button(self.frame, text="Prev", command=self.show_previous_image, style='Custom.TButton')
        self.prev_button.pack(pady=10)
        

        self.next_button = ttk.Button(self.frame, text='Next', command=self.show_next_image, style='Custom.TButton')
        self.next_button.pack(pady=10)
        
        self.save_button = ttk.Button(self.frame, text="Save", command=self.save_image, style='Custom.TButton')
        self.save_button.pack(pady=10)
        
        # Create a label and entry for the text box
        self.number_label = ttk.Label(self.frame, text="Enter ID number:",  font=('Calibri', 12))
        self.number_label.pack(pady=10)
        self.number_entry = tk.Entry(self.frame)
        self.number_entry.pack(pady=10)

        self.save_button = ttk.Button(self.frame, text="Export to DB", command=self.export_to_db, style='Custom.TButton')
        self.save_button.pack(pady=10)
  

        # Create a frame for showing the list of entries
        self.list_frame = tk.Frame(self.master, width=400, height=1000)
        self.list_frame.pack(side=tk.RIGHT, padx=10)
        
        # Create a label for the entry list
        self.list_label = ttk.Label(self.list_frame, text="History of commands", font=('Calibri', 12))
        self.list_label.pack(pady=10)
        
        # Create a text widget for displaying the list of entries
        self.entry_text = tk.Text(self.list_frame, width=30, height=30)
        self.entry_text.pack(pady=10)
        
        self.load_images()
        self.show_current_image()

        # bind the left mouse button event to the canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Bind right arrow keypress to a function
        self.master.bind("<Right>", self.show_next_image)
        # Bind right arrow keypress to a function
        self.master.bind("<Left>", self.show_previous_image)

        # Bind "s" keypress to a function
        self.master.bind("s", self.save_image)

        self.master.bind("e", self.export_to_db)

        self.master.bind("f", self.show_next_image)

        self.master.bind("<Return>", self.save_image)


    def jump_to_frame(self):
        toFrame = int(self.number_entry.get())
        # Display the frame image
        self.current_index = (toFrame-1) % len(self.image_list)
        self.show_current_image()
        self.number_entry.delete(0, tk.END)





    def load_images(self):
        # Load the images from the directory
        folder_path = "posnetki/teren6AB/t6Abbcoco/" #nextset
        for i in range(1, 7509):
            filename = "frameCt6Abb{}.jpg".format(i) #nextset
            filepath = os.path.join(folder_path, filename)
            if os.path.exists(filepath):
                self.image_list.append(filepath)
            else:
                print("File not found: {}".format(filepath))
    
    def show_current_image(self):
        # Display the current image on the canvas
        img_x = 1569 #nextset
        img_y = 1198 #nextset
        img = Image.open(self.image_list[self.current_index])
        img = img.resize((int(img_x/1.25), int(img_y/1.25)), Image.LANCZOS) # 
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk
        
    def show_next_image(self, event=None):
        print("show next image")
        # Display the next image in the sequence
        self.current_index = (self.current_index + 1) % len(self.image_list)
        self.show_current_image()
        
    def show_previous_image(self, event=None):
        # Display the previous image in the sequence
        self.current_index = (self.current_index - 1) % len(self.image_list)
        self.show_current_image()

    def export_to_db(self, event=None):
        print("dela")
        file_path = "posnetki/teren6AB/t6A/frameCt6A{}.jpg".format(self.current_index + 1) #nextset
        dest_folder = "database_images/"
        shutil.copy(file_path, dest_folder)
        file_path = "posnetki/teren6AB/t6AbbRjson/frameCt6A{}.json".format(self.current_index + 1) #nextset
        dest_folder = "database_jsons/"
        shutil.copy(file_path, dest_folder)
        file_path = "posnetki/teren6AB/t6Abbcoco/frameCt6Abb{}.jpg".format(self.current_index + 1) #nextset
        dest_folder = "database_bb_images/"
        shutil.copy(file_path, dest_folder)

        # Draw a checkmark at the center of the image
        check_size = 100
        # Get the center coordinates of the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        x = canvas_width // 2
        y = canvas_height // 2
        check_x1 = x - check_size//2
        check_y1 = y - check_size//2
        check_x2 = x + check_size//2
        check_y2 = y + check_size//2
        self.canvas.create_line(check_x1, y, x, check_y2, width=25, fill="#7fff00", joinstyle="round", capstyle="round")
        self.canvas.create_line(x, check_y2, check_x2, check_y1, width=25, fill="#7fff00", joinstyle="round", capstyle="round")

    def save_image(self, event=None):
        numbers = ""
        # Save the name of the current image and the number entered in the text box to a CSV file
        filename = "frameCt6A{}.jpg".format(self.current_index + 1) #nextset
        numbers = self.number_entry.get()
        numbers = ''.join(c for c in numbers if c.isdigit() or c == ',')

        with open('sampledatabase.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([filename, numbers])
        self.show_saved_entries()
        print("numbers empty: ", numbers)
        number_list = []
        if numbers:
            number_list = [int(n) for n in numbers.split(",")]
        self.remove_id_from_json(self.current_index + 1, number_list)
        self.cocobbox(self.current_index + 1, "6") #nextset
        self.show_current_image()

        self.number_entry.delete(0, tk.END)
        print("done,showed")

    def show_saved_entries(self):
        # Clear the current text in the text widget
        self.entry_text.delete(1.0, tk.END)

        # Load the saved entries from the CSV file and display them in the text widget
        with open('sampledatabase.csv', mode='r') as file:
            reader = csv.reader(file)
            entries = list(reader)
            for row in reversed(entries):
                self.entry_text.insert(tk.END, "{}: {}\n".format(row[0], row[1]))

    def remove_id_from_json(self,x, remove_id):

        try:
            # Open the JSON file
            with open(f"posnetki/teren6AB/t6AbbRjson/frameCt6A{x}.json") as f: #nextset
                data = json.load(f)
 
        except:
            # Open the JSON file
            with open(f"posnetki/teren6AB/t6ACOCOvehicle/frameCt6A{x}.json") as f: #nextset
                data = json.load(f)

        # Remove the annotation with the specified id
        annotations = [ann for ann in data['annotations'] if ann['id'] not in remove_id]
        data['annotations'] = annotations

        # Save the modified JSON file
        new_json_path = f"posnetki/teren6AB/t6AbbRjson/frameCt6A{x}.json" #nextset
        with open(new_json_path, 'w') as f:
            json.dump(data, f, indent=4)

    def add_id_to_json(self,image_index, bbox_info, FOL ):
        try:
            with open(f'posnetki/teren{FOL}AB/t{FOL}AbbRjson/frameCt{FOL}A{image_index}.json', 'r') as f:
                coco_dict = json.load(f)
        except:
            with open(f'posnetki/teren{FOL}AB/t{FOL}ACOCOvehicle/frameCt{FOL}A{image_index}.json', 'r') as f:
                coco_dict = json.load(f)
        # convert bbox_info from [[x1,y1],[x2,y2]] format to [x, y, w, h] format
        x1, y1 = bbox_info[0]
        x2, y2 = bbox_info[1]
        x, y = min(x1, x2), min(y1, y2)
        w, h = abs(x2 - x1), abs(y2 - y1)

        # add new bounding box
        try:
            max_id = max(anno['id'] for anno in coco_dict['annotations'])
        except:
            max_id = 0
        new_anno = {
            'id': max_id + 1,
            'image_id': coco_dict['images']['id'],
            'category_id': 1, # 'car' category ID
            'bbox': [x, y, w, h],
            'area': w * h
        }
        coco_dict['annotations'].append(new_anno)

        # save updated JSON file
        with open(f'posnetki/teren{FOL}AB/t{FOL}AbbRjson/frameCt{FOL}A{image_index}.json', 'w') as f:
            json.dump(coco_dict, f, indent=4)

        print("done added new bb")


    def on_canvas_click(self, event):
        # Get the x and y coordinates of the mouse click
        x = event.x
        y = event.y

        img_x = int(x*1.25)
        img_y = int(y*1.25)

        # Save the clicked point to self.handbbox
        if self.handbb_index == 0:
            self.handbb_index = 1
            self.handbbox = [[img_x,img_y],[0,0]]
        else:
            self.handbb_index = 0
            self.handbbox[1] = [img_x, img_y]

            # Add new bbox to the JSON file
            self.add_id_to_json(self.current_index + 1, self.handbbox, "6") #nextset

            # Save the image
            self.save_image()

            # Reset self.handbbox
            self.handbbox = None

            print("Done saving image with new bounding box:", self.handbbox)

            
        # Create a text label with the x and y coordinates
        label = "x: {}, y: {}".format(img_x, img_y)
        
        # Remove any existing label from the canvas
        self.canvas.delete("coords")
        
        # Offset the label from the mouse click position
        label_x = 1250
        label_y = 20
        
        # Display the label on the canvas at the offset position
        self.canvas.create_text(label_x, label_y, text=label, fill="red", tags="coords")
        
        # Draw a cross or T-shaped lines to indicate the location
        self.canvas.create_line(x-55, y, x+55, y, width=1, fill="red")
        self.canvas.create_line(x, y-55, x, y+55, width=1, fill="red")

    def cocobbox(self, x, FOL):
        # Path to JSON file
        max_id = 0
        xs = str(x)
        path = "posnetki/teren{FOL}AB/t{FOL}AbbRjson/frameCt{FOL}A{xs}.json".format(FOL=FOL, xs=xs)
        #print(path)
        # Path to image
        image_path = "posnetki/teren{FOL}AB/t{FOL}A/frameCt{FOL}A{xs}.jpg".format(FOL=FOL, xs=xs)

        # Open the JSON file
        with open(path) as f:
            data = json.load(f)

        # Open the image
        image = Image.open(image_path)

        # Get the drawing context
        draw = ImageDraw.Draw(image)

        # Define some colors
        id_colors = [(214, 39, 40), (148, 103, 189), (44, 160, 44), (31, 119, 180), (255, 127, 14), (227, 119, 194), (188, 189, 34), (23, 190, 207), (140, 86, 75), (127, 127, 127), (247, 182, 210), (219, 219, 141), (214, 39, 40), (148, 103, 189), (44, 160, 44), (31, 119, 180), (255, 127, 14), (227, 119, 194), (188, 189, 34), (23, 190, 207), (140, 86, 75), (127, 127, 127), (247, 182, 210), (219, 219, 141), (214, 39, 40), (148, 103, 189), (44, 160, 44), (31, 119, 180), (255, 127, 14), (227, 119, 194), (188, 189, 34)]
        bbox_color = (0, 255, 0, 128)  # green with alpha=128
        text_color = (255, 124, 0)  # red
        font = ImageFont.truetype("arial.ttf", 36)
        font_label = ImageFont.truetype("arial.ttf", 20)

        # Map category IDs to category names
        category_map = {}
        for category in data["categories"]:
            category_map[category["id"]] = category["name"]

        # Iterate over the annotations
        for annotation in data["annotations"]:
            label = category_map[annotation["category_id"]] +" "+ str(annotation["id"])
            bbox = annotation["bbox"]
            #print(bbox)
            if annotation["id"] > max_id:
                max_id = annotation["id"]
                print(x,":",max_id)



            # Draw the bounding box
            draw.rectangle([bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]], outline=id_colors[annotation["id"]], width=2)

            # Add the label
            draw.text((bbox[0], bbox[1]), label.upper(), fill=text_color, font=font_label)

        draw.text((15, 15), "frameCt{FOL}A{xs}".format(FOL=FOL, xs=xs), fill=(255,230,0), font=font)

        # Add a label at the bottom of the image
        bottom_margin = 30
        label_font = ImageFont.truetype("arial.ttf", 20)
        label_height = label_font.getsize("A")[1]
        num_colors = len(id_colors)
        color_box_width = image.width // num_colors
        for i in range(num_colors):
            # Draw the colored box
            color_box = (i*color_box_width, image.height-bottom_margin, (i+1)*color_box_width, image.height)
            draw.rectangle(color_box, fill=id_colors[i], outline=(0,0,0), width=2)

            # Draw the index label
            index_label = str(i)
            label_width = label_font.getsize(index_label)[0]
            label_x = color_box[0] + (color_box_width - label_width) // 2
            label_y = image.height - bottom_margin + (bottom_margin - label_height) // 2
            draw.text((label_x, label_y), index_label, fill=(0,0,0), font=label_font)



        # Show the image
        #image.show()

        # Save the image
        image.save("posnetki/teren{FOL}AB/t{FOL}Abbcoco/frameCt{FOL}Abb{xs}.jpg".format(FOL=FOL, xs=xs))
        print("done frame:",x, "posnetki/teren{FOL}AB/t{FOL}Abbcoco/frameCt{FOL}Abb{xs}.jpg".format(FOL=FOL, xs=xs))


                

root = tk.Tk()


# Load the custom image
cross_img = tk.PhotoImage(file="cursor.png")

# Set the mouse pointer to the custom image
#root.config(cursor="plus")

app = ImageSequenceViewer(root)
root.mainloop()
