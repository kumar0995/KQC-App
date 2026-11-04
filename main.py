from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from simulator import run_kqc


class KQCApp(App):

    def build(self):
        self.title = "Kumar Quantum Computer"
        self.circuit = []

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

        self.target = Spinner(
            text="Select Target Qubit",
            values=tuple(str(i) for i in range(8)),
            size_hint_y=None,
            height=55
        )
        layout.add_widget(self.target)

        add = Button(
            text="ADD GATE",
            size_hint_y=None,
            height=55
        )
        add.bind(on_press=self.add_gate)
        layout.add_widget(add)

        run = Button(
            text="RUN SIMULATION",
            size_hint_y=None,
            height=60
        )
        run.bind(on_press=self.run_simulation)
        layout.add_widget(run)

        clear = Button(
            text="CLEAR CIRCUIT",
            size_hint_y=None,
            height=50
        )
        clear.bind(on_press=self.clear_circuit)
        layout.add_widget(clear)

        self.result = Label(
            text="Welcome to KQC",
            font_size=14
        )
        layout.add_widget(self.result)

        return layout

    def add_gate(self, instance):
        gate = self.gate.text

        try:
            q = int(self.qubit.text)

            if gate == "CNOT":
                t = int(self.target.text)

                if q == t:
                    self.result.text = "Choose different qubits!"
                    return

                self.circuit.append(["CNOT", q, t])

            elif gate in ("H", "X", "Y", "Z"):
                self.circuit.append([gate, q])

            else:
                self.result.text = "Select a Gate and Qubit!"
                return

            self.status.text = "Gates Added: " + str(len(self.circuit))
            self.result.text = str(self.circuit)

        except ValueError:
            self.result.text = "Please select qubits!"

    def run_simulation(self, instance):
        if not self.circuit:
            self.result.text = "Circuit is empty!"
            return

        state, counts = run_kqc(self.circuit)

        output = "MEASUREMENT RESULTS\n"

        for key, value in sorted(counts.items()):
            output += key + " : " + str(value) + "\n"

        output += "\nTotal Measurements: 1000"

        self.result.text = output

    def clear_circuit(self, instance):
        self.circuit.clear()
        self.status.text = "KQC-14 | Circuit Cleared"
        self.result.text = "Welcome to KQC"


KQCApp().run()