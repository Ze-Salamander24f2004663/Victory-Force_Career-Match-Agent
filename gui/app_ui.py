import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from logic.evaluate import evaluate_form_input, extract_stream_from_jd
from utils.extract_text import extract_text_from_file
import os

class CareerMatchPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Career Match Predictor")
        self.root.configure(bg="#1e1e2f")
        self.root.geometry("1000x600")

        self.job_path = ""
        self.job_text = ""

        title = tk.Label(root, text="Career Match Predictor", font=("Arial", 24, "bold"), fg="#00ffae", bg="#1e1e2f")
        title.pack(pady=10)

        container = tk.Frame(root, bg="#1e1e2f")
        container.pack(fill="both", expand=True)

        right_frame = tk.Frame(container, bg="#1e1e2f")
        right_frame.pack(side="right", fill="y", padx=20, pady=20)

        job_btn = tk.Button(right_frame, text="Select Job Description", command=self.load_job_file, bg="#3cb371", fg="white", width=25)
        job_btn.pack(pady=10)

        self.job_label = tk.Label(right_frame, text="", fg="white", bg="#1e1e2f")
        self.job_label.pack()

        qualities_btn = tk.Button(right_frame, text="Your Qualities", command=self.open_qualities_window, bg="#4682b4", fg="white", width=25)
        qualities_btn.pack(pady=10)

        self.result_box = ScrolledText(container, height=25, width=80, bg="#2b2b3d", fg="white", font=("Consolas", 11), wrap="word")
        self.result_box.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    def load_job_file(self):
        path = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.docx")])
        if path:
            self.job_path = path
            self.job_text = extract_text_from_file(path)
            self.job_label.config(text=os.path.basename(path))

    def open_qualities_window(self):
        if not self.job_text:
            messagebox.showwarning("Missing File", "Please select a job description first.")
            return

        win = tk.Toplevel(self.root)
        win.title("Enter Your Qualities")
        win.geometry("420x600")
        win.configure(bg="#1e1e2f")

        stream_detected = extract_stream_from_jd(self.job_text)

        tk.Label(win, text="Select Stream:", fg="white", bg="#1e1e2f", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        self.stream_var = tk.StringVar(value=stream_detected)
        for s in ["Arts", "Science", "Commerce"]:
            tk.Radiobutton(win, text=s, variable=self.stream_var, value=s, bg="#1e1e2f", fg="white", selectcolor="black", activebackground="#1e1e2f").pack(anchor="w", padx=40)

        tk.Label(win, text="Enter Skills (comma separated):", fg="white", bg="#1e1e2f", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        self.skills_entry = tk.Text(win, height=4, width=45, bg="#2b2b3d", fg="white")
        self.skills_entry.pack(padx=20)

        tk.Label(win, text="Years of Experience:", fg="white", bg="#1e1e2f", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        self.exp_var = tk.StringVar(value="Fresher")
        for option in ["Fresher", "2–5", "5–10", "10+"]:
            tk.Radiobutton(win, text=option, variable=self.exp_var, value=option, bg="#1e1e2f", fg="white", selectcolor="black", activebackground="#1e1e2f").pack(anchor="w", padx=40)

        self.project_var = tk.StringVar()
        self.intern_var = tk.StringVar()

        self.project_frame = tk.Frame(win, bg="#1e1e2f")
        self.project_frame.pack(anchor="w", padx=20, pady=(10, 0))

        self.project_label = tk.Label(self.project_frame, text="Number of Projects:", fg="white", bg="#1e1e2f")
        self.project_dropdown = tk.OptionMenu(self.project_frame, self.project_var, *[str(i) for i in range(5)])

        self.intern_label = tk.Label(self.project_frame, text="Have you done Internship?", fg="white", bg="#1e1e2f")
        self.intern_var.set("No")
        self.intern_radio_yes = tk.Radiobutton(self.project_frame, text="Yes", variable=self.intern_var, value="Yes", bg="#1e1e2f", fg="white", selectcolor="black")
        self.intern_radio_no = tk.Radiobutton(self.project_frame, text="No", variable=self.intern_var, value="No", bg="#1e1e2f", fg="white", selectcolor="black")

        def update_project_section(*args):
            for widget in self.project_frame.winfo_children():
                widget.pack_forget()
            if self.stream_var.get() in ["Arts", "Science"]:
                self.project_label.pack(anchor="w")
                self.project_var.set("0")
                self.project_dropdown.pack(anchor="w")
            else:
                self.intern_label.pack(anchor="w")
                self.intern_radio_yes.pack(anchor="w")
                self.intern_radio_no.pack(anchor="w")

        self.stream_var.trace_add("write", update_project_section)
        update_project_section()

        tk.Label(win, text="Communication Skills:", fg="white", bg="#1e1e2f", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        self.comm_var = tk.StringVar(value="10")
        for text, val in [
            ("Mother tongue + English", "10"),
            ("Mother tongue + Other", "5"),
            ("Mother + English + Other(s)", "20")
        ]:
            tk.Radiobutton(win, text=text, variable=self.comm_var, value=val, bg="#1e1e2f", fg="white", selectcolor="black").pack(anchor="w", padx=40)

        tk.Button(win, text="Evaluate", command=self.evaluate_qualities, bg="#2e8b57", fg="white", font=("Arial", 10, "bold"), width=20).pack(pady=20)

    def evaluate_qualities(self):
        try:
            skills = [s.strip() for s in self.skills_entry.get("1.0", tk.END).split(",") if s.strip()]
            exp_map = {"Fresher": 0, "2–5": 3, "5–10": 7, "10+": 11}
            years = exp_map.get(self.exp_var.get(), 0)
            if self.stream_var.get() == "Commerce":
                projects = 4 if self.intern_var.get() == "Yes" else 0
            else:
                projects = int(self.project_var.get())
            comm_score = int(self.comm_var.get())

            match_score, fit_rating, suggestions = evaluate_form_input(skills, years, projects, comm_score, self.job_text)

            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, f"🔢 Match Probability: {match_score:.2f}%\n")
            self.result_box.insert(tk.END, f"🎯 Fit Rating: {fit_rating}\n\n")
            self.result_box.insert(tk.END, "📌 Suggestions to Improve:\n")
            for s in suggestions:
                self.result_box.insert(tk.END, f"• {s}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

# Entry point
def run_app():
    root = tk.Tk()
    app = CareerMatchPredictorApp(root)
    root.mainloop()
