"""
AI Exam Paper Corrector - Main Application
==========================================
An intelligent system that grades exam papers using AI techniques.

Features:
- OCR text extraction from images
- Multiple question type support (MCQ, Short Answer, Math)
- AI-powered answer matching using search algorithms
- Bayesian confidence scoring
- Detailed feedback generation

Syllabus Coverage:
- Unit I: BFS/DFS/A* for answer matching
- Unit II: CSP for rubric constraints
- Unit III: Bayesian probability for OCR confidence & partial marks
- Unit IV: Q-learning for improving grading
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from image_processing.ocr_engine import OCREngine
from grading_engine.grader import ExamGrader
from ai_algorithms.search.answer_search import AnswerSearcher
from ai_algorithms.bayesian.confidence_scorer import ConfidenceScorer
from gui.results_view import ResultsWindow


class AIExamCorrectorApp:
    """Main application window for AI Exam Corrector"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📝 AI Exam Paper Corrector - Phase 1")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.ocr_engine = OCREngine()
        self.grader = ExamGrader()
        self.searcher = AnswerSearcher()
        self.confidence_scorer = ConfidenceScorer()
        
        # Current image
        self.current_image = None
        self.current_image_path = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="📝 AI Exam Paper Corrector",
            font=('Helvetica', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left panel - Image upload
        left_panel = tk.LabelFrame(
            main_frame, 
            text="Upload Answer Sheet",
            font=('Helvetica', 12, 'bold'),
            bg='#f0f0f0'
        )
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Image display area
        self.image_frame = tk.Frame(left_panel, bg='#e0e0e0', width=400, height=400)
        self.image_frame.pack(padx=10, pady=10, fill='both', expand=True)
        self.image_frame.pack_propagate(False)
        
        self.image_label = tk.Label(
            self.image_frame,
            text="📸 Drop image here\nor click 'Browse' below",
            font=('Helvetica', 14),
            bg='#e0e0e0',
            fg='#666'
        )
        self.image_label.pack(expand=True)
        
        # Buttons
        btn_frame = tk.Frame(left_panel, bg='#f0f0f0')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        browse_btn = tk.Button(
            btn_frame,
            text="📂 Browse Image",
            font=('Helvetica', 11),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=8,
            command=self.browse_image
        )
        browse_btn.pack(side='left', padx=5)
        
        sample_btn = tk.Button(
            btn_frame,
            text="📋 Use Sample",
            font=('Helvetica', 11),
            bg='#9b59b6',
            fg='white',
            padx=20,
            pady=8,
            command=self.use_sample
        )
        sample_btn.pack(side='left', padx=5)
        
        # Right panel - Settings & Actions
        right_panel = tk.Frame(main_frame, bg='#f0f0f0', width=300)
        right_panel.pack(side='right', fill='y', padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Subject selection
        subject_frame = tk.LabelFrame(
            right_panel,
            text="Subject & Settings",
            font=('Helvetica', 11, 'bold'),
            bg='#f0f0f0'
        )
        subject_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(subject_frame, text="Subject:", bg='#f0f0f0').pack(anchor='w', padx=10, pady=(10, 0))
        self.subject_var = tk.StringVar(value="General")
        subjects = ["General", "Mathematics", "Science", "English", "Computer Science", "AI Course"]
        subject_combo = ttk.Combobox(subject_frame, textvariable=self.subject_var, values=subjects, width=25)
        subject_combo.pack(padx=10, pady=5)
        
        tk.Label(subject_frame, text="Question Type:", bg='#f0f0f0').pack(anchor='w', padx=10, pady=(10, 0))
        self.qtype_var = tk.StringVar(value="Mixed")
        qtypes = ["Mixed", "MCQ Only", "Short Answer", "Math Problems", "Essay"]
        qtype_combo = ttk.Combobox(subject_frame, textvariable=self.qtype_var, values=qtypes, width=25)
        qtype_combo.pack(padx=10, pady=5)
        
        # AI Algorithm selection
        algo_frame = tk.LabelFrame(
            right_panel,
            text="AI Algorithm (Unit I-IV)",
            font=('Helvetica', 11, 'bold'),
            bg='#f0f0f0'
        )
        algo_frame.pack(fill='x', pady=10)
        
        self.algo_var = tk.StringVar(value="A* Search")
        algos = [
            ("A* Search (Unit I)", "A* Search"),
            ("BFS Matching (Unit I)", "BFS"),
            ("CSP Rubric (Unit II)", "CSP"),
            ("Bayesian Scoring (Unit III)", "Bayesian"),
            ("Q-Learning (Unit IV)", "QLearning")
        ]
        
        for text, value in algos:
            rb = tk.Radiobutton(
                algo_frame,
                text=text,
                variable=self.algo_var,
                value=value,
                bg='#f0f0f0'
            )
            rb.pack(anchor='w', padx=10)
        
        # Grade button
        grade_btn = tk.Button(
            right_panel,
            text="🔍 ANALYZE & GRADE",
            font=('Helvetica', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=15,
            command=self.grade_paper
        )
        grade_btn.pack(fill='x', pady=20)
        
        # Quick demo button
        demo_btn = tk.Button(
            right_panel,
            text="🎯 Run Demo (No Image)",
            font=('Helvetica', 11),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            command=self.run_demo
        )
        demo_btn.pack(fill='x', pady=5)
        
        # Status
        self.status_label = tk.Label(
            right_panel,
            text="Ready to grade...",
            font=('Helvetica', 10),
            fg='#666',
            bg='#f0f0f0'
        )
        self.status_label.pack(pady=10)
        
        # Info panel
        info_frame = tk.LabelFrame(
            right_panel,
            text="About This Project",
            font=('Helvetica', 10, 'bold'),
            bg='#f0f0f0'
        )
        info_frame.pack(fill='both', expand=True, pady=10)
        
        info_text = """
AI Exam Corrector uses:

📌 Unit I: Search Algorithms
   - A*, BFS, DFS for matching

📌 Unit II: CSP
   - Rubric constraints

📌 Unit III: Bayesian
   - OCR confidence scoring
   - Partial mark probability

📌 Unit IV: Q-Learning
   - Adaptive grading
        """
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            justify='left',
            font=('Helvetica', 9),
            bg='#f0f0f0'
        )
        info_label.pack(padx=10, pady=5)
        
    def browse_image(self):
        """Open file dialog to select image"""
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="Select Answer Sheet Image",
            filetypes=filetypes
        )
        
        if filepath:
            self.load_image(filepath)
            
    def load_image(self, filepath):
        """Load and display image"""
        try:
            self.current_image_path = filepath
            image = Image.open(filepath)
            
            # Resize for display
            display_size = (380, 380)
            image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            self.current_image = ImageTk.PhotoImage(image)
            self.image_label.configure(image=self.current_image, text="")
            
            self.status_label.configure(text=f"Loaded: {os.path.basename(filepath)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
            
    def use_sample(self):
        """Use sample answer data (no image needed)"""
        self.current_image_path = "SAMPLE"
        self.image_label.configure(
            text="📋 Using Sample Data\n\nQ1: What is AI?\nA: Artificial Intelligence\n\nQ2: 2+2 = ?\nA: 4\n\nQ3: Capital of India?\nA: New Delhi",
            image=""
        )
        self.status_label.configure(text="Sample data loaded")
        
    def grade_paper(self):
        """Grade the uploaded paper"""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please upload an image or use sample data first!")
            return
            
        self.status_label.configure(text="Processing...")
        self.root.update()
        
        try:
            # Get selected algorithm
            algorithm = self.algo_var.get()
            subject = self.subject_var.get()
            
            # Process based on input type
            if self.current_image_path == "SAMPLE":
                # Use sample data
                extracted_text = """
Q1: What is Artificial Intelligence?
A: AI is the simulation of human intelligence in machines.

Q2: Calculate: 15 + 27 = ?
A: 42

Q3: What is the capital of France?
A: Paris

Q4: Define BFS algorithm.
A: Breadth First Search explores all neighbors at current depth before moving to next level.

Q5: What is 2x + 3 = 11? Find x.
A: x = 4
                """
            else:
                # Use OCR
                extracted_text = self.ocr_engine.extract_text(self.current_image_path)
            
            # Grade using selected algorithm
            results = self.grader.grade(
                extracted_text,
                algorithm=algorithm,
                subject=subject
            )
            
            # Show results
            self.show_results(results, algorithm)
            
        except Exception as e:
            messagebox.showerror("Error", f"Grading failed: {str(e)}")
            self.status_label.configure(text="Error occurred")
            
    def run_demo(self):
        """Run a quick demo without image"""
        self.use_sample()
        self.grade_paper()
        
    def show_results(self, results, algorithm):
        """Display grading results"""
        ResultsWindow(self.root, results, algorithm)
        self.status_label.configure(text="Grading complete!")


def main():
    root = tk.Tk()
    app = AIExamCorrectorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
