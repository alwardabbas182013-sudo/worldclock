"""
World Clock - shows current time in major cities around the globe.
Built with Kivy so it can be packaged into an Android APK via Buildozer.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock
from datetime import datetime
import pytz

# City name -> IANA timezone name
CITIES = [
    ("San Francisco", "America/Los_Angeles"),
    ("New York",       "America/New_York"),
    ("Sao Paulo",      "America/Sao_Paulo"),
    ("London",         "Europe/London"),
    ("Paris",          "Europe/Paris"),
    ("Cairo",          "Africa/Cairo"),
    ("Moscow",         "Europe/Moscow"),
    ("Dubai",          "Asia/Dubai"),
    ("New Delhi",      "Asia/Kolkata"),
    ("Bangkok",        "Asia/Bangkok"),
    ("Beijing",        "Asia/Shanghai"),
    ("Tokyo",          "Asia/Tokyo"),
    ("Sydney",         "Australia/Sydney"),
    ("Auckland",       "Pacific/Auckland"),
]


class CityRow(BoxLayout):
    def __init__(self, city_name, tz_name, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=56, **kwargs)
        self.tz = pytz.timezone(tz_name)

        self.city_label = Label(
            text=city_name,
            halign="left",
            valign="middle",
            size_hint_x=0.5,
        )
        self.city_label.bind(size=self.city_label.setter("text_size"))

        self.time_label = Label(
            text="--:--:--",
            halign="right",
            valign="middle",
            size_hint_x=0.5,
            font_size="20sp",
            bold=True,
        )
        self.time_label.bind(size=self.time_label.setter("text_size"))

        self.add_widget(self.city_label)
        self.add_widget(self.time_label)

    def refresh(self):
        now = datetime.now(self.tz)
        self.time_label.text = now.strftime("%H:%M:%S  (%a, %d %b)")


class WorldClockApp(App):
    def build(self):
        self.title = "World Clock"
        root = BoxLayout(orientation="vertical")

        header = Label(
            text="World Clock",
            size_hint_y=None,
            height=60,
            font_size="26sp",
            bold=True,
        )
        root.add_widget(header)

        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=4, padding=8)
        grid.bind(minimum_height=grid.setter("height"))

        self.rows = []
        for city_name, tz_name in CITIES:
            row = CityRow(city_name, tz_name)
            grid.add_widget(row)
            self.rows.append(row)

        scroll.add_widget(grid)
        root.add_widget(scroll)

        # Update every second
        Clock.schedule_interval(self.update_all, 1)
        self.update_all(0)

        return root

    def update_all(self, dt):
        for row in self.rows:
            row.refresh()


if __name__ == "__main__":
    WorldClockApp().run()
