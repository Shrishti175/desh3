from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import json

class UpcomingAbhiyaanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_file = "upcoming_abhiyaan.json"
        self.load_data()
        self.build_main_layout()

    def build_main_layout(self, *_):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title = MDLabel(text="Upcoming Abhiyaan", halign="center", theme_text_color="Primary", font_style="H4")
        layout.add_widget(title)

        layout.add_widget(MDLabel(text="Abhiyaan Name", halign="center"))
        self.abhiyaan_name = TextInput(font_size=20)
        layout.add_widget(self.abhiyaan_name)

        layout.add_widget(MDLabel(text="Date", halign="center"))
        self.abhiyaan_date = TextInput(font_size=20, hint_text="DD-MM-YYYY")
        layout.add_widget(self.abhiyaan_date)

        layout.add_widget(MDLabel(text="Work to be Done", halign="center"))
        self.work_inputs = []
        self.work_layout = GridLayout(cols=1, size_hint_y=None)
        self.work_layout.bind(minimum_height=self.work_layout.setter('height'))
        self.add_work_input()  # Start with one input field

        work_scroll = ScrollView(size_hint=(1, 0.3))
        work_scroll.add_widget(self.work_layout)
        layout.add_widget(work_scroll)

        add_work_btn = MDRaisedButton(text="Add More Work", on_press=self.add_work_input)
        layout.add_widget(add_work_btn)

        layout.add_widget(MDRaisedButton(text="Add Upcoming Abhiyaan", on_press=self.save_record))
        layout.add_widget(MDRaisedButton(text="Show All Upcoming Abhiyaan", on_press=self.show_all_records))
        layout.add_widget(MDRaisedButton(text="Back", on_press=self.go_back))

        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def add_work_input(self, *_):
        work_input = TextInput(font_size=12, hint_text="Enter work to be done")
        self.work_inputs.append(work_input)
        self.work_layout.add_widget(work_input)

    def save_record(self, *_):
        work_list = [work.text for work in self.work_inputs if work.text.strip()]
        record = {
            "Abhiyaan Name": self.abhiyaan_name.text,
            "Date": self.abhiyaan_date.text,
            "Work to be Done": work_list
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

    def show_all_records(self, *_):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(MDLabel(text="Upcoming Abhiyaan List", halign="center", font_style="H4"))

        if not self.data:
            layout.add_widget(MDLabel(text="No upcoming abhiyaan found!", halign="center"))
        else:
            for record in self.data:
                details = f"Name: {record['Abhiyaan Name']}\nDate: {record['Date']}\nWork to be Done:"
                layout.add_widget(MDLabel(text=details, halign="left", bold=True))

                for work in record.get("Work to be Done", []):
                    layout.add_widget(MDLabel(text=f"  - {work}", halign="left"))

        layout.add_widget(MDRaisedButton(text="Back", on_press=self.build_main_layout))
        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def go_back(self, *_):
        self.manager.current = "dashboard"
