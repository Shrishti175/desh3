from kivymd.app import MDApp 
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRaisedButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from kendra_details import KendraDetailsScreen
from sevekari_details import SevekariDetailsScreen
from abhiyaan_details import AbhiyaanDetailsScreen
from Upcoming_Abhiyaan import UpcomingAbhiyaanScreen  # Import new tab

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background = Image(source="background.jpg", size_hint=(1, 1), allow_stretch=True)
        self.add_widget(self.background)

        self.layout = FloatLayout()

        self.kendra_button = MDRaisedButton(
            text="Kendra Details",
            size_hint=(0.3, None), height=40, 
            pos_hint={'center_x': 0.1, 'center_y': 0.7}, 
            on_press=self.open_kendra
        )
        self.layout.add_widget(self.kendra_button)

        self.sevekari_button = MDRaisedButton(
            text="Sevekari Details",
            size_hint=(0.3, None), height=40, 
            pos_hint={'center_x': 0.1, 'center_y': 0.6},
            on_press=self.open_sevekari
        )
        self.layout.add_widget(self.sevekari_button)

        self.abhiyaan_button = MDRaisedButton(
            text="Abhiyaan Details",
            size_hint=(0.3, None), height=40, 
            pos_hint={'center_x': 0.1, 'center_y': 0.5},
            on_press=self.open_abhiyaan
        )
        self.layout.add_widget(self.abhiyaan_button)

        self.upcoming_button = MDRaisedButton(
            text="Upcoming Abhiyaan",  # New button
            size_hint=(0.3, None), height=40,
            pos_hint={'center_x': 0.1, 'center_y': 0.4},
            on_press=self.open_upcoming
        )
        self.layout.add_widget(self.upcoming_button)

        self.add_widget(self.layout)

    def open_kendra(self, instance):
        self.manager.current = "kendra_details"

    def open_sevekari(self, instance):
        self.manager.current = "sevekari_details"

    def open_abhiyaan(self, instance):
        self.manager.current = "abhiyaan_details"

    def open_upcoming(self, instance):  # New function for upcoming abhiyaan
        self.manager.current = "upcoming_abhiyaan"

class MyApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(DashboardScreen(name='dashboard'))
        self.sm.add_widget(KendraDetailsScreen(name='kendra_details'))
        self.sm.add_widget(SevekariDetailsScreen(name='sevekari_details'))
        self.sm.add_widget(AbhiyaanDetailsScreen(name='abhiyaan_details'))
        self.sm.add_widget(UpcomingAbhiyaanScreen(name='upcoming_abhiyaan'))  # Add new tab

        return self.sm

if __name__ == '__main__':
    MyApp().run()

