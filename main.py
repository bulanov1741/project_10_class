from kivy import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager

from profile import ProfileScreen
from recognize import RecognizeBox, RecognizeScreen
from saved_db import SavedDatabaseScreen
from editor import EditorScreen
from theory import TheoryScreen


class MainBox(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        Config.set('input', 'mouse', 'mouse, disable_multitouch')
        # Экраны
        self.screen_manager = ScreenManager()
        self.theory_screen = TheoryScreen()
        self.theory_screen.name = 'theory'
        self.saved_db_screen = SavedDatabaseScreen()
        self.saved_db_screen.name = 'saved_db'
        self.editor_screen = EditorScreen()
        self.editor_screen.name = 'editor'
        self.recognize_screen = RecognizeScreen()
        self.recognize_screen.name = 'recognize'
        self.profile_screen = ProfileScreen()
        self.profile_screen.name = 'profile'

        self.screen_manager.add_widget(self.theory_screen)
        self.screen_manager.add_widget(self.editor_screen)
        self.screen_manager.add_widget(self.recognize_screen)
        self.screen_manager.add_widget(self.saved_db_screen)
        self.screen_manager.add_widget(self.profile_screen)

        self.add_widget(self.screen_manager)
        # Навигационная панель
        self.navigation_bar = BoxLayout()
        self.theory = Button(text="Теория")
        self.editor = Button(text="Редактор")
        self.recognize = Button(text="Распознование")
        self.saved_db = Button(text="Сохраненные")
        self.profile = Button(text="Профиль")

        self.theory.bind(on_press=self.changing_screens_on_theory)
        self.editor.bind(on_press=self.changing_screens_on_editor)
        self.recognize.bind(on_press=self.changing_screens_on_recognize)
        self.saved_db.bind(on_press=self.changing_screens_on_saved_db)
        self.profile.bind(on_press=self.changing_screens_on_profile)



        for i in [self.theory, self.editor, self.recognize, self.saved_db, self.profile]:
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


    def changing_screens_on_theory(self, instance):
        self.screen_manager.switch_to(self.theory_screen)

    def changing_screens_on_editor(self, instance):
        self.screen_manager.switch_to(self.editor_screen)

    def changing_screens_on_recognize(self, instance):
        self.screen_manager.switch_to(self.recognize_screen)

    def changing_screens_on_saved_db(self, instance):
        self.screen_manager.switch_to(self.saved_db_screen)

    def changing_screens_on_profile(self, instance):
        self.screen_manager.switch_to(self.profile_screen)


class MainApp(App):
    def build(self):
        return MainBox()


if __name__ == "__main__":
    app = MainApp()
    app.run()






