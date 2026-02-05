from kivy import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager

from profile import ProfileScreen
from recognize import RecognizeBox, RecognizeScreen
from saved_db import SavedDatabaseScreen
from editor import EditorScreen
from about import AboutScreen


class MainBox(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        Config.set('input', 'mouse', 'mouse, disable_multitouch')
        # Экраны
        self.screen_manager = ScreenManager()
        self.about_screen = AboutScreen()
        self.about_screen.name = 'about'
        self.saved_db_screen = SavedDatabaseScreen()
        self.saved_db_screen.name = 'saved_db'
        self.editor_screen = EditorScreen()
        self.editor_screen.name = 'editor'
        self.recognize_screen = RecognizeScreen()
        self.recognize_screen.name = 'recognize'
        self.profile_screen = ProfileScreen()
        self.profile_screen.name = 'profile'

        self.screen_manager.add_widget(self.about_screen)
        self.screen_manager.add_widget(self.editor_screen)
        self.screen_manager.add_widget(self.recognize_screen)
        self.screen_manager.add_widget(self.saved_db_screen)
        self.screen_manager.add_widget(self.profile_screen)

        self.add_widget(self.screen_manager)
        # Навигационная панель
        self.navigation_bar = BoxLayout()
        self.about = Button(text="О приложении")
        self.editor = Button(text="Редактор")
        self.recognize = Button(text="Распознование")
        self.saved_db = Button(text="Сохраненные")
        self.profile = Button(text="Профиль")

        self.about.bind(on_press=self.changing_screens_on_about)
        self.editor.bind(on_press=self.changing_screens_on_editor)
        self.recognize.bind(on_press=self.changing_screens_on_recognize)
        self.saved_db.bind(on_press=self.changing_screens_on_saved_db)
        self.profile.bind(on_press=self.changing_screens_on_profile)



        for i in [self.about, self.editor, self.recognize, self.saved_db, self.profile]:
            self.navigation_bar.add_widget(i)
        self.navigation_bar.size = (self.width, self.width / 5)
        self.add_widget(self.navigation_bar)



        # Обновление размеров элементов при изменении размера виджета
        self.bind(size=self.update_size, pos=self.update_size)

    def update_size(self, instance, value):
        self.clear_widgets()
        self.screen_manager.size_hint_y = self.height / (self.width / 5)
        self.add_widget(self.screen_manager)
        self.add_widget(self.navigation_bar)


    def changing_screens_on_about(self, instance):
        self.screen_manager.switch_to(self.about_screen)

    def changing_screens_on_editor(self, instance):
        self.editor_screen = EditorScreen()
        self.screen_manager.switch_to(self.editor_screen)

    def changing_screens_on_recognize(self, instance):
        self.screen_manager.switch_to(self.recognize_screen)

    def changing_screens_on_saved_db(self, instance):
        self.saved_db_screen = SavedDatabaseScreen()
        self.screen_manager.switch_to(self.saved_db_screen)

    def changing_screens_on_profile(self, instance):
        self.screen_manager.switch_to(self.profile_screen)


class MainApp(App):
    def build(self):
        Builder.load_file("about.kv")
        return MainBox()


if __name__ == "__main__":
    app = MainApp()
    app.run()






