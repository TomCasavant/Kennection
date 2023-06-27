import requests
from bs4 import BeautifulSoup
import re

# Send a GET request to the webpage
base_url = 'https://www.mentalfloss.com/posts/ken-jennings-kennections-quiz-46'
answers_url = f"{base_url}/2"
kennection_url = f"{base_url}/3"

response = requests.get(answers_url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the paragraph elements containing the quiz questions
question_elements = soup.find_all('p')

# Use regular expressions to extract the questions and answers
question_pattern = re.compile(r'^\d+\.\s+(.*)')  # Matches the numbering pattern followed by the question text
questions = []
answers = []
is_question = True  # Flag to track if a paragraph element is a question or an answer

for element in question_elements:
    if is_question:
        question_text = element.text.strip()
        match = question_pattern.match(question_text)
        if match:
            question = match.group(1)
            questions.append(question)
            is_question = False
    else:
        answer = element.text.strip()
        answers.append(answer)
        is_question = True

# retrieve kennection
response_final = requests.get(kennection_url)
soup_final = BeautifulSoup(response_final.content, 'html.parser')

answer_element = soup_final.find('p').find('strong')
final_answer = answer_element.text.strip()

questions.append("What is the KENNECTION?")
answers.append(final_answer)
total_questions = len(questions)
# Game loop
score = 0
for index, (question, answer) in enumerate(zip(questions, answers), start=1):
    print(f"Question {index}: {question}")

    hint = " ".join("_" * len(word) for word in answer.split())

    while True:
        print("Hint:", hint)
        user_answer = input("Your answer: ")
        if user_answer.lower() == answer.lower():
            print("Correct!")
            score += 1
            break
        elif user_answer == r'\q':
            print("Answer:", answer)
            break
        else:
            print("Incorrect. Try again.")

# Display the final score
print(f"Final Score: {score} out of {total_questions}\n{base_url}")
print("Final Answer:", final_answer)

