from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager

from profile import ProfileScreen
from recognize import RecognizeBox, RecognizeScreen
from test import TestScreen
from textbook import TextbookScreen
from theory import TheoryScreen


class MainBox(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        # Экраны
        self.screen_manager = ScreenManager()
        self.theory_screen = TheoryScreen()
        self.theory_screen.name = 'theory'
        self.textbook_screen = TextbookScreen()
        self.textbook_screen.name = 'textbook'
        self.recognize_screen = RecognizeScreen()
        self.recognize_screen.name = 'recognize'
        self.test_screen = TestScreen()
        self.test_screen.name = 'test'
        self.profile_screen = ProfileScreen()
        self.profile_screen.name = 'profile'

        self.screen_manager.add_widget(self.theory_screen)
        self.screen_manager.add_widget(self.textbook_screen)
        self.screen_manager.add_widget(self.recognize_screen)
        self.screen_manager.add_widget(self.test_screen)
        self.screen_manager.add_widget(self.profile_screen)

        self.add_widget(self.screen_manager)
        # Навигационная панель
        self.navigation_bar = BoxLayout()
        self.theory = Button(text="Теория")
        self.textbook = Button(text="Учебник")
        self.recognize = Button(text="Распознование")
        self.test = Button(text="Упражнения")
        self.profile = Button(text="Профиль")

        self.theory.bind(on_press=self.changing_screens_on_theory)
        self.textbook.bind(on_press=self.changing_screens_on_textbook)
        self.recognize.bind(on_press=self.changing_screens_on_recognize)
        self.test.bind(on_press=self.changing_screens_on_test)
        self.profile.bind(on_press=self.changing_screens_on_profile)



        for i in [self.theory, self.textbook, self.recognize, self.test, self.profile]:
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

    def changing_screens_on_textbook(self, instance):
        self.screen_manager.switch_to(self.textbook_screen)

    def changing_screens_on_recognize(self, instance):
        self.screen_manager.switch_to(self.recognize_screen)

    def changing_screens_on_test(self, instance):
        self.screen_manager.switch_to(self.test_screen)

    def changing_screens_on_profile(self, instance):
        self.screen_manager.switch_to(self.profile_screen)


class MainApp(App):
    def build(self):
        return MainBox()


if __name__ == "__main__":
    app = MainApp()
    app.run()






