import tkinter as tk
from tkinter import messagebox, filedialog
from newspaper import Article
from textblob import TextBlob
import nltk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
import tempfile
import os

# Download sentence tokenizer
nltk.download('punkt')

# Classify sentiment
def classify_sentiment(p):
    if p > 0.1:
        return "Positive"
    elif p < -0.1:
        return "Negative"
    else:
        return "Neutral"

# Main analysis function
def analyze_article():
    global fig  # So we can access it in the save_to_pdf function

    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a valid URL.")
        return

    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        text = article.text
        summary = article.summary
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        sentiment = classify_sentiment(polarity)

        # Display summary and sentiment
        summary_text.delete("1.0", tk.END)
        summary_text.insert(tk.END, summary)
        result_label.config(text=f"Sentiment: {sentiment} (Polarity Score: {polarity:.2f})")

        sentences = blob.sentences
        polarities = [s.sentiment.polarity for s in sentences]

        # Clear old plot
        for widget in plot_frame.winfo_children():
            widget.destroy()

        # Plot
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(polarities, marker='o', markersize=3, linestyle='-', linewidth=1, color='blue')
        ax.axhline(0, color='gray', linestyle='--', linewidth=1)
        ax.set_title("Sentiment Polarity per Sentence", fontsize=14)
        ax.set_xlabel("Sentence Number")
        ax.set_ylabel("Polarity Score")
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process article:\n{e}")

# Save summary and graph to PDF
def save_to_pdf():
    if not summary_text.get("1.0", tk.END).strip():
        messagebox.showwarning("No Data", "Please run the analysis first.")
        return

    try:
        # Define fixed PDF output path
        save_path = r"C:\Users\Mawuenyefia Hunorkpa\Desktop\PYTHON PROJECTS\SENTIMENT_TEXT_ANALYSIS\File\analysis.pdf"

        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Temporary image file for the plot
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img:
            fig.savefig(temp_img.name)
            image_path = temp_img.name

        # Start PDF
        pdf = pdf_canvas.Canvas(save_path, pagesize=letter)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(30, 750, "News Article Sentiment Analysis")

        # Sentiment result
        pdf.setFont("Helvetica", 11)
        pdf.drawString(30, 720, result_label.cget("text"))
        pdf.drawString(30, 700, "Summary:")

        # Add summary text
        text = summary_text.get("1.0", tk.END).strip()
        lines = text.split("\n")
        y = 680
        for line in lines:
            if y < 100:
                pdf.showPage()
                y = 750
                pdf.setFont("Helvetica", 11)
            pdf.drawString(30, y, line[:95])
            y -= 15

        # Add the plot image
        pdf.drawImage(image_path, 100, y - 220, width=400, height=200)
        pdf.save()

        os.remove(image_path)  # Clean up temp image

        messagebox.showinfo("Saved", f"PDF saved to:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save PDF:\n{e}")

# GUI setup
root = tk.Tk()
root.title("News Article Sentiment Analyzer")
root.geometry("1000x750")

tk.Label(root, text="Enter Article URL:").pack(pady=5)
url_entry = tk.Entry(root, width=100)
url_entry.pack(pady=5)

analyze_btn = tk.Button(root, text="Analyze", command=analyze_article)
analyze_btn.pack(pady=10)

save_btn = tk.Button(root, text="Save as PDF", command=save_to_pdf)
save_btn.pack(pady=5)

result_label = tk.Label(root, text="", font=('Arial', 14))
result_label.pack(pady=10)

tk.Label(root, text="Article Summary:").pack()
summary_text = tk.Text(root, height=10, wrap=tk.WORD)
summary_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
