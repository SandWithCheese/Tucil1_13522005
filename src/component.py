import customtkinter


class TitleFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.title_label = customtkinter.CTkLabel(
            self,
            text=self.title,
            fg_color="gray30",
            corner_radius=6,
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")


class InputFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure((0, 1), weight=1)
        self.values = values
        self.title = title
        self.entries = []
        self.default_values = ["5", "BD 1C 7A 55 E9", "7", "6", "6", "3", "4"]

        self.title = customtkinter.CTkLabel(
            self, text=self.title, fg_color="gray30", corner_radius=6
        )
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        for i, value in enumerate(self.values):
            label = customtkinter.CTkLabel(self, text=value)
            label.grid(row=i + 1, column=0, padx=10, pady=10, sticky="ew")

            entry = customtkinter.CTkEntry(self)
            entry.insert(0, self.default_values[i])
            entry.grid(row=i + 1, column=1, padx=10, pady=10, sticky="ew")
            self.entries.append(entry)

    def get(self):
        if not all(entry.get() for entry in self.entries):
            return {}

        values = [
            "unique_token",
            "token",
            "buffer_size",
            "m_width",
            "m_height",
            "sequences_count",
            "sequences_max_length",
        ]
        return {key: entry.get() for key, entry in zip(values, self.entries)}

    def set(self, values):
        for i, value in enumerate(values):
            self.entries[i].set(value)


class FileUploadFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.data = {}

        self.title = customtkinter.CTkLabel(
            self, text=self.title, fg_color="gray30", corner_radius=6
        )
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.button = customtkinter.CTkButton(self, text="Upload File")
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.button.configure(command=self.open_file)

        self.text = customtkinter.CTkLabel(self, text="No file uploaded")
        self.text.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def open_file(self):
        filetypes = [("text files", "*.txt")]
        f = customtkinter.filedialog.askopenfilename(
            filetypes=filetypes, title="Select file"
        )

        if f:
            with open(f, "r") as file:
                buffer_size = int(file.readline().strip())
                m_width, m_height = map(int, file.readline().strip().split())
                m = [
                    list(map(str, file.readline().strip().split()))
                    for _ in range(m_height)
                ]
                n = int(file.readline().strip())
                sequences = []
                weights = []
                for _ in range(n):
                    sequence = list(file.readline().strip().split())
                    weight = int(file.readline().strip())
                    sequences.append(sequence)
                    weights.append(weight)

                self.data = {
                    "buffer_size": buffer_size,
                    "m_width": m_width,
                    "m_height": m_height,
                    "m": m,
                    "n": n,
                    "sequences": sequences,
                    "weights": weights,
                }
                self.text.configure(text=f)

    def get(self):
        return self.data


class RadioButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="Manual")

        self.title = customtkinter.CTkLabel(
            self, text=self.title, fg_color="gray30", corner_radius=6
        )
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(
                self, text=value, value=value, variable=self.variable
            )
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=10, sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()


class MatrixFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, m_width, m_height, m):
        super().__init__(master)
        self.grid_columnconfigure((0, m_width - 1), weight=1)
        self.title = title
        self.m_width = m_width
        self.m_height = m_height
        self.entries = []

        self.title = customtkinter.CTkLabel(
            self, text=self.title, fg_color="gray30", corner_radius=6
        )
        self.title.grid(
            row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=m_width
        )

        for i in range(self.m_height):
            for j in range(self.m_width):
                entry = customtkinter.CTkEntry(self, width=30)
                entry.insert(0, m[i][j])
                entry.grid(row=i + 1, column=j, padx=5, pady=5, sticky="ew")
                entry.configure(state="disabled")
                self.entries.append(entry)

    def configure_cell(self, row, column):
        self.entries[row * self.m_width + column].configure(fg_color="#2b719e")


class SequenceFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, sequences, weights):
        super().__init__(master)
        self.grid_columnconfigure((0, 3), weight=1)
        self.title = title
        self.sequences = sequences
        self.entries = []

        self.title = customtkinter.CTkLabel(
            self, text=self.title, fg_color="gray30", corner_radius=6
        )
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=4)

        for i, sequence in enumerate(self.sequences):
            label = customtkinter.CTkLabel(self, text=f"Sequence {i + 1}")
            label.grid(row=i + 1, column=0, padx=10, pady=10, sticky="ew")

            entry = customtkinter.CTkEntry(self)
            entry.insert(0, " ".join(sequence))
            entry.grid(row=i + 1, column=1, padx=10, pady=10, sticky="ew")
            entry.configure(state="disabled")

            label1 = customtkinter.CTkLabel(self, text="Weight")
            label1.grid(row=i + 1, column=2, padx=10, pady=10, sticky="ew")

            entry1 = customtkinter.CTkEntry(self)
            entry1.insert(0, weights[i])
            entry1.grid(row=i + 1, column=3, padx=10, pady=10, sticky="ew")
            entry1.configure(state="disabled")

            self.entries.append(entry)


class CoordinateFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, coordinates):
        super().__init__(master)
        self.grid_columnconfigure((0, 1), weight=1)
        self.title = title
        self.coordinates = coordinates
        self.entries = []

        self.title = customtkinter.CTkLabel(
            self, text=self.title, fg_color="gray30", corner_radius=6
        )
        self.title.grid(row=0, column=0, pady=10, sticky="ew", columnspan=2)

        for i, coordinate in enumerate(self.coordinates):
            label = customtkinter.CTkLabel(self, text=f"Coordinate {i + 1}")
            label.grid(row=i + 1, column=0, pady=10, sticky="ew")

            entry = customtkinter.CTkEntry(self)
            entry.insert(0, f"({coordinate[1] + 1}, {coordinate[0] + 1})")
            entry.grid(row=i + 1, column=1, pady=10, sticky="ew")
            entry.configure(state="disabled")

            self.entries.append(entry)


class ResultFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, result):
        super().__init__(master)
        self.grid_columnconfigure((0, 1), weight=1)
        self.title = title
        self.result = result

        self.title = customtkinter.CTkLabel(
            self, text=self.title, fg_color="gray30", corner_radius=6
        )
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=4)

        label1 = customtkinter.CTkLabel(self, text="Max Weight")
        label1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        entry1 = customtkinter.CTkEntry(self)
        entry1.insert(0, self.result["max_weight"])
        entry1.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        entry1.configure(state="disabled")

        label2 = customtkinter.CTkLabel(self, text="Path")
        label2.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        entry2 = customtkinter.CTkEntry(self)
        entry2.insert(0, self.result["shortest_path"])
        entry2.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        entry2.configure(state="disabled")

        label3 = customtkinter.CTkLabel(self, text="Time Taken")
        label3.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        entry3 = customtkinter.CTkEntry(self)
        entry3.insert(0, f"{self.result['time']:.3f} seconds")
        entry3.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        entry3.configure(state="disabled")

        self.coordinate_frame = CoordinateFrame(
            self, "Coordinates", self.result["shortest_coordinate"]
        )
        self.coordinate_frame.grid(
            row=4, column=0, padx=10, pady=10, sticky="nsew", columnspan=2
        )
