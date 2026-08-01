import threading

import customtkinter as ctk
from tkinter import filedialog, messagebox
import fitz
from dotenv import load_dotenv

from core.analyzer import analyze_resume
from core.suggestions import generate_suggestions
from core.interview import generate_questions
from core.report import generate_pdf_report
from core.coach import get_career_advice, CoachError

load_dotenv()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

PLACEHOLDER_JD = "Paste job description here..."


class JobFitAI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("JobFit AI")
        self.geometry("1000x750")
        self.minsize(900, 650)

        self.resume_text = ""
        self.resume_path = ""
        self.last_result = None

        self._build_header()
        self._build_input_section()
        self._build_tabs()

    # ---------- layout ----------

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))

        ctk.CTkLabel(header, text="JobFit AI", font=("Arial", 30, "bold")).pack(side="left")
        ctk.CTkLabel(
            header, text="Resume & Job Match Analyzer",
            font=("Arial", 14), text_color="gray"
        ).pack(side="left", padx=(15, 0), pady=(10, 0))

    def _build_input_section(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=30, pady=10)

        top_row = ctk.CTkFrame(frame, fg_color="transparent")
        top_row.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkButton(
            top_row, text="Upload Resume PDF", command=self.upload_resume, width=200
        ).pack(side="left")

        self.resume_label = ctk.CTkLabel(top_row, text="No resume selected", text_color="gray")
        self.resume_label.pack(side="left", padx=15)

        self.jd_box = ctk.CTkTextbox(frame, height=100)
        self.jd_box.pack(fill="x", padx=15, pady=10)
        self.jd_box.insert("0.0", PLACEHOLDER_JD)

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=15, pady=(0, 15))

        self.analyze_btn = ctk.CTkButton(
            btn_row, text="Analyze Resume", command=self.analyze, fg_color="#2fa572"
        )
        self.analyze_btn.pack(side="left")

        self.export_btn = ctk.CTkButton(
            btn_row, text="Export PDF Report", command=self.export_pdf, state="disabled"
        )
        self.export_btn.pack(side="left", padx=10)

    def _build_tabs(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        self.dashboard_tab = self.tabs.add("Dashboard")
        self.suggestions_tab = self.tabs.add("Suggestions")
        self.interview_tab = self.tabs.add("Interview Prep")
        self.coach_tab = self.tabs.add("AI Career Coach")

        self._build_dashboard_tab()
        self._build_suggestions_tab()
        self._build_interview_tab()
        self._build_coach_tab()

    def _build_dashboard_tab(self):
        top = ctk.CTkFrame(self.dashboard_tab, fg_color="transparent")
        top.pack(fill="x", pady=20)

        self.score_label = ctk.CTkLabel(top, text="ATS Score: —", font=("Arial", 26, "bold"))
        self.score_label.pack()

        self.progress = ctk.CTkProgressBar(top, width=500)
        self.progress.pack(pady=10)
        self.progress.set(0)

        cols = ctk.CTkFrame(self.dashboard_tab, fg_color="transparent")
        cols.pack(fill="both", expand=True, padx=10, pady=10)
        cols.grid_columnconfigure(0, weight=1)
        cols.grid_columnconfigure(1, weight=1)
        cols.grid_rowconfigure(0, weight=1)

        matched_frame = ctk.CTkFrame(cols)
        matched_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(
            matched_frame, text="Matched Skills", font=("Arial", 16, "bold")
        ).pack(pady=10)
        self.matched_box = ctk.CTkTextbox(matched_frame)
        self.matched_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        missing_frame = ctk.CTkFrame(cols)
        missing_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(
            missing_frame, text="Missing Skills", font=("Arial", 16, "bold")
        ).pack(pady=10)
        self.missing_box = ctk.CTkTextbox(missing_frame)
        self.missing_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _build_suggestions_tab(self):
        ctk.CTkLabel(
            self.suggestions_tab, text="Personalized Resume Suggestions",
            font=("Arial", 18, "bold")
        ).pack(pady=15)
        self.suggestions_box = ctk.CTkTextbox(self.suggestions_tab)
        self.suggestions_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _build_interview_tab(self):
        ctk.CTkLabel(
            self.interview_tab, text="Suggested Interview Questions",
            font=("Arial", 18, "bold")
        ).pack(pady=15)
        self.interview_box = ctk.CTkTextbox(self.interview_tab)
        self.interview_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _build_coach_tab(self):
        header_row = ctk.CTkFrame(self.coach_tab, fg_color="transparent")
        header_row.pack(fill="x", pady=(15, 5))

        ctk.CTkLabel(
            header_row, text="AI Career Coach", font=("Arial", 18, "bold")
        ).pack(side="left", padx=15)

        self.coach_btn = ctk.CTkButton(
            header_row, text="Get Coaching", command=self.ask_coach, state="disabled"
        )
        self.coach_btn.pack(side="right", padx=15)

        self.coach_box = ctk.CTkTextbox(self.coach_tab)
        self.coach_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.coach_box.insert(
            "0.0",
            "Run an analysis first, then click 'Get Coaching' for personalized "
            "advice from the AI career coach.\n\n"
            "Requires GROQ_API_KEY to be set (see .env.example)."
        )

    # ---------- actions ----------

    def upload_resume(self):
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file:
            return

        try:
            doc = fitz.open(file)
            text = "".join(page.get_text() for page in doc)
            doc.close()
        except Exception as e:
            messagebox.showerror("Error", f"Could not read PDF:\n{e}")
            return

        self.resume_text = text
        self.resume_path = file
        display_name = file.replace("\\", "/").split("/")[-1]
        self.resume_label.configure(text=display_name, text_color="white")

    def analyze(self):
        if not self.resume_text:
            messagebox.showwarning("No Resume", "Please upload a resume first.")
            return

        job_description = self.jd_box.get("0.0", "end").strip()
        if not job_description or job_description == PLACEHOLDER_JD:
            messagebox.showwarning("No Job Description", "Please paste a job description first.")
            return

        score, matched, missing = analyze_resume(self.resume_text, job_description)
        suggestions = generate_suggestions(self.resume_text, matched, missing, score)
        questions = generate_questions(matched, missing)

        self.last_result = {
            "score": score,
            "matched": matched,
            "missing": missing,
            "suggestions": suggestions,
            "questions": questions,
        }

        self.score_label.configure(text=f"ATS Score: {score}%")
        self.progress.set(score / 100)

        self.matched_box.delete("0.0", "end")
        self.matched_box.insert("0.0", "\n".join(f"\u2713 {s}" for s in matched) or "No matches found.")

        self.missing_box.delete("0.0", "end")
        self.missing_box.insert("0.0", "\n".join(f"\u2717 {s}" for s in missing) or "No gaps — full coverage!")

        self.suggestions_box.delete("0.0", "end")
        self.suggestions_box.insert("0.0", "\n\n".join(f"\u2022 {s}" for s in suggestions))

        self.interview_box.delete("0.0", "end")
        q_text = "\n\n".join(f"[{qtype.upper()}] {q}" for _, q, qtype in questions)
        self.interview_box.insert("0.0", q_text)

        self.export_btn.configure(state="normal")
        self.coach_btn.configure(state="normal")

        self.coach_box.delete("0.0", "end")
        self.coach_box.insert("0.0", "Click 'Get Coaching' for personalized advice on this analysis.")

        self.tabs.set("Dashboard")

    def export_pdf(self):
        if not self.last_result:
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="JobFit_AI_Report.pdf",
        )
        if not filepath:
            return

        try:
            generate_pdf_report(
                filepath,
                self.last_result["score"],
                self.last_result["matched"],
                self.last_result["missing"],
                self.last_result["suggestions"],
                self.last_result["questions"],
            )
            messagebox.showinfo("Success", f"Report saved to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate PDF:\n{e}")


    def ask_coach(self):
        if not self.last_result:
            return

        self.coach_btn.configure(state="disabled", text="Thinking...")
        self.coach_box.delete("0.0", "end")
        self.coach_box.insert("0.0", "Contacting the AI career coach...")

        job_description = self.jd_box.get("0.0", "end").strip()

        def worker():
            try:
                advice = get_career_advice(
                    self.resume_text,
                    job_description,
                    self.last_result["score"],
                    self.last_result["matched"],
                    self.last_result["missing"],
                )
                self.after(0, self._show_coach_result, advice, None)
            except CoachError as e:
                self.after(0, self._show_coach_result, None, str(e))
            except Exception as e:
                self.after(0, self._show_coach_result, None, f"Unexpected error: {e}")

        threading.Thread(target=worker, daemon=True).start()

    def _show_coach_result(self, advice, error):
        self.coach_btn.configure(state="normal", text="Get Coaching")
        self.coach_box.delete("0.0", "end")
        self.coach_box.insert("0.0", advice if advice else f"Error: {error}")


if __name__ == "__main__":
    app = JobFitAI()
    app.mainloop()
