import customtkinter
import random
from component import *
from brute_solver import brute_solve


class Result(customtkinter.CTkToplevel):
    def __init__(self, master, data):
        super().__init__(master)
        self.title("Cyberpunk 2077 Breach Protocol Solver Result")
        self.attributes("-zoomed", True)
        self.grid_columnconfigure((0, 1), weight=1)

        self.result = None
        self.title_label = customtkinter.CTkLabel(
            self,
            text="Cyberpunk 2077 Breach Protocol Solver Result",
            fg_color="gray30",
            corner_radius=6,
        )
        self.title_label.grid(
            row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2
        )

        self.matrix_frame = MatrixFrame(
            self,
            "Matrix",
            m_width=int(data["m_width"]),
            m_height=int(data["m_height"]),
            m=data["m"],
        )
        self.matrix_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        self.sequence_frame = SequenceFrame(
            self, "Sequences", data["sequences"], data["weights"]
        )
        self.sequence_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        self.button = customtkinter.CTkButton(self, text="Solve")
        self.button.grid(row=2, column=0, padx=10, pady=10, sticky="n", columnspan=2)
        self.button.configure(command=lambda: self.solve(data))

    def solve(self, data):
        self.result = brute_solve(data)

        if self.result is not None:
            shortest_coordinate = self.result["shortest_coordinate"]
            for coordinate in shortest_coordinate:
                self.matrix_frame.configure_cell(coordinate[0], coordinate[1])

            self.result_frame = ResultFrame(self, "Result", self.result)
            self.result_frame.grid(
                row=3,
                column=0,
                padx=10,
                pady=10,
                sticky="nsew",
                columnspan=2,
                rowspan=2,
            )

            self.button1 = customtkinter.CTkButton(self, text="Export Result")
            self.button1.grid(
                row=5, column=0, padx=10, pady=10, sticky="ew", columnspan=2
            )
            self.button1.configure(command=lambda: self.export_result(self.result))
        else:
            self.error_label = customtkinter.CTkLabel(
                self,
                text="Too many paths for buffer size!",
                fg_color="red",
                corner_radius=6,
            )
            self.error_label.grid(
                row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2
            )

    def export_result(self, result):
        filetypes = [("text files", "*.txt")]
        file_path = customtkinter.filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=filetypes
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(f"{result['max_weight']}\n")
                    f.write(f"{result['shortest_path']}\n")
                    for coordinate in result["shortest_coordinate"]:
                        f.write(f"{coordinate[1] + 1},{coordinate[0] + 1}\n")

                    f.write("\n")
                    f.write(f"{result['time']:.3f} seconds\n")
            except Exception as e:
                print(e)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cyberpunk 2077 Breach Protocol Solver")
        self.attributes("-zoomed", True)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure((0, 1), weight=1)

        self.title_frame = TitleFrame(self, "Cyberpunk 2077 Breach Protocol Solver")
        self.title_frame.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2
        )

        self.values = [
            "Number of Unique Tokens",
            "Tokens",
            "Buffer Size",
            "Matrix Width",
            "Matrix Height",
            "Number of Sequences",
            "Sequences Max Length",
        ]
        self.input_frame = InputFrame(self, "Input", values=self.values)
        self.input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.file_upload_frame = FileUploadFrame(self, "File Upload")
        self.file_upload_frame.grid(row=1, column=1, padx=10, pady=10, sticky="new")

        self.radio_button_frame = RadioButtonFrame(
            self, "Select Mode", values=["Manual", "File"]
        )
        self.radio_button_frame.grid(
            row=2, column=0, padx=10, pady=10, sticky="nsew", columnspan=2
        )

        self.button = customtkinter.CTkButton(self, text="Generate")
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.button.configure(command=self.generate)

    def generate(self):
        mode = self.radio_button_frame.get()
        if mode == "Manual":
            values = self.input_frame.get()
            values = self.generate_data(values)
            res = Result(self, values)
        else:
            values = self.file_upload_frame.get()
            res = Result(self, values)

    def generate_data(self, values):
        unique_token = int(values["unique_token"])
        token = values["token"].split()
        buffer_size = int(values["buffer_size"])
        m_width = int(values["m_width"])
        m_height = int(values["m_height"])
        sequences_count = int(values["sequences_count"])
        sequences_max_length = int(values["sequences_max_length"])

        m = self.generate_matrix(m_width, m_height, token)
        sequences = self.generate_sequence(sequences_count, sequences_max_length, token)
        weights = self.generate_weight(sequences_count)

        return {
            "buffer_size": buffer_size,
            "m_width": m_width,
            "m_height": m_height,
            "m": m,
            "n": sequences_count,
            "sequences": sequences,
            "weights": weights,
        }

    def generate_matrix(self, m_width, m_height, token):
        m = []
        for i in range(m_height):
            row = []
            for j in range(m_width):
                row.append(random.choice(token))
            m.append(row)
        return m

    def generate_sequence(self, sequences_count, sequences_max_length, token):
        sequences = []
        for i in range(sequences_count):
            sequence = []
            for j in range(random.randint(1, sequences_max_length)):
                sequence.append(random.choice(token))

            while sequence in sequences:
                sequence = []
                for j in range(random.randint(1, sequences_max_length)):
                    sequence.append(random.choice(token))

            sequences.append(sequence)
        return sequences

    def generate_weight(self, sequences_count):
        weights = []
        for i in range(sequences_count):
            weights.append(random.randint(1, 10) * 5)
        return weights


if __name__ == "__main__":
    app = App()
    app.mainloop()
