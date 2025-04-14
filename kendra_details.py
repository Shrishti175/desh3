from kivy.uix.screenmanager import Screen 
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import json
from kivy.lang import Builder
Builder.load_file("style.kv")


class KendraDetailsScreen(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.data_file = "kendra_details.json"
        self.load_data()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10) 
        
        title = MDLabel(text="Select Country", halign="center", theme_text_color="Primary", font_style="H4")
        layout.add_widget(title)
        
        self.countries = ['India', 'USA', 'Australia', 'Oman', 'Dubai']
        for country in self.countries:
            btn = MDRaisedButton(text=country, size_hint=(None, None), pos_hint={'center_x': 0.5})
            btn.bind(on_press=self.show_states if country == "India" else self.show_city_details)
            layout.add_widget(btn)
        
        find_button = MDRaisedButton(text="Find Record", on_press=self.find_record)
        layout.add_widget(find_button)
        
        edit_button = MDRaisedButton(text="Edit Record", on_press=self.edit_record)
        layout.add_widget(edit_button)
        
        show_all_button = MDRaisedButton(text="Show All Records", on_press=self.show_all_records)
        layout.add_widget(show_all_button)
        layout.add_widget(MDRaisedButton(text="Back", on_press=self.go_back))
        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)
    
    
    def show_states(self, instance):
        self.clear_widgets()  # Clear the previous UI

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Title Label
        title = MDLabel(
            text="Select State",
            halign="center",
            theme_text_color="Primary",
            font_style="H4"
        )
        layout.add_widget(title)

        # List of states
        states = [
            'Andhra Pradesh', 'Arunachal Pradesh', 
            'Assam', 'Bihar', 'Chhattisgarh', 
            'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 
            'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 
            'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 
            'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 
            'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
        ]

        # Scrollable Grid Layout
        scroll_view = ScrollView()
        grid = GridLayout(cols=3, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Create state selection buttons
        for state in states:
            btn = MDRaisedButton(
                text=state,
                size_hint=(None, None),
                size=(180, 50)
            )
            btn.bind(on_press=self.show_city_details)  # Bind button press event
            grid.add_widget(btn)

        scroll_view.add_widget(grid)
        layout.add_widget(scroll_view)

        # Back Button
        back_button = MDRaisedButton(
            text="Back",
            size_hint=(None, None),
            size=(100, 40),
            on_press=self.build_main_layout
        )
        layout.add_widget(back_button)

        # Add everything to the screen
        self.add_widget(layout)
    
    def show_city_details(self, instance):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(MDLabel(text="Enter City Details", halign="center"))
        self.city_input = TextInput(font_size=20)
        layout.add_widget(self.city_input)
        
        layout.add_widget(MDLabel(text="Enter Vibhag Names"))
        self.vibhag_input = BoxLayout(orientation='vertical')
        layout.add_widget(self.vibhag_input)
        
        layout.add_widget(MDRaisedButton(text="Add Vibhag", on_press=self.add_vibhag_input))
        
        layout.add_widget(MDLabel(text="Enter Local Sevekari"))
        self.local_sevekari_input = BoxLayout(orientation='vertical')
        layout.add_widget(self.local_sevekari_input)
        layout.add_widget(MDRaisedButton(text="Add Sevekari", on_press=self.add_sevekari_input))
        
        layout.add_widget(MDLabel(text="Enter Arti Timings"))
        self.arti_timings_input = BoxLayout(orientation='vertical')
        layout.add_widget(self.arti_timings_input)
        layout.add_widget(MDRaisedButton(text="Add Arti Timing", on_press=self.add_arti_timing_input))
        
        add_button = MDRaisedButton(text="Add Kendra Details", on_press=self.save_record)
        layout.add_widget(add_button)
        
        back_button = MDRaisedButton(text="Back", on_press=self.build_main_layout)
        layout.add_widget(back_button)
        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)
        
    def add_vibhag_input(self, instance):
        self.vibhag_input.add_widget(TextInput(font_size=20))
    
    def add_sevekari_input(self, instance):
        self.local_sevekari_input.add_widget(TextInput(font_size=20))
    
    def add_arti_timing_input(self, instance):
        self.arti_timings_input.add_widget(TextInput(font_size=20))
    
    def save_record(self, instance):
        record = {
            "city": self.city_input.text,
            "vibhag": [child.text for child in self.vibhag_input.children if isinstance(child, TextInput)],
            "sevekari": [child.text for child in self.local_sevekari_input.children if isinstance(child, TextInput)],
            "arti_timings": [child.text for child in self.arti_timings_input.children if isinstance(child, TextInput)]
        }
        self.data.append(record)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []
    
    def build_main_layout(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title = MDLabel(text="Kendra Details", halign="center", font_style="H4")
        layout.add_widget(title)

        find_button = MDRaisedButton(text="Find Record", on_press=self.find_record)
        layout.add_widget(find_button)

        edit_button = MDRaisedButton(text="Edit Record", on_press=self.edit_record)
        layout.add_widget(edit_button)

        show_all_button = MDRaisedButton(text="Show All Records", on_press=self.show_all_records)
        layout.add_widget(show_all_button)

        back_button = MDRaisedButton(text="Back", on_press=self.go_back)
        layout.add_widget(back_button)

        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def find_record(self, instance):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = MDLabel(text="Search Kendra", halign="center", font_style="H5")
        layout.add_widget(title)

        self.find_input = TextInput(hint_text="Enter City Name")
        layout.add_widget(self.find_input)

        search_button = MDRaisedButton(text="Search", on_press=self.display_find_result)
        layout.add_widget(search_button)

        back_button = MDRaisedButton(text="Back", on_press=self.build_main_layout)
        layout.add_widget(back_button)
        
        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def display_find_result(self, instance):
        city = self.find_input.text.strip().lower()
        found_record = next((record for record in self.data if record["city"].strip().lower() == city), None)
        
        if found_record:
            self.show_record_details(found_record)
        else:
            self.find_input.text = ""
            self.find_input.hint_text = "No Record Found!"

    def show_record_details(self, record):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        details = (f"City: {record['city']}\n\n"
                   f"Vibhag: {', '.join(record['vibhag'])}\n\n"
                   f"Sevekari: {', '.join(record['sevekari'])}\n\n"
                   f"Arti Timings: {', '.join(record['arti_timings'])}")
        
        layout.add_widget(MDLabel(text=details, halign="left"))
        layout.add_widget(MDRaisedButton(text="Back", on_press=self.build_main_layout))

        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def edit_record(self, instance):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title = MDLabel(text="Edit Kendra", halign="center", font_style="H5")
        layout.add_widget(title)

        self.edit_input = TextInput(hint_text="Enter City Name")
        layout.add_widget(self.edit_input)

        search_button = MDRaisedButton(text="Edit", on_press=self.display_edit_form)
        layout.add_widget(search_button)

        back_button = MDRaisedButton(text="Back", on_press=self.build_main_layout)
        layout.add_widget(back_button)
        
        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def display_edit_form(self, instance):
        city = self.edit_input.text.strip().lower()
        self.found_record = next((record for record in self.data if record["city"].strip().lower() == city), None)
        
        if not self.found_record:
            self.edit_input.text = ""
            self.edit_input.hint_text = "No Record Found!"
            return

        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.city_input = TextInput(text=self.found_record['city'])
        layout.add_widget(self.city_input)

        self.vibhag_input = TextInput(text=", ".join(self.found_record['vibhag']))
        layout.add_widget(self.vibhag_input)

        self.sevekari_input = TextInput(text=", ".join(self.found_record['sevekari']))
        layout.add_widget(self.sevekari_input)

        self.arti_timings_input = TextInput(text=", ".join(self.found_record['arti_timings']))
        layout.add_widget(self.arti_timings_input)

        save_button = MDRaisedButton(text="Save Changes", on_press=self.save_edited_record)
        layout.add_widget(save_button)

        back_button = MDRaisedButton(text="Back", on_press=self.build_main_layout)
        layout.add_widget(back_button)
        
        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def save_edited_record(self, instance):
        self.found_record['city'] = self.city_input.text.strip()
        self.found_record['vibhag'] = [x.strip() for x in self.vibhag_input.text.split(",")]
        self.found_record['sevekari'] = [x.strip() for x in self.sevekari_input.text.split(",")]
        self.found_record['arti_timings'] = [x.strip() for x in self.arti_timings_input.text.split(",")]

        self.save_data()
        self.build_main_layout()

    def show_all_records(self, instance):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(MDLabel(text="All Records", halign="center", font_style="H4"))
        for record in self.data:
            layout.add_widget(MDLabel(text=f"City: {record['city']}\nVibhag: {', '.join(record['vibhag'])}\nSevekari: {', '.join(record['sevekari'])}\nArti Timings: {', '.join(record['arti_timings'])}", halign="left"))
        back_button = MDRaisedButton(text="Back", on_press=lambda x: self.build_main_layout())
        layout.add_widget(back_button)
        scroll_view = ScrollView()
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def go_back(self, instance):
     if self.manager:
        self.manager.current = "dashboard"
     else:
        print("ScreenManager not set. Cannot navigate back.")


