from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import json

class SevekariDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_file = "sevekari_details.json"
        self.load_data()
        self.create_ui()

    def create_ui(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title = MDLabel(text="Sevekari Details", halign="center", theme_text_color="Primary", font_style="H4")
        layout.add_widget(title)

        layout.add_widget(MDLabel(text="Sevekari Name", halign="left"))
        self.sevekari_name = TextInput()
        layout.add_widget(self.sevekari_name)

        layout.add_widget(MDLabel(text="Enter City", halign="left"))
        self.city_name = TextInput()
        layout.add_widget(self.city_name)

        layout.add_widget(MDLabel(text="Abhiyaan Done (Multiple Inputs)", halign="left"))
        self.abhiyaan_done_layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.abhiyaan_done_layout)
        layout.add_widget(MDRaisedButton(text="Add Abhiyaan Done", on_press=self.add_abhiyaan_done))

        layout.add_widget(MDRaisedButton(text="Add Sevekari Details", on_press=self.save_record))
        layout.add_widget(MDRaisedButton(text="Find Record", on_press=self.prompt_find_record))
        layout.add_widget(MDRaisedButton(text="Edit Record", on_press=self.prompt_edit_record))
        layout.add_widget(MDRaisedButton(text="Show All Records", on_press=self.show_all_records))
        layout.add_widget(MDRaisedButton(text="Back", on_press=self.go_back))

        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def add_abhiyaan_done(self, instance):
        self.abhiyaan_done_layout.add_widget(TextInput())

    def save_record(self, instance):
        record = {
            "Sevekari Name": self.sevekari_name.text,
            "City": self.city_name.text,
            "Abhiyaan Done": [child.text for child in self.abhiyaan_done_layout.children if isinstance(child, TextInput)]
        }
        self.data.append(record)
        self.save_data()
        self.create_ui()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def prompt_find_record(self, instance):
        self.prompt_for_input("Enter Sevekari Name to Find", self.find_record)

    def prompt_edit_record(self, instance):
        self.prompt_for_input("Enter Sevekari Name to Edit", self.edit_record)

    def prompt_for_input(self, label_text, callback):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(MDLabel(text=label_text, halign="center", font_style="H5"))
        self.search_input = TextInput()
        layout.add_widget(self.search_input)
        layout.add_widget(MDRaisedButton(text="Submit", on_press=lambda x: callback(self.search_input.text.strip())))
        layout.add_widget(MDRaisedButton(text="Back", on_press=self.create_ui))
        self.add_widget(layout)

    def find_record(self, search_name):
        self.display_records([record for record in self.data if record["Sevekari Name"].strip().lower() == search_name.lower()], "Search Results")

    def edit_record(self, search_name):
        found_index = next((i for i, record in enumerate(self.data) if record["Sevekari Name"].lower() == search_name.lower()), None)
        if found_index is not None:
            self.show_edit_screen(found_index)
        else:
            self.display_records([], "No Record Found")

    def show_edit_screen(self, record_index):
        record = self.data[record_index]
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(MDLabel(text="Edit Sevekari Details", halign="center", font_style="H4"))

        self.edit_sevekari_name = TextInput(text=record["Sevekari Name"])
        layout.add_widget(MDLabel(text="Sevekari Name", halign="center"))
        layout.add_widget(self.edit_sevekari_name)

        self.edit_city_name = TextInput(text=record["City"])
        layout.add_widget(MDLabel(text="City", halign="center"))
        layout.add_widget(self.edit_city_name)

        self.edit_abhiyaan_done_layout = BoxLayout(orientation='vertical')
        for abhiyaan in record["Abhiyaan Done"]:
            self.edit_abhiyaan_done_layout.add_widget(TextInput(text=abhiyaan))
        layout.add_widget(MDLabel(text="Abhiyaan Done (Multiple Inputs)", halign="center"))
        layout.add_widget(self.edit_abhiyaan_done_layout)

        layout.add_widget(MDRaisedButton(text="Add More Abhiyaan Done", on_press=self.add_abhiyaan_done))
        layout.add_widget(MDRaisedButton(text="Save Changes", on_press=lambda x: self.save_edit_record(record_index)))
        layout.add_widget(MDRaisedButton(text="Back", on_press=self.create_ui))

        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def save_edit_record(self, record_index):
        self.data[record_index] = {
            "Sevekari Name": self.edit_sevekari_name.text,
            "City": self.edit_city_name.text,
            "Abhiyaan Done": [child.text for child in self.edit_abhiyaan_done_layout.children if isinstance(child, TextInput)]
        }
        self.save_data()
        self.create_ui()

    def show_all_records(self, instance):
        self.display_records(self.data, "All Records")

    def display_records(self, records, title):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(MDLabel(text=title, halign="center", font_style="H4"))
        for record in records:
            record_text = f"Sevekari Name: {record['Sevekari Name']}\nCity: {record['City']}\n\nAbhiyaan Done:\n" + "\n".join(record['Abhiyaan Done'])
            layout.add_widget(MDLabel(text=record_text, halign="left"))
        layout.add_widget(MDRaisedButton(text="Back", on_press=self.create_ui))
        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def go_back(self, instance):
        self.manager.current = "dashboard"
