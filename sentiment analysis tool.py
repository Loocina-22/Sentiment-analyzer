import tkinter as tk
from tkinter import messagebox
from afinn import Afinn  # AFINN sentiment lexicon
import re  # For handling phrases

# Initialize AFINN lexicon
afinn = Afinn()

# Custom phrase sentiment lexicon
# Enhancements for modifiers and negations
# Map overall sentiment scores to statements
def get_sentiment_statement(score):
    if score >= 3:
        return "Very Positive"
    elif 1 < score <= 2:
        return "Positive"
    elif 0 < score <= 1:
        return "Slightly Positive"
    elif score == 0:
        return "Neutral"
    elif -1 <= score < 0:
        return "Slightly Negative"
    elif -2 <= score < -1:
        return "Negative"
    elif score <= -3:
        return "Very Negative"

# Enhancements for modifiers and negations
modifiers = {
    "very": 1,
    "extremely": 2,
    "absolutely": 2,
    "totally": 2,
    "slightly": -0.5,
}

negations = {"not", "no", "never", "hardly"}

# Function to calculate sentiment and display colored words
# Function to calculate sentiment and display colored words
def analyze_sentiment():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showerror("Input Error", "Please enter some text.")
        return

    # Tokenize text into words
    tokens = re.findall(r'\w+|[^\w\s]', input_text)
    word_scores = []
    overall_score = 0

    # Process tokens with negation and modifier handling
    i = 0
    while i < len(tokens):
        token = tokens[i].lower()
        score = 0

        if token in negations:
            word_scores.append((tokens[i], 0))  # Negation words themselves are neutral
            if i + 1 < len(tokens):
                next_token = tokens[i + 1].lower()
                next_score = afinn.score(next_token)
                if next_score != 0:
                    score = -next_score  # Reverse sentiment of the next word
                    word_scores.append((tokens[i + 1], score))  # Add next word with modified score
                    i += 1
        elif token in modifiers:
            word_scores.append((tokens[i], 0))  # Modifier words themselves are neutral
            if i + 1 < len(tokens):
                next_token = tokens[i + 1].lower()
                next_score = afinn.score(next_token)
                if next_score != 0:
                    if next_score<0:
                        score = next_score - modifiers[token]  # Boost sentiment of the next word
                    else:
                        score = next_score + modifiers[token]
                    word_scores.append((tokens[i + 1], score))  # Add next word with modified score
                    i += 1
        else:
            score = afinn.score(token)
            word_scores.append((tokens[i], score))  # Normal words with their sentiment score

        overall_score += score
        i += 1

    # Clear previous output
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)

    # Display tokens with color coding
    for token, score in word_scores:
        if score > 0:
            green_value = 255 - min(int(score * 50), 255)
            color = f"#00{hex(green_value)[2:].zfill(2)}00"  # Green
        elif score < 0:
            red_value = 255 - min(int(abs(score) * 50), 255)
            color = f"#{hex(red_value)[2:].zfill(2)}0000"  # Red
        else:
            color = "#FFFFFF"  # White
        result_text.insert(tk.END, f"{token} ", ("colored", token))
        result_text.tag_config(token, foreground=color)

    # Display overall sentiment statement
    sentiment_statement = get_sentiment_statement(overall_score)
    result_label.config(text=f"Overall Sentiment: {sentiment_statement} \n Overall Score: {overall_score}")
    result_text.config(state=tk.DISABLED)

# GUI Setup
app = tk.Tk()
app.title("Enhanced Sentiment Analysis Tool")
app.geometry("700x500")

# Input Field
tk.Label(app, text="Enter Text:", font=("Arial", 12)).pack(pady=5)
text_input = tk.Text(app, height=5, width=80)
text_input.pack(pady=5)

# Analyze Button
analyze_button = tk.Button(app, text="Analyze Sentiment", command=analyze_sentiment)
analyze_button.pack(pady=10)

# Result Display
result_label = tk.Label(app, text="Overall Sentiment: Neutral", font=("Arial", 12))
result_label.pack(pady=5)

result_text = tk.Text(app, height=15, width=80, state=tk.DISABLED, wrap=tk.WORD)
result_text.config(bg="black")
result_text.pack(pady=5)

# Run Application
app.mainloop()
