from kivy.uix.screenmanager import Screen   
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
import json
from kivy.lang import Builder

Builder.load_file("style.kv")

class AbhiyaanDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_file = "abhiyaan_details.json"
        self.load_data()
        self.build_main_layout()

    def build_main_layout(self):
        self.clear_widgets()

        # Root layout with background image
        root_layout = FloatLayout()

        # Background Image
        bg_image = Image(source='45.jpg', allow_stretch=True, keep_ratio=False)
        root_layout.add_widget(bg_image)


        self.data_file = "abhiyaan_details.json"
        self.load_data()
        self.build_main_layout()

    def build_main_layout(self, instance=None):
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        title = MDLabel(
        text="Abhiyaan Details", 
        halign="center", 
        theme_text_color="Primary", 
        font_style="H4",
        size_hint_y=None,
        height=60
    )
        layout.add_widget(title)

        layout.add_widget(MDLabel(text="Abhiyaan Place"))
        self.abhiyaan_place = TextInput(font_size=20, size_hint_y=None, height=40)
        layout.add_widget(self.abhiyaan_place)

        layout.add_widget(MDLabel(text="Work Done (Multiple Inputs)"))
        self.work_done_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.work_done_layout.bind(minimum_height=self.work_done_layout.setter('height'))
        layout.add_widget(self.work_done_layout)
        layout.add_widget(MDRaisedButton(text="Add Work Done", on_press=self.add_work_done, halign="center", md_bg_color=(0.1, 0.5, 0.7, 1),pos_hint={"center_x": 0.5}))

        layout.add_widget(MDLabel(text="Local Sevekari (Multiple Inputs)"))
        self.local_sevekari_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.local_sevekari_layout.bind(minimum_height=self.local_sevekari_layout.setter('height'))
        layout.add_widget(self.local_sevekari_layout)
        layout.add_widget(MDRaisedButton(text="Add Local Sevekari", on_press=self.add_local_sevekari, md_bg_color=(0.1, 0.5, 0.7, 1),pos_hint={"center_x": 0.5}))
        
        layout.add_widget(MDRaisedButton(text="Add Abhiyaan Details", on_press=self.save_record, md_bg_color=(0.0, 0.6, 0.3, 1),pos_hint={"center_x": 0.5}))

        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
       
        btn_layout.add_widget(MDRaisedButton(text="Edit Record", on_press=self.find_record_for_edit, md_bg_color=(0.3, 0.3, 0.9, 1)))
        btn_layout.add_widget(MDRaisedButton(text="Show All Records", on_press=self.show_all_records, md_bg_color=(0.3, 0.3, 0.9, 1)))
        btn_layout.add_widget(MDRaisedButton(text="Back", on_press=self.go_back, md_bg_color=(0.3, 0.3, 0.9, 1)))
        layout.add_widget(btn_layout)

        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def add_work_done(self, instance):
        new_input = TextInput(font_size=20, size_hint_y=None, height=40)
        self.work_done_layout.add_widget(new_input)

    def add_local_sevekari(self, instance):
        new_input = TextInput(font_size=20, size_hint_y=None, height=40)
        self.local_sevekari_layout.add_widget(new_input)

    def save_record(self, instance):
        record = {
            "Abhiyaan Place": self.abhiyaan_place.text,
            "Work Done": [child.text for child in self.work_done_layout.children if isinstance(child, TextInput)],
            "Local Sevekari": [child.text for child in self.local_sevekari_layout.children if isinstance(child, TextInput)]
        }
        self.data.append(record)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)
        self.build_main_layout()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def find_record_for_edit(self, instance):
        self.find_record(instance, edit_mode=True)

    def find_record(self, instance, edit_mode=False):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(MDLabel(text="Enter Abhiyaan Place to Find:", halign="center"))
        self.find_input = TextInput()
        layout.add_widget(self.find_input)
        layout.add_widget(MDRaisedButton(text="Search", on_press=lambda x: self.display_find_result(edit_mode)))
        layout.add_widget(MDRaisedButton(text="Back", on_press=self.build_main_layout))
        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def display_find_result(self, edit_mode):
        place = self.find_input.text.strip().lower()
        for record in self.data:
            if record["Abhiyaan Place"].strip().lower() == place:
                if edit_mode:
                    return self.display_edit_screen(record)
                self.show_record_details(record)
                return
        self.find_record(None)
        self.find_input.hint_text = "No record found!"

    def display_edit_screen(self, record):
        self.clear_widgets()
    
        scroll_view = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))  # Enables scrolling

        self.abhiyaan_place = TextInput(text=record["Abhiyaan Place"], font_size=20, size_hint_y=None, height=50)
        layout.add_widget(self.abhiyaan_place)
        
        layout.add_widget(MDLabel(text="Work Done:", halign="center"))
        self.work_done_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        for work in record["Work Done"]:
            self.work_done_layout.add_widget(TextInput(text=work, font_size=20))
        layout.add_widget(self.work_done_layout)
        self.work_done_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.work_done_layout.bind(minimum_height=self.work_done_layout.setter('height'))
        layout.add_widget(self.work_done_layout)
        layout.add_widget(MDRaisedButton(text="Add Work Done", on_press=self.add_work_done, halign="center", md_bg_color=(0.1, 0.5, 0.7, 1),pos_hint={"center_x": 0.5}))

        layout.add_widget(MDLabel(text="Local Sevekari:", halign="center"))
        self.local_sevekari_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        for sevekari in record["Local Sevekari"]:
            self.local_sevekari_layout.add_widget(TextInput(text=sevekari, font_size=20))
        layout.add_widget(self.local_sevekari_layout)
        self.local_sevekari_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.local_sevekari_layout.bind(minimum_height=self.local_sevekari_layout.setter('height'))
        layout.add_widget(self.local_sevekari_layout)
        layout.add_widget(MDRaisedButton(text="Add Local Sevekari", on_press=self.add_local_sevekari, md_bg_color=(0.1, 0.5, 0.7, 1),pos_hint={"center_x": 0.5}))

        layout.add_widget(MDRaisedButton(text="Save Changes", on_press=lambda x: self.update_record(record)))
        layout.add_widget(MDRaisedButton(text="Back", on_press=self.build_main_layout))
        
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)
        


    def update_record(self, record):
        record["Abhiyaan Place"] = self.abhiyaan_place.text
        record["Work Done"] = [child.text for child in self.work_done_layout.children if isinstance(child, TextInput)]
        record["Local Sevekari"] = [child.text for child in self.local_sevekari_layout.children if isinstance(child, TextInput)]

        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)
        self.build_main_layout()

    def show_all_records(self, instance):
        self.clear_widgets()
    
        scroll_view = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        layout.add_widget(MDLabel(text="All Records", halign="center", font_style="H4", size_hint_y=None, height=50))

        if not self.data:
            layout.add_widget(MDLabel(text="No records found!", halign="center", size_hint_y=None, height=40))

        for record in self.data:
            details = f"Abhiyaan Place: {record['Abhiyaan Place']}\n\nWork Done:\n- " + "\n- ".join(
            record['Work Done']) + "\n\nLocal Sevekari:\n- " + "\n- ".join(record['Local Sevekari'])
            layout.add_widget(MDLabel(text=details, halign="left", size_hint_y=None, height=200))

        layout.add_widget(MDRaisedButton(text="Back", on_press=self.build_main_layout, size_hint_y=None, height=50))

        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)
    def go_back(self, instance):
        self.manager.current = "dashboard"
