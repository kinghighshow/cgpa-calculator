from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.uix.popup import Popup


class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons = [
            ("Grading System", self.show_grading_system),
            ("Calculate GPA", self.calculate_gpa),
            ("Calculate CGPA", self.calculate_cgpa),
            ("Help", self.show_help)
        ]

        button_height = dp(80)
        y_offset = 1

        for text, func in self.buttons:
            button = Button(
                text=text,
                on_press=func,
                size_hint=(0.8, None),
                height=button_height,
                pos_hint={"center_x": 0.5, "y": y_offset - 0.35}
            )
            self.add_widget(button)
            y_offset -= 0.1

    def show_grading_system(self, instance):
        content = BoxLayout(orientation='vertical')
        grading_data = [
            ["Score", "Letter Grade", "Grade Point"],
            ["70 - Above", "A", "5.00"],
            ["60 – 69", "B", "4.00"],
            ["50 – 59", "C", "3.00"],
            ["45 – 49", "D", "2.00"],
            ["40 – 44", "E", "1.00"],
            ["0 – 39", "F", "0.00"]
        ]

        for data in grading_data:
            label = Label(text=f"{data[0]}  |  {data[1]}  |  {data[2]}", size_hint_y=None, height=dp(50))
            content.add_widget(label)

        scrollview = ScrollView(size_hint=(1, None), height=dp(400))
        scrollview.add_widget(content)

        popup = Popup(title="Grading System", content=scrollview, size_hint=(0.7, 0.8))
        close_button = Button(text="Close", size_hint_y=None, height=dp(40))
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(close_button)
        popup.open()

    def go_back(self, instance):
        self.clear_widgets()
        y_offset = 1
        for text, func in self.buttons:
            button = Button(
                text=text,
                on_press=func,
                size_hint=(0.8, None),
                height=dp(60),
                pos_hint={"center_x": 0.5, "y": y_offset - 0.35}
            )
            self.add_widget(button)
            y_offset -= 0.1

    def calculate_gpa(self, instance):
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Enter Course Units and Grades", size_hint_y=None, height=dp(30)))

        scroll_view = ScrollView(size_hint=(1, 0.7))
        self.gpa_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.gpa_layout.bind(minimum_height=self.gpa_layout.setter('height'))
        scroll_view.add_widget(self.gpa_layout)
        layout.add_widget(scroll_view)

        self.gpa_rows = []
        self.add_row_gpa()

        control_buttons = BoxLayout(size_hint_y=None, height=dp(50))
        add_button = Button(text="Add Row", on_press=self.add_row_gpa)
        back_button = Button(text="Back", on_press=self.go_back)
        submit_button = Button(text="Submit", on_press=self.calculate_gpa_result)

        control_buttons.add_widget(add_button)
        control_buttons.add_widget(submit_button)
        control_buttons.add_widget(back_button)

        layout.add_widget(control_buttons)
        self.add_widget(layout)

    def add_row_gpa(self, instance=None):
        row_layout = BoxLayout(size_hint_y=None, height=dp(40))
        units_input = TextInput(hint_text="Course Units", input_filter="int", size_hint_x=0.4)
        grade_input = TextInput(hint_text="Grade (A-F)", size_hint_x=0.4)
        remove_button = Button(text="Remove", size_hint_x=0.2)
        remove_button.bind(on_press=lambda x: self.remove_row_gpa(row_layout))

        row_layout.add_widget(units_input)
        row_layout.add_widget(grade_input)
        row_layout.add_widget(remove_button)
        self.gpa_layout.add_widget(row_layout)
        self.gpa_rows.append((units_input, grade_input))

    def remove_row_gpa(self, row_layout):
        self.gpa_layout.remove_widget(row_layout)
        self.gpa_rows = [row for row in self.gpa_rows if row[0].parent != row_layout]

    def calculate_gpa_result(self, instance):
        grade_points_map = {
            "A": 5.0,
            "B": 4.0,
            "C": 3.0,
            "D": 2.0,
            "E": 1.0,
            "F": 0.0
        }

        total_points = 0
        total_units = 0

        for units_input, grade_input in self.gpa_rows:
            try:
                units = int(units_input.text)
                grade = grade_input.text.upper()
                grade_point = grade_points_map.get(grade, None)
                if grade_point is not None:
                    total_points += units * grade_point
                    total_units += units
            except ValueError:
                continue

        gpa = total_points / total_units if total_units > 0 else 0
        popup = Popup(
            title="GPA Calculation Result",
            content=Label(text=f"Total Points: {total_points}\nTotal Units: {total_units}\nGPA: {gpa:.2f}"),
            size_hint=(0.6, 0.4)
        )
        popup.open()

    def calculate_cgpa(self, instance):
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Enter Semester Points and Units", size_hint_y=None, height=dp(30)))

        scroll_view = ScrollView(size_hint=(1, 0.7))
        self.cgpa_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.cgpa_layout.bind(minimum_height=self.cgpa_layout.setter('height'))
        scroll_view.add_widget(self.cgpa_layout)
        layout.add_widget(scroll_view)

        self.cgpa_rows = []
        self.add_row_cgpa()

        control_buttons = BoxLayout(size_hint_y=None, height=dp(50))
        add_button = Button(text="Add Row", on_press=self.add_row_cgpa)
        back_button = Button(text="Back", on_press=self.go_back)
        submit_button = Button(text="Submit", on_press=self.calculate_cgpa_result)

        control_buttons.add_widget(add_button)
        control_buttons.add_widget(submit_button)
        control_buttons.add_widget(back_button)

        layout.add_widget(control_buttons)
        self.add_widget(layout)

    def add_row_cgpa(self, instance=None):
        row_layout = BoxLayout(size_hint_y=None, height=dp(40))
        points_input = TextInput(hint_text="Total Grade Points", input_filter="float", size_hint_x=0.4)
        units_input = TextInput(hint_text="Total Course Units", input_filter="int", size_hint_x=0.4)
        remove_button = Button(text="Remove", size_hint_x=0.2)
        remove_button.bind(on_press=lambda x: self.remove_row_cgpa(row_layout))

        row_layout.add_widget(points_input)
        row_layout.add_widget(units_input)
        row_layout.add_widget(remove_button)
        self.cgpa_layout.add_widget(row_layout)
        self.cgpa_rows.append((points_input, units_input))

    def remove_row_cgpa(self, row_layout):
        self.cgpa_layout.remove_widget(row_layout)
        self.cgpa_rows = [row for row in self.cgpa_rows if row[0].parent != row_layout]

    def calculate_cgpa_result(self, instance):
        total_points = 0
        total_units = 0

        for points_input, units_input in self.cgpa_rows:
            try:
                points = float(points_input.text)
                units = int(units_input.text)
                total_points += points
                total_units += units
            except ValueError:
                continue

        cgpa = total_points / total_units if total_units > 0 else 0
        popup = Popup(
            title="CGPA Calculation Result",
            content=Label(text=f"Total Points: {total_points}\nTotal Units: {total_units}\nCGPA: {cgpa:.2f}"),
            size_hint=(0.6, 0.4)
        )
        popup.open()

    def show_help(self, instance):
        popup = Popup(
            title="Help",
            content=Label(text="For any assistance, \nplease contact:\nsultanatanda123@gmail.com"),
            size_hint=(0.7, 0.4)
        )
        popup.open()


class CGPAApp(App):
    def build(self):
        return MainScreen()


CGPAApp().run()

