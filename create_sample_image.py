"""
Generate Sample Answer Sheet Image for Testing
===============================================
Creates a simple image with Q&A text that can be used to test OCR
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_sample_answer_sheet():
    """Create a sample answer sheet image"""
    
    # Create white image
    width, height = 800, 1000
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use a font, fall back to default
    try:
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_text = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((200, 30), "AI Course - Answer Sheet", fill='black', font=font_title)
    draw.text((280, 70), "Student: Demo Student", fill='gray', font=font_small)
    draw.text((280, 90), "Roll No: AI2024001", fill='gray', font=font_small)
    
    # Draw line
    draw.line([(50, 120), (750, 120)], fill='black', width=2)
    
    # Questions and Answers
    qa_pairs = [
        ("Q1: What is Artificial Intelligence?", 
         "A: AI is the simulation of human intelligence in machines."),
        
        ("Q2: Calculate: 15 + 27 = ?", 
         "A: 42"),
        
        ("Q3: What is the capital of France?", 
         "A: Paris"),
        
        ("Q4: Define BFS algorithm.", 
         "A: Breadth First Search explores all neighbors at current depth before moving to next level."),
        
        ("Q5: What is 2x + 3 = 11? Find x.", 
         "A: x = 4"),
        
        ("Q6: What is a heuristic function?",
         "A: A heuristic estimates the cost from current state to goal state."),
        
        ("Q7: Define Q-learning.",
         "A: Q-learning is a reinforcement learning algorithm that learns action values."),
        
        ("Q8: What is Bayesian inference?",
         "A: Bayesian inference uses Bayes theorem to update probability based on evidence."),
    ]
    
    y_position = 150
    
    for question, answer in qa_pairs:
        # Question
        draw.text((50, y_position), question, fill='black', font=font_text)
        y_position += 35
        
        # Answer
        draw.text((50, y_position), answer, fill='blue', font=font_text)
        y_position += 50
        
        # Separator line
        draw.line([(50, y_position), (750, y_position)], fill='lightgray', width=1)
        y_position += 20
    
    # Footer
    draw.text((250, height - 50), "- End of Answer Sheet -", fill='gray', font=font_small)
    
    # Save image
    output_path = os.path.join(os.path.dirname(__file__), "sample_answer_sheet.png")
    image.save(output_path)
    print(f"✅ Sample answer sheet created: {output_path}")
    
    return output_path


def create_sample_mcq_sheet():
    """Create a sample MCQ answer sheet"""
    
    width, height = 600, 400
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    draw.text((200, 20), "MCQ Answer Sheet", fill='black', font=font)
    
    mcq = [
        "Q1: B",
        "Q2: A", 
        "Q3: C",
        "Q4: D",
        "Q5: A",
    ]
    
    y = 70
    for q in mcq:
        draw.text((50, y), q, fill='black', font=font)
        y += 40
    
    output_path = os.path.join(os.path.dirname(__file__), "sample_mcq_sheet.png")
    image.save(output_path)
    print(f"✅ Sample MCQ sheet created: {output_path}")
    
    return output_path


if __name__ == "__main__":
    print("Creating sample answer sheets for testing...")
    print()
    
    # Check if PIL is available
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        path1 = create_sample_answer_sheet()
        path2 = create_sample_mcq_sheet()
        
        print()
        print("=" * 50)
        print("Sample images created! You can now:")
        print("1. Run: python main.py")
        print("2. Click 'Browse Image'")
        print(f"3. Select: {path1}")
        print("4. Click 'ANALYZE & GRADE'")
        print("=" * 50)
        
    except ImportError:
        print("❌ PIL/Pillow not installed.")
        print("Run: pip install Pillow")
        print()
        print("Alternatively, just use the 'Use Sample' button in the GUI!")
