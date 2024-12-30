import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os
import sqlite3
from datetime import datetime, timedelta
import schedule
import time

# File paths
db_file = r"E:\SIH FINAL\codes\post.db"  # Updated to correct file path
output_dir = r"E:\SIH FINAL\datasets\feed piechart"
os.makedirs(output_dir, exist_ok=True)

# Function to fetch data from SQLite database
def fetch_feedback_data():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_file)
        query = "SELECT * FROM Feedback"
        feedback_data = pd.read_sql_query(query, conn)
        conn.close()
        return feedback_data
    except Exception as e:
        print(f"Error fetching data from database: {e}")
        return None

# Function to train a sentiment classification model
def train_sentiment_model(feedback_data):
    try:
        # Ensure the required columns exist
        if 'Feedback_Description' not in feedback_data.columns or 'Sentiment' not in feedback_data.columns:
            print("Error: Feedback or Sentiment column not found in the dataset.")
            return None, None

        # Preprocess data
        feedback_data.dropna(subset=['Feedback_Description', 'Sentiment'], inplace=True)
        X = feedback_data['Feedback_Description']
        y = feedback_data['Sentiment']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Convert text to feature vectors using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)

        # Train a Multinomial Naive Bayes model
        model = MultinomialNB()
        model.fit(X_train_tfidf, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test_tfidf)
        print("Model Evaluation:\n", classification_report(y_test, y_pred))

        return model, vectorizer
    except Exception as e:
        print(f"Error training the sentiment model: {e}")
        return None, None

# Function to analyze sentiments and generate recommendations
def analyze_sentiments_and_recommend(feedback_data, model, vectorizer):
    try:
        # Filter data for the last 7 days
        if 'Date' in feedback_data.columns:
            feedback_data['Date'] = pd.to_datetime(feedback_data['Date'], errors='coerce')
        else:
            print("Error: Date column not found in the dataset.")
            return None, None

        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_feedback = feedback_data[feedback_data['Date'] >= seven_days_ago]

        # Predict sentiments for recent feedback
        if 'Feedback_Description' in recent_feedback.columns:
            X_recent = recent_feedback['Feedback_Description']
            X_recent_tfidf = vectorizer.transform(X_recent)
            recent_feedback.loc[:, 'Predicted_Sentiment'] = model.predict(X_recent_tfidf)
        else:
            print("Error: Feedback column not found in the recent data.")
            return None, None

        # Analyze sentiment distribution
        sentiment_counts = recent_feedback['Predicted_Sentiment'].value_counts()

        # Separate recommendations for negative and neutral feedback
        recommendations = []
        negative_feedback = recent_feedback[recent_feedback['Predicted_Sentiment'] == 'Negative']
        neutral_feedback = recent_feedback[recent_feedback['Predicted_Sentiment'] == 'Neutral']

        # Recommendations for negative feedback
        if not negative_feedback.empty:
            recommendations.append("Action Plan for Negative Feedback:")
            recommendations.append("1. Address issues like poor service or delays.")
            recommendations.append("2. Provide immediate responses to complaints and track resolutions.")

        # Recommendations for neutral feedback
        if not neutral_feedback.empty:
            recommendations.append("Action Plan for Neutral Feedback:")
            recommendations.append("1. Investigate further to understand why feedback is neither positive nor negative.")
            recommendations.append("2. Try to convert neutral feedback into positive by improving specific aspects.")

        # Recommendations for positive feedback
        if sentiment_counts.get('Positive', 0) > 0:
            recommendations.append("Maintain strengths identified in positive feedback, such as courteous staff and timely service.")
            
        return sentiment_counts, recommendations
    except Exception as e:
        print(f"Error analyzing sentiments: {e}")
        return None, None

# Function to send the email
def send_email(sentiment_counts, recommendations, output_file):
    # Email configuration
    sender_email = "kutemanjusha4@gmail.com"
    receiver_email = ["ashishnalawade683@gmail.com"]
    email_password = "ryuu mpuz nkpk xipd"

    # Email content
    subject = "Sentiment Analysis Report for Last 7 Days with Recommendations"
    body = f"""
    Dear Ashish,

    Please find attached the sentiment analysis report based on the feedback dataset for the last 7 days. 
    The analysis reveals the following sentiment distribution:
    - Positive Feedback: {sentiment_counts.get('Positive', 0)}
    - Neutral Feedback: {sentiment_counts.get('Neutral', 0)}
    - Negative Feedback: {sentiment_counts.get('Negative', 0)}

    **Recommendations**:
    {chr(10).join(recommendations)}

    The attached pie chart visualizes this distribution for your reference.

    Best Regards,  
    Manjusha
    """

    # Prepare email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_email)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach pie chart
    try:
        with open(output_file, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(output_file)}')
        msg.attach(part)
    except Exception as e:
        print(f"Error attaching pie chart: {e}")
        return

    # Send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main function to execute the workflow
def main():
    try:
        # Fetch data from the database
        feedback_data = fetch_feedback_data()
        if feedback_data is None:
            return

        # Train the sentiment analysis model
        model, vectorizer = train_sentiment_model(feedback_data)
        if model is None or vectorizer is None:
            return

        # Analyze sentiments and generate recommendations
        sentiment_counts, recommendations = analyze_sentiments_and_recommend(feedback_data, model, vectorizer)
        if sentiment_counts is None or recommendations is None:
            return

        # Generate pie chart
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"sentiment_piechart_{timestamp}.png")
        plt.figure(figsize=(8, 6))
        sentiment_counts.plot.pie(
            autopct='%1.1f%%', 
            colors=['lightgreen', 'gold', 'lightcoral'], 
            startangle=90
        )
        plt.title('Sentiment Distribution (Last 7 Days)')
        plt.ylabel('')
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()

        print(f"Pie chart saved at {output_file}")

        # Send the email with the report
        send_email(sentiment_counts, recommendations, output_file)

    except Exception as e:
        print(f"Error in main workflow: {e}")

# Function to wait for 5 minutes before sending the email
def wait_and_send_email():
    print("Waiting for 5 minutes...")
    time.sleep(300)  # Wait for 5 minutes (300 seconds)
    main()

# Run the wait and send function
wait_and_send_email()
