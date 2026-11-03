from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

class KQCApp(App):
    def build(self):
        self.title = "Kumar Quantum Computer"

        layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=12
        )

        title = Label(
            text="KUMAR QUANTUM COMPUTER",
            font_size=22,
            bold=True,
            size_hint_y=None,
            height=60
        )

        layout.add_widget(title)

        self.status = Label(
            text="KQC-14 | 8 Qubit Simulator",
            font_size=18
        )
        layout.add_widget(self.status)

        self.gate = Spinner(
            text="Select Quantum Gate",
            values=("H", "X", "Y", "Z", "CNOT"),
            size_hint_y=None,
            height=55
        )
        layout.add_widget(self.gate)

        self.qubit = Spinner(
            text="Select Qubit",
            values=tuple(str(i) for i in range(8)),
            size_hint_y=None,
            height=55
        )
        layout.add_widget(self.qubit)

        add = Button(text="ADD GATE", size_hint_y=None, height=55)
        add.bind(on_press=self.add_gate)
        layout.add_widget(add)

        run = Button(text="RUN SIMULATION", size_hint_y=None, height=60)
        run.bind(on_press=self.run_simulation)
        layout.add_widget(run)

        self.result = Label(text="Welcome to KQC", font_size=16)
        layout.add_widget(self.result)

        return layout

    def add_gate(self, instance):
        self.status.text = (
            "Gate: " + self.gate.text +
            " | Qubit: " + self.qubit.text
        )

    def run_simulation(self, instance):
        self.result.text = "KQC Simulator connection pending"

KQCApp().run()
