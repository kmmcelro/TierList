import os
import sys
from PIL import ImageTk, Image, ImageGrab
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import time

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # colors
        self.bg_color = "#151515"

        # standard font
        self.tier_font = "Helvecita"

        # basic setup
        self.title("Tier List")
        self.geometry("1300x900")
        self.resizable(0, 0)
        self.width = 1300
        self.height = 900
        self.tier_width = 900
        
        # colors
        self.colors = ["#c95444", "#ff8000", "#ffa900", "#ffff00", "#b5e61d", "#15d15d", "#00a2e8"]
        self.standard_tiers = ["S", "A", "B", "C", "D", "E", "F"]

        # frames (not necessary but allows for easy creation of multiple frames)
        container = tk.Frame(self)
        container.place(x=0, y=0, width=self.width, height=self.height)
        self.frames = {"MAIN" : MainPage(container, self),
                       "SETTINGS" : SettingsPage(container, self)}

        self.frames["SETTINGS"].tkraise()

    def initialise_frame(self, frame_object, image=None): # for all the basic setup stuff in frames
        frame_object.place(x=0, y=0, width=self.width, height=self.height) # 
        frame_object.configure(bg=self.bg_color)

        if image != None: # for making it easier to initialise a frame with a background
            background_gif = tk.PhotoImage(file=self.resource_path(image))
            background = tk.Label(frame_object, image=background_gif, borderwidth=0, highlightthickness=0)
            background.image = background_gif # keep reference to image
            background.place(x=0, y=0)

    def resource_path(self, relative_path): # copied from stackoverflow, for making the program a .exe in future
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS # PyInstaller creates a temp folder and stores path in _MEIPASS
            
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        #intialise
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.initialise_frame(self) # use a image for the 'grid' , "background.png"

        # fonts
        self.text_font = (self.controller.tier_font, 14)
        self.title_font = (self.controller.tier_font, 32)
        self.button_font = (self.controller.tier_font, 40) # initial font for each tier
        
        # tier size
        self.tier_height = 73

        # widgets
        self.title = tk.Label(self, text="My Tier List", font=self.title_font, fg="white", bg=self.controller.bg_color, cursor="hand2")
        self.title.bind("<Button-1>", self.edit_title)
        self.title.place(x=5, y=5, width=890, height=92) # place the title perfectly inside the borderlines

        # create tier buttons, dims = 165x75
        self.buttons = []
        self.tier_bounds = []
        
        # Initizing the tier list with all the tiers
        for i in range(len(self.controller.colors)):
            button = tk.Label(self, text=self.controller.standard_tiers[i], font=self.button_font, bg=self.controller.colors[i], wraplength=192, cursor="hand2")
            button.bind("<Button-1>", lambda event, i=i: self.edit_tier(event, self.buttons[i][0]))
            
            label = tk.Label(self,bg="black")
            
            self.tier_bounds.append([(i*80)+104,(i*80)+100,(i*80)+107+self.tier_height])
            self.buttons.append([button, label])
            
            button.place(x=6, y=(i*80)+104, width=192, height=self.tier_height)
            label.place(x=204,y=(i*80)+102, width=690, height=self.tier_height+4)
            
            
        # settings
        self.settings_button = tk.Button(self, text="SETTINGS", command=lambda: self.controller.frames["SETTINGS"].tkraise(), font=self.title_font, fg="grey", bg=self.controller.bg_color, cursor="hand2")
        self.settings_button.place(x=900, y=100)    
        
        # load images
        self.load_button = tk.Button(self, text="LOAD FOLDER", command=lambda: self.load_image(), font=self.title_font, fg="green", bg=self.controller.bg_color, cursor="hand2")
        self.load_button.place(x=900, y=200)
        
        # load one image
        self.load_button = tk.Button(self, text="LOAD PICTURE", command=lambda: self.load_one_image(), font=self.title_font, fg="green", bg=self.controller.bg_color, cursor="hand2")
        self.load_button.place(x=900, y=300)
        
        # save tier list
        self.save_button = tk.Button(self, text="SAVE", command=lambda: self.save_tier(), font=self.title_font, fg="blue", bg=self.controller.bg_color, cursor="hand2")
        self.save_button.place(x=900, y=400)
            

    def load_image(self): # load and format image for label
        #image_dir = filedialog.askopenfilename(initialdir=os.getcwd(), title="Load Image", filetypes=(("PNG Images", ".png"), )) # load png directory
        images_dir = filedialog.askdirectory(initialdir=os.getcwd())
        if images_dir == "": # if filedialog was closed
            return
        filelist=os.listdir(images_dir)
        xpos = 10
        ypos = self.tier_bounds[-1][2] + 5
        for image in filelist[:]: # filelist[:] makes a copy of filelist.
            image_dir = images_dir + "/" + image
            if not(image.endswith(".png")) or image.endswith("_resized.png"):
                #filelist.remove(image)
                continue
            resized_dir = image_dir[:-4] + "_resized.png" # create new png for resized image by removing .png extension first
            if not image_dir[:-4].endswith("_resized"): # check if file is already resized
                preimage = Image.open(image_dir)
                preimage_tk = ImageTk.PhotoImage(preimage)
                ratio = preimage_tk.width()/preimage_tk.height() # to maintain the current aspect ratio on the image
                resized_width = int(ratio*self.tier_height)
                resized = Image.open(image_dir).resize((resized_width, self.tier_height)) # slightly less than height to allow for error
                resized.save(resized_dir)
                image = tk.PhotoImage(file=resized_dir)

            else:
                image = tk.PhotoImage(file=image_dir)

            label = tk.Label(self, image=image, cursor="fleur", borderwidth=0, highlightthickness=0)
            label.image = image # keep reference of image
            label.place(x=xpos, y=ypos) # place at the bottom
            self.make_draggable(label)
            xpos += resized_width
            print(xpos)
            print(self.controller.width)
            if xpos >= self.controller.width - resized_width: # so the images aren't loaded off the window
                print(xpos)
                xpos = 10
                ypos += 78
                if ypos >= self.controller.height - 78: # if there's too many to put neatly starting stacking them
                    ypos = self.tier_bounds[-1][2] + 5
            
        #print(filelist) # Debug
        
    def load_one_image(self):
        image_dir = filedialog.askopenfilename(initialdir=os.getcwd(), title="Load Image", filetypes=(("PNG Images", ".png"), )) # load gif directory

        if image_dir == "": # if filedialog was closed
            return

        resized_dir = image_dir[:-4] + "_resized.png" # create new gif for resized image by removing .gif extension first
        
        if not image_dir[:-4].endswith("_resized"): # check if file is already resized
            preimage = Image.open(image_dir)
            preimage_tk = ImageTk.PhotoImage(preimage)
            ratio = preimage_tk.width()/preimage_tk.height() # to maintain the current aspect ratio on the image
            resized_width = int(ratio*self.tier_height)
            resized = Image.open(image_dir).resize((resized_width, self.tier_height)) # slightly less than height to allow for error
            resized.save(resized_dir)
            image = tk.PhotoImage(file=resized_dir)

        else:
            image = tk.PhotoImage(file=image_dir)

        label = tk.Label(self, image=image, cursor="fleur", borderwidth=0, highlightthickness=0)
        label.image = image # keep reference of image
        xpos = 10
        ypos = self.tier_bounds[-1][2] + 5
        label.place(x=xpos, y=ypos) # place in the space the first image goes when you load the whole folder top left in the box

        self.make_draggable(label)    
    

    # drag functions copied from stackoverflow 
    def make_draggable(self, widget): 
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)

    def on_drag_start(self, event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def on_drag_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        
        if y < self.tier_bounds[0][1]:
            y = self.tier_bounds[0][0]
        # fix positions between borders to place and limit from overlapping labels                
        for tier in self.tier_bounds: # tier is [object location, min pixel position in range, max pixel position in range]
            if tier[1] < y < tier[2]:
                y = tier[0]
                
        if y < self.tier_bounds[-1][2] and x < 204:
            x = 204

        widget.place(x=x, y=y)

    # create new instance of toplevel class to configure parts
    def edit_title(self, event):
        ConfigureTitle(self)

    def edit_tier(self, event, button):
        ConfigureTier(self, button)
        
    def save_tier(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        width = self.controller.tier_width  #get details about window
        takescreenshot = ImageGrab.grab(bbox=(x, y, x + width, y + self.tier_bounds[-1][2] + 5))
        timestr = time.strftime("%Y%m%d%H%M%S")
        save_location = os.getcwd() + "\Tiers\\" + self.title.cget("text") + "_" + timestr + ".png"
        takescreenshot.save(save_location)
        
    def edit_tierlist(self, button_status): # to allow for tiers to be removed or added back into the tierlist default includes S and A-F
        i = 0
        self.tier_bounds = []
        for j in range(0,len(button_status)):
            status = button_status[j]
            [button, label] = self.buttons[j]
            if status:
                self.tier_bounds.append([(i*80)+104,(i*80)+100,(i*80)+107+self.tier_height])
                button.place(x=6, y=(i*80)+104, width=192, height=self.tier_height)
                label.place(x=204,y=(i*80)+102, width=690, height=self.tier_height+4)
                i += 1
            else:
                button.place(x=6, y=-104, width=192, height=self.tier_height)
                label.place(x=204,y=-102, width=690, height=self.tier_height+4)

        
class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        # initialise
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.initialise_frame(self)

        # fonts
        self.input_font = (self.controller.tier_font, 32)
        self.button_font = (self.controller.tier_font, 40)
        self.title_font = (self.controller.tier_font, 32)
        self.tier_font = (self.controller.tier_font, 20) # initial font for each tier

        # Renaming the tierlist
        title_label = tk.Label(self, text="Tier List Title:", font=self.title_font, fg="white", bg=self.controller.bg_color)
        title_label.place(x=275, y=75)
        self.title_var = tk.StringVar()
        tier_title = tk.Entry(self, textvariable=self.title_var, width=10, font=self.input_font)
        tier_title.place(x=700, y=75)
        
        # Tier Status Variables
        self.S_status = tk.BooleanVar()
        self.A_status = tk.BooleanVar()
        self.B_status = tk.BooleanVar()
        self.C_status = tk.BooleanVar()
        self.D_status = tk.BooleanVar()
        self.E_status = tk.BooleanVar()
        self.F_status = tk.BooleanVar()
        self.S_status.set(True)
        self.A_status.set(True)
        self.B_status.set(True)
        self.C_status.set(True)
        self.D_status.set(True)
        self.E_status.set(True)
        self.F_status.set(True)
        self.tier_status_list = [self.S_status, self.A_status, self.B_status, self.C_status, self.D_status, self.E_status, self.F_status]
        
        # Tier name variables
        self.stier_title_var = tk.StringVar()
        self.atier_title_var = tk.StringVar()
        self.btier_title_var = tk.StringVar()
        self.ctier_title_var = tk.StringVar()
        self.dtier_title_var = tk.StringVar()
        self.etier_title_var = tk.StringVar()
        self.ftier_title_var = tk.StringVar()
        self.tier_title_list = [self.stier_title_var, self.atier_title_var, self.btier_title_var, self.ctier_title_var, self.dtier_title_var, self.etier_title_var, self.ftier_title_var]
        
        # Constant parameters for each tier
        self.tier_label_list = ["S Tier Label:", "A Tier Label:", "B Tier Label:", "C Tier Label:", "D Tier Label:","E Tier Label:", "F Tier Label:"]
        self.colors = self.controller.colors
        tier_name_list = self.controller.standard_tiers
        
        # Tier Status checkboxes to select the desired tiers and the textboxes to change the tier names
        ypos = 200
        for i in range(0,len(self.colors)):
            if i > 3:
                xi = 550
            else:
                xi = 0
            tier = tk.Checkbutton(self, text = tier_name_list[i], variable = self.tier_status_list[i], command=lambda:self.tier_flag(), font=self.tier_font, bg=self.colors[i], activebackground=self.colors[i], height=1, width = 5, justify="left")
            tier.place(x=100+xi, y=ypos) 
            tier_label = tk.Label(self, text=self.tier_label_list[i], font=self.tier_font, fg="white", bg=self.controller.bg_color)
            tier_label.place(x=260+xi, y=ypos)
            tier_title = tk.Entry(self, textvariable=self.tier_title_list[i], width=10, font=self.tier_font)
            tier_title.place(x=450+xi, y=ypos)
            if i == 3:
                ypos = 200
            else:
                ypos += 80
        
        # Initizing the checkbutton parameters to a list to make them easier to reference
        self.button_status = [self.S_status.get(), self.A_status.get(), self.B_status.get(), self.C_status.get(), self.D_status.get(), self.E_status.get(), self.F_status.get()]
        
        apply_button = tk.Button(self, text="Apply", command=lambda: self.save(), font=self.button_font, fg="green", bg=self.controller.bg_color, cursor="hand2")
        apply_button.place(x=865, y=650)

        cancel_button = tk.Button(self, text="Cancel", command=lambda: self.controller.frames["MAIN"].tkraise(), font=self.button_font, fg="red", bg=self.controller.bg_color, cursor="hand2")
        cancel_button.place(x=215, y=650)

    def save(self): # Saves current settings to apply to the tier list
        if self.title_var.get() != "":
            title = self.title_var.get() 
            self.controller.frames["MAIN"].title.configure(text=title)
        count = 0
        for tier in self.tier_title_list:
            if tier.get() != "":
                tier_name = tier.get()
                size = len(tier_name)
                if size < 121: # adjusting font size for longer names
                    if size < 16:
                        font_size = (5 - (size//4)) * 8 # calculate varying font size for less than 16 chars
                    else:
                        font_size = 16
                self.controller.frames["MAIN"].buttons[count][0].configure(text=tier_name,font=(self.controller.tier_font, font_size))
            count += 1
        self.controller.frames["MAIN"].edit_tierlist(self.button_status)
        self.controller.frames["MAIN"].tkraise()

    def tier_flag(self): # Saving the updated checkbutton parameters to a list 
        self.button_status = [self.S_status.get(), self.A_status.get(), self.B_status.get(), self.C_status.get(), self.D_status.get(), self.E_status.get(), self.F_status.get()]     

class ConfigureTitle(tk.Toplevel): # So you can change the title if you click on it in the Tiermaker screen
    def __init__(self, controller):
        # initialise toplevel
        tk.Toplevel.__init__(self)
        self.controller = controller

        # fonts
        self.title_font = (self.controller.controller.tier_font, 28)
        self.button_font = (self.controller.controller.tier_font, 18)
        self.input_font = (self.controller.controller.tier_font, 10)

        # basic setup
        self.title("Configuring Title")
        self.geometry("400x300")
        self.configure(bg=self.controller.controller.bg_color)
        self.resizable(0, 0)
        
        # widgets
        title = tk.Label(self, text="Title:", bg=self.controller.controller.bg_color, fg="white", font=self.title_font)
        title.place(x=160, y=15)

        self.name_entry = tk.Text(self, width=30, height=4, font=self.input_font)
        self.name_entry.insert(1.0, self.controller.title["text"])
        self.name_entry.place(x=90, y=75)

        apply_button = tk.Button(self, text="Apply", font=self.button_font, fg="green", bg=self.controller.controller.bg_color, command=lambda: self.save())
        apply_button.place(x=65, y=200)

        cancel_button = tk.Button(self, text="Cancel", font=self.button_font, fg="red", bg=self.controller.controller.bg_color, command=lambda: self.destroy())
        cancel_button.place(x=250, y=200)

    def save(self):
        new_title = self.name_entry.get(1.0, "end-1c")
        size = len(new_title)
        if size < 48:
            self.controller.title.configure(text=new_title)
            self.destroy()
        else:
            messagebox.showerror(title="Title Configuration Error", message="The given title was too large, limit=48 chars.")


class ConfigureTier(tk.Toplevel): # pretty much replica of ConfigureTitle but for the tier names
    def __init__(self, controller, button):
        # initialise toplevel
        tk.Toplevel.__init__(self)
        self.controller = controller
        self.button = button

        # font
        self.title_font = (self.controller.controller.tier_font, 28)
        self.button_font = (self.controller.controller.tier_font, 18)
        self.input_font = (self.controller.controller.tier_font, 10)

        # basic setup
        self.title("Configuring Tier")
        self.geometry("400x300")
        self.configure(bg=self.controller.controller.bg_color)
        self.resizable(0, 0)
        
        # widgets
        title = tk.Label(self, text="Tier Name:", fg="white", bg=self.controller.controller.bg_color, font=self.title_font)
        title.place(x=105, y=15)

        self.name_entry = tk.Text(self, width=30, height=4, font=self.input_font)
        self.name_entry.insert(1.0, self.button["text"])
        self.name_entry.place(x=90, y=75)

        apply_button = tk.Button(self, text="Apply", font=self.button_font, fg="green", bg=self.controller.controller.bg_color, command=lambda: self.save())
        apply_button.place(x=50, y=200)

        cancel_button = tk.Button(self, text="Cancel", font=self.button_font, fg="red", bg=self.controller.controller.bg_color, command=lambda: self.destroy())
        cancel_button.place(x=250, y=200)

    def save(self):
        tier_name = self.name_entry.get(1.0, "end-1c")
        size = len(tier_name)
        if size < 121: # adjusting font size for longer names
            if size < 16:
                font_size = (5 - (size//4)) * 8 # calculate varying font size for less than 16 chars

            else:
                font_size = 16
            
            self.button.configure(text=tier_name, font=(self.controller.controller.tier_font, font_size))
            self.destroy()


        else:
            messagebox.showerror(title="Tier Configuration Error", message="The given tier name was too large, limit=120 chars.")

# run the program
gui = GUI()
gui.mainloop()