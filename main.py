
"""
World Clock - shows current time in cities around the globe, with search.
Built with Kivy so it can be packaged into an Android APK via Buildozer.
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Rectangle
from datetime import datetime
import pytz

# ---------- Theme ----------
BG_COLOR = (0.07, 0.08, 0.12, 1)        # near-black navy
CARD_COLOR = (0.12, 0.13, 0.19, 1)      # dark slate card
CARD_COLOR_ALT = (0.10, 0.11, 0.16, 1)  # subtle alternate shade
ACCENT_COLOR = (0.35, 0.75, 0.95, 1)    # cyan accent for time text
TEXT_COLOR = (0.92, 0.93, 0.96, 1)      # near-white
SUBTEXT_COLOR = (0.55, 0.58, 0.66, 1)   # muted gray

# City name -> IANA timezone name
CITIES = [
    ("San Francisco", "America/Los_Angeles"),
    ("Los Angeles", "America/Los_Angeles"),
    ("Seattle", "America/Los_Angeles"),
    ("Vancouver", "America/Vancouver"),
    ("Denver", "America/Denver"),
    ("Phoenix", "America/Phoenix"),
    ("Chicago", "America/Chicago"),
    ("Mexico City", "America/Mexico_City"),
    ("New York", "America/New_York"),
    ("Toronto", "America/Toronto"),
    ("Miami", "America/New_York"),
    ("Bogota", "America/Bogota"),
    ("Lima", "America/Lima"),
    ("Santiago", "America/Santiago"),
    ("Sao Paulo", "America/Sao_Paulo"),
    ("Buenos Aires", "America/Argentina/Buenos_Aires"),
    ("Reykjavik", "Atlantic/Reykjavik"),
    ("London", "Europe/London"),
    ("Dublin", "Europe/Dublin"),
    ("Lisbon", "Europe/Lisbon"),
    ("Madrid", "Europe/Madrid"),
    ("Paris", "Europe/Paris"),
    ("Amsterdam", "Europe/Amsterdam"),
    ("Brussels", "Europe/Brussels"),
    ("Berlin", "Europe/Berlin"),
    ("Zurich", "Europe/Zurich"),
    ("Rome", "Europe/Rome"),
    ("Vienna", "Europe/Vienna"),
    ("Prague", "Europe/Prague"),
    ("Warsaw", "Europe/Warsaw"),
    ("Stockholm", "Europe/Stockholm"),
    ("Oslo", "Europe/Oslo"),
    ("Copenhagen", "Europe/Copenhagen"),
    ("Helsinki", "Europe/Helsinki"),
    ("Athens", "Europe/Athens"),
    ("Istanbul", "Europe/Istanbul"),
    ("Kyiv", "Europe/Kyiv"),
    ("Moscow", "Europe/Moscow"),
    ("Cairo", "Africa/Cairo"),
    ("Lagos", "Africa/Lagos"),
    ("Nairobi", "Africa/Nairobi"),
    ("Johannesburg", "Africa/Johannesburg"),
    ("Casablanca", "Africa/Casablanca"),
    ("Tel Aviv", "Asia/Jerusalem"),
    ("Dubai", "Asia/Dubai"),
    ("Abu Dhabi", "Asia/Dubai"),
    ("Riyadh", "Asia/Riyadh"),
    ("Tehran", "Asia/Tehran"),
    ("Karachi", "Asia/Karachi"),
    ("New Delhi", "Asia/Kolkata"),
    ("Mumbai", "Asia/Kolkata"),
    ("Dhaka", "Asia/Dhaka"),
    ("Kathmandu", "Asia/Kathmandu"),
    ("Bangkok", "Asia/Bangkok"),
    ("Hanoi", "Asia/Bangkok"),
    ("Jakarta", "Asia/Jakarta"),
    ("Singapore", "Asia/Singapore"),
    ("Kuala Lumpur", "Asia/Kuala_Lumpur"),
    ("Manila", "Asia/Manila"),
    ("Hong Kong", "Asia/Hong_Kong"),
    ("Beijing", "Asia/Shanghai"),
    ("Shanghai", "Asia/Shanghai"),
    ("Taipei", "Asia/Taipei"),
    ("Seoul", "Asia/Seoul"),
    ("Tokyo", "Asia/Tokyo"),
    ("Osaka", "Asia/Tokyo"),
    ("Perth", "Australia/Perth"),
    ("Adelaide", "Australia/Adelaide"),
    ("Sydney", "Australia/Sydney"),
    ("Melbourne", "Australia/Melbourne"),
    ("Brisbane", "Australia/Brisbane"),
    ("Auckland", "Pacific/Auckland"),
    ("Fiji", "Pacific/Fiji"),
    ("Honolulu", "Pacific/Honolulu"),

    # --- More North America ---
    ("Boston", "America/New_York"),
    ("Washington DC", "America/New_York"),
    ("Atlanta", "America/New_York"),
    ("Philadelphia", "America/New_York"),
    ("Houston", "America/Chicago"),
    ("Dallas", "America/Chicago"),
    ("Austin", "America/Chicago"),
    ("Minneapolis", "America/Chicago"),
    ("Detroit", "America/Detroit"),
    ("San Diego", "America/Los_Angeles"),
    ("Las Vegas", "America/Los_Angeles"),
    ("Portland", "America/Los_Angeles"),
    ("Montreal", "America/Toronto"),
    ("Calgary", "America/Edmonton"),
    ("Ottawa", "America/Toronto"),
    ("Winnipeg", "America/Winnipeg"),
    ("Guadalajara", "America/Mexico_City"),
    ("Monterrey", "America/Monterrey"),
    ("Havana", "America/Havana"),
    ("San Jose (Costa Rica)", "America/Costa_Rica"),
    ("Panama City", "America/Panama"),

    # --- More South America ---
    ("Caracas", "America/Caracas"),
    ("Quito", "America/Guayaquil"),
    ("Montevideo", "America/Montevideo"),
    ("Asuncion", "America/Asuncion"),
    ("La Paz", "America/La_Paz"),
    ("Medellin", "America/Bogota"),
    ("Rio de Janeiro", "America/Sao_Paulo"),
    ("Brasilia", "America/Sao_Paulo"),
    ("Salvador", "America/Bahia"),

    # --- More Europe ---
    ("Edinburgh", "Europe/London"),
    ("Manchester", "Europe/London"),
    ("Birmingham", "Europe/London"),
    ("Glasgow", "Europe/London"),
    ("Porto", "Europe/Lisbon"),
    ("Barcelona", "Europe/Madrid"),
    ("Seville", "Europe/Madrid"),
    ("Milan", "Europe/Rome"),
    ("Naples", "Europe/Rome"),
    ("Venice", "Europe/Rome"),
    ("Munich", "Europe/Berlin"),
    ("Frankfurt", "Europe/Berlin"),
    ("Hamburg", "Europe/Berlin"),
    ("Cologne", "Europe/Berlin"),
    ("Geneva", "Europe/Zurich"),
    ("Bern", "Europe/Zurich"),
    ("Luxembourg", "Europe/Luxembourg"),
    ("Bratislava", "Europe/Bratislava"),
    ("Budapest", "Europe/Budapest"),
    ("Bucharest", "Europe/Bucharest"),
    ("Sofia", "Europe/Sofia"),
    ("Belgrade", "Europe/Belgrade"),
    ("Zagreb", "Europe/Zagreb"),
    ("Ljubljana", "Europe/Ljubljana"),
    ("Vilnius", "Europe/Vilnius"),
    ("Riga", "Europe/Riga"),
    ("Tallinn", "Europe/Tallinn"),
    ("Minsk", "Europe/Minsk"),
    ("Chisinau", "Europe/Chisinau"),
    ("Sarajevo", "Europe/Sarajevo"),
    ("Skopje", "Europe/Skopje"),
    ("Podgorica", "Europe/Podgorica"),
    ("Valletta", "Europe/Malta"),
    ("Nicosia", "Asia/Nicosia"),
    ("Monaco", "Europe/Monaco"),

    # --- More Africa ---
    ("Tunis", "Africa/Tunis"),
    ("Algiers", "Africa/Algiers"),
    ("Tripoli", "Africa/Tripoli"),
    ("Khartoum", "Africa/Khartoum"),
    ("Addis Ababa", "Africa/Addis_Ababa"),
    ("Accra", "Africa/Accra"),
    ("Abidjan", "Africa/Abidjan"),
    ("Dakar", "Africa/Dakar"),
    ("Kinshasa", "Africa/Kinshasa"),
    ("Luanda", "Africa/Luanda"),
    ("Harare", "Africa/Harare"),
    ("Lusaka", "Africa/Lusaka"),
    ("Maputo", "Africa/Maputo"),
    ("Dar es Salaam", "Africa/Dar_es_Salaam"),
    ("Kampala", "Africa/Kampala"),
    ("Kigali", "Africa/Kigali"),
    ("Windhoek", "Africa/Windhoek"),
    ("Gaborone", "Africa/Gaborone"),
    ("Antananarivo", "Indian/Antananarivo"),

    # --- Middle East ---
    ("Baghdad", "Asia/Baghdad"),
    ("Amman", "Asia/Amman"),
    ("Beirut", "Asia/Beirut"),
    ("Damascus", "Asia/Damascus"),
    ("Doha", "Asia/Qatar"),
    ("Kuwait City", "Asia/Kuwait"),
    ("Manama", "Asia/Bahrain"),
    ("Muscat", "Asia/Muscat"),
    ("Sanaa", "Asia/Aden"),

    # --- More Asia ---
    ("Islamabad", "Asia/Karachi"),
    ("Lahore", "Asia/Karachi"),
    ("Colombo", "Asia/Colombo"),
    ("Male", "Indian/Maldives"),
    ("Yangon", "Asia/Yangon"),
    ("Phnom Penh", "Asia/Phnom_Penh"),
    ("Vientiane", "Asia/Vientiane"),
    ("Ulaanbaatar", "Asia/Ulaanbaatar"),
    ("Almaty", "Asia/Almaty"),
    ("Tashkent", "Asia/Tashkent"),
    ("Baku", "Asia/Baku"),
    ("Tbilisi", "Asia/Tbilisi"),
    ("Yerevan", "Asia/Yerevan"),

    # --- More Oceania ---
    ("Wellington", "Pacific/Auckland"),
    ("Christchurch", "Pacific/Auckland"),
    ("Port Moresby", "Pacific/Port_Moresby"),
    ("Guam", "Pacific/Guam"),
]


class CityRow(BoxLayout):
    def __init__(self, city_name, tz_name, index=0, **kwargs):
        super().__init__(
            orientation="horizontal",
            size_hint_y=None,
            height=64,
            padding=[16, 0, 16, 0],
            **kwargs,
        )
        self.city_name = city_name
        self.tz = pytz.timezone(tz_name)

        # Rounded card background, alternating shade for readability
        bg = CARD_COLOR if index % 2 == 0 else CARD_COLOR_ALT
        with self.canvas.before:
            Color(*bg)
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[14])
        self.bind(pos=self._update_bg, size=self._update_bg)

        text_col = BoxLayout(orientation="vertical", size_hint_x=0.55)
        self.city_label = Label(
            text=city_name,
            halign="left",
            valign="middle",
            color=TEXT_COLOR,
            font_size="17sp",
            bold=True,
        )
        self.city_label.bind(size=self.city_label.setter("text_size"))

        self.tzname_label = Label(
            text=tz_name.replace("_", " "),
            halign="left",
            valign="middle",
            color=SUBTEXT_COLOR,
            font_size="11sp",
        )
        self.tzname_label.bind(size=self.tzname_label.setter("text_size"))

        text_col.add_widget(self.city_label)
        text_col.add_widget(self.tzname_label)

        self.time_label = Label(
            text="--:--:--",
            halign="right",
            valign="middle",
            size_hint_x=0.45,
            font_size="21sp",
            bold=True,
            color=ACCENT_COLOR,
        )
        self.time_label.bind(size=self.time_label.setter("text_size"))

        self.add_widget(text_col)
        self.add_widget(self.time_label)

    def _update_bg(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def refresh(self):
        now = datetime.now(self.tz)
        self.time_label.text = now.strftime("%H:%M:%S")
        self.tzname_label.text = now.strftime("%a, %d %b")


class WorldClockApp(App):
    def build(self):
        self.title = "World Clock"
        Window.clearcolor = BG_COLOR

        root = BoxLayout(orientation="vertical", padding=[0, 0, 0, 0])
        with root.canvas.before:
            Color(*BG_COLOR)
            self._root_bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_root_bg, size=self._update_root_bg)

        # ---------- Header ----------
        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=90,
            padding=[20, 14, 20, 10],
        )
        title = Label(
            text="World Clock",
            halign="left",
            valign="middle",
            font_size="28sp",
            bold=True,
            color=TEXT_COLOR,
            size_hint_y=None,
            height=40,
        )
        title.bind(size=title.setter("text_size"))
        subtitle = Label(
            text="Live time, everywhere",
            halign="left",
            valign="middle",
            font_size="13sp",
            color=SUBTEXT_COLOR,
            size_hint_y=None,
            height=22,
        )
        subtitle.bind(size=subtitle.setter("text_size"))
        header.add_widget(title)
        header.add_widget(subtitle)
        root.add_widget(header)

        # ---------- Search box ----------
        search_wrap = BoxLayout(
            size_hint_y=None,
            height=56,
            padding=[20, 4, 20, 10],
        )
        self.search_box = TextInput(
            hint_text="Search a city...",
            hint_text_color=SUBTEXT_COLOR,
            multiline=False,
            padding=[16, 12, 16, 12],
            background_normal="",
            background_active="",
            background_color=CARD_COLOR,
            foreground_color=TEXT_COLOR,
            cursor_color=ACCENT_COLOR,
        )
        self.search_box.bind(text=self.on_search_text)
        search_wrap.add_widget(self.search_box)
        root.add_widget(search_wrap)

        # ---------- City list ----------
        self.scroll = ScrollView()
        self.grid = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=8,
            padding=[20, 4, 20, 20],
        )
        self.grid.bind(minimum_height=self.grid.setter("height"))

        self.all_rows = []
        for i, (city_name, tz_name) in enumerate(CITIES):
            row = CityRow(city_name, tz_name, index=i)
            self.all_rows.append(row)

        self.apply_filter("")

        self.scroll.add_widget(self.grid)
        root.add_widget(self.scroll)

        Clock.schedule_interval(self.update_all, 1)
        self.update_all(0)

        return root

    def _update_root_bg(self, instance, *args):
        self._root_bg.pos = instance.pos
        self._root_bg.size = instance.size

    def on_search_text(self, instance, value):
        self.apply_filter(value)

    def apply_filter(self, query):
        query = query.strip().lower()
        self.grid.clear_widgets()
        self.visible_rows = []
        for row in self.all_rows:
            if query in row.city_name.lower():
                self.grid.add_widget(row)
                self.visible_rows.append(row)

    def update_all(self, dt):
        for row in self.visible_rows:
            row.refresh()


if __name__ == "__main__":
    WorldClockApp().run()
