"""
Results View - Display Grading Results
=======================================
GUI window to show detailed grading results
"""

import tkinter as tk
from tkinter import ttk, filedialog
import os


class ResultsWindow:
    """Window to display grading results"""
    
    def __init__(self, parent, results, algorithm):
        self.results = results
        self.algorithm = algorithm
        
        # Create new window
        self.window = tk.Toplevel(parent)
        self.window.title("📊 Grading Results")
        self.window.geometry("800x600")
        self.window.configure(bg='#f0f0f0')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the results UI"""
        # Header
        header_frame = tk.Frame(self.window, bg='#27ae60', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        if self.results.get('success', False):
            grade = self.results['grade']
            percentage = self.results['percentage']
            
            title_text = f"📊 Grade: {grade}  |  Score: {percentage:.1f}%"
            color = self.get_grade_color(grade)
            header_frame.configure(bg=color)
        else:
            title_text = "❌ Grading Failed"
            
        title_label = tk.Label(
            header_frame,
            text=title_text,
            font=('Helvetica', 22, 'bold'),
            fg='white',
            bg=header_frame['bg']
        )
        title_label.pack(pady=20)
        
        # Summary frame
        summary_frame = tk.Frame(self.window, bg='#ecf0f1', height=100)
        summary_frame.pack(fill='x', padx=20, pady=10)
        
        if self.results.get('success', False):
            summary = self.results['summary']
            
            stats_text = f"✅ Correct: {summary['correct']}  |  ⚠️ Partial: {summary['partial']}  |  ❌ Incorrect: {summary['incorrect']}  |  Total: {summary['total']}"
            
            stats_label = tk.Label(
                summary_frame,
                text=stats_text,
                font=('Helvetica', 12),
                bg='#ecf0f1'
            )
            stats_label.pack(pady=5)
            
            marks_text = f"Total Marks: {self.results['total_marks']}/{self.results['total_max_marks']}  |  Algorithm: {self.results['algorithm_used']}"
            marks_label = tk.Label(
                summary_frame,
                text=marks_text,
                font=('Helvetica', 11),
                fg='#666',
                bg='#ecf0f1'
            )
            marks_label.pack(pady=5)
            
        # Results list
        results_frame = tk.Frame(self.window, bg='#f0f0f0')
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create scrollable area
        canvas = tk.Canvas(results_frame, bg='white')
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Add question results
        if self.results.get('success', False):
            for q in self.results['questions']:
                self.add_question_result(scrollable_frame, q)
        else:
            error_label = tk.Label(
                scrollable_frame,
                text=f"Error: {self.results.get('error', 'Unknown error')}",
                font=('Helvetica', 12),
                fg='red',
                bg='white'
            )
            error_label.pack(pady=20)
            
        # Buttons frame
        btn_frame = tk.Frame(self.window, bg='#f0f0f0')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        # Export button
        export_btn = tk.Button(
            btn_frame,
            text="📥 Export Report",
            font=('Helvetica', 11),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=8,
            command=self.export_report
        )
        export_btn.pack(side='left', padx=5)
        
        # Algorithm info button
        info_btn = tk.Button(
            btn_frame,
            text="ℹ️ Algorithm Details",
            font=('Helvetica', 11),
            bg='#9b59b6',
            fg='white',
            padx=20,
            pady=8,
            command=self.show_algorithm_info
        )
        info_btn.pack(side='left', padx=5)
        
        # Close button
        close_btn = tk.Button(
            btn_frame,
            text="Close",
            font=('Helvetica', 11),
            bg='#95a5a6',
            fg='white',
            padx=20,
            pady=8,
            command=self.window.destroy
        )
        close_btn.pack(side='right', padx=5)
        
    def add_question_result(self, parent, question_data):
        """Add a single question result card"""
        # Card frame
        card = tk.Frame(parent, bg='white', bd=1, relief='solid')
        card.pack(fill='x', padx=10, pady=5)
        
        # Status color
        if question_data['status'] == 'correct':
            status_color = '#27ae60'
        elif question_data['status'] == 'partial':
            status_color = '#f39c12'
        else:
            status_color = '#e74c3c'
            
        # Question header
        header = tk.Frame(card, bg=status_color)
        header.pack(fill='x')
        
        q_num = question_data['question_number']
        marks = question_data['marks']
        max_marks = question_data['max_marks']
        icon = question_data['icon']
        
        header_text = f"  {icon} Question {q_num}  |  Marks: {marks}/{max_marks}"
        
        header_label = tk.Label(
            header,
            text=header_text,
            font=('Helvetica', 11, 'bold'),
            fg='white',
            bg=status_color,
            anchor='w'
        )
        header_label.pack(fill='x', padx=10, pady=5)
        
        # Question text
        q_text_frame = tk.Frame(card, bg='#f9f9f9')
        q_text_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            q_text_frame,
            text="Question:",
            font=('Helvetica', 9, 'bold'),
            bg='#f9f9f9',
            anchor='w'
        ).pack(anchor='w')
        
        tk.Label(
            q_text_frame,
            text=question_data['question_text'][:200],
            font=('Helvetica', 10),
            bg='#f9f9f9',
            wraplength=700,
            justify='left',
            anchor='w'
        ).pack(anchor='w')
        
        # Student answer
        tk.Label(
            q_text_frame,
            text="Your Answer:",
            font=('Helvetica', 9, 'bold'),
            bg='#f9f9f9',
            anchor='w'
        ).pack(anchor='w', pady=(10, 0))
        
        tk.Label(
            q_text_frame,
            text=question_data['student_answer'][:300],
            font=('Helvetica', 10),
            bg='#f9f9f9',
            wraplength=700,
            justify='left',
            anchor='w'
        ).pack(anchor='w')
        
        # Feedback
        feedback_frame = tk.Frame(card, bg='#fff3cd' if question_data['status'] != 'correct' else '#d4edda')
        feedback_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            feedback_frame,
            text=f"💡 {question_data['feedback']}",
            font=('Helvetica', 10),
            bg=feedback_frame['bg'],
            wraplength=700,
            justify='left'
        ).pack(padx=10, pady=5, anchor='w')
        
        # Stats
        stats_frame = tk.Frame(card, bg='white')
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        stats_text = f"Similarity: {question_data['similarity']:.1%} | Keywords: {question_data['keyword_score']:.1%} | Confidence: {question_data['confidence']:.1%} | Algorithm: {question_data['algorithm']} | Nodes: {question_data['nodes_explored']}"
        
        tk.Label(
            stats_frame,
            text=stats_text,
            font=('Helvetica', 8),
            fg='#888',
            bg='white'
        ).pack(anchor='w')
        
    def get_grade_color(self, grade):
        """Get color for grade"""
        colors = {
            'A+': '#27ae60',
            'A': '#2ecc71',
            'B+': '#3498db',
            'B': '#9b59b6',
            'C': '#f39c12',
            'D': '#e67e22',
            'F': '#e74c3c'
        }
        return colors.get(grade, '#95a5a6')
        
    def export_report(self):
        """Export grading report to text file"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialname="grading_report.txt"
        )
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("         AI EXAM PAPER CORRECTOR - GRADING REPORT\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"Overall Grade: {self.results['grade']}\n")
                f.write(f"Total Score: {self.results['total_marks']}/{self.results['total_max_marks']}\n")
                f.write(f"Percentage: {self.results['percentage']}%\n")
                f.write(f"Algorithm Used: {self.results['algorithm_used']}\n\n")
                
                summary = self.results['summary']
                f.write(f"Summary: {summary['correct']} correct, {summary['partial']} partial, {summary['incorrect']} incorrect\n")
                f.write("-" * 60 + "\n\n")
                
                for q in self.results['questions']:
                    f.write(f"Q{q['question_number']}: {q['question_text']}\n")
                    f.write(f"Answer: {q['student_answer']}\n")
                    f.write(f"Status: {q['icon']} {q['status'].upper()}\n")
                    f.write(f"Marks: {q['marks']}/{q['max_marks']}\n")
                    f.write(f"Feedback: {q['feedback']}\n")
                    f.write("-" * 40 + "\n\n")
                    
                f.write("\n" + "=" * 60 + "\n")
                f.write("Generated by AI Exam Corrector - Phase 1\n")
                
            tk.messagebox.showinfo("Export Complete", f"Report saved to:\n{filepath}")
            
    def show_algorithm_info(self):
        """Show information about AI algorithms used"""
        info_window = tk.Toplevel(self.window)
        info_window.title("🧠 AI Algorithm Information")
        info_window.geometry("500x400")
        
        info_text = """
╔══════════════════════════════════════════════════════╗
║           AI ALGORITHMS USED IN GRADING              ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  📌 UNIT I: Search Algorithms                        ║
║  ─────────────────────────────────────               ║
║  • A* Search: Finds optimal answer match using       ║
║    f(n) = g(n) + h(n) with keyword heuristic        ║
║  • BFS: Explores all answers at same similarity     ║
║  • DFS: Deep exploration of answer variations       ║
║  • Greedy: Quick matching using keyword overlap     ║
║                                                      ║
║  📌 UNIT II: CSP                                     ║
║  ─────────────────────────────────────               ║
║  • Rubric constraints for valid grading             ║
║  • Constraint propagation for marks                 ║
║                                                      ║
║  📌 UNIT III: Bayesian Inference                     ║
║  ─────────────────────────────────────               ║
║  • P(correct | keyword, similarity, length)          ║
║  • OCR confidence estimation                        ║
║  • Partial marks calculation with probability       ║
║                                                      ║
║  📌 UNIT IV: Q-Learning                              ║
║  ─────────────────────────────────────               ║
║  • Learning optimal grading from feedback           ║
║  • Adaptive confidence thresholds                   ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
        """
        
        text_widget = tk.Text(info_window, font=('Courier', 10), wrap='word')
        text_widget.insert('1.0', info_text)
        text_widget.config(state='disabled')
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)


# For testing
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    # Sample results
    sample_results = {
        'success': True,
        'questions': [
            {
                'question_number': 1,
                'question_text': 'What is AI?',
                'student_answer': 'AI is simulation of human intelligence',
                'status': 'correct',
                'icon': '✅',
                'marks': 5,
                'max_marks': 5,
                'similarity': 0.85,
                'keyword_score': 0.9,
                'confidence': 0.88,
                'algorithm': 'A* Search',
                'nodes_explored': 4,
                'feedback': 'Correct!'
            }
        ],
        'total_marks': 5,
        'total_max_marks': 5,
        'percentage': 100,
        'grade': 'A+',
        'algorithm_used': 'A* Search',
        'subject': 'AI',
        'summary': {'correct': 1, 'partial': 0, 'incorrect': 0, 'total': 1}
    }
    
    ResultsWindow(root, sample_results, "A* Search")
    root.mainloop()
