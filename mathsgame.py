import pygame
from openai import OpenAI

client = OpenAI(api_key="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")
import random
import os

# OpenAI API Setup (Replace with your API Key)

# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Math Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
GREEN = (0, 200, 100)
RED = (200, 0, 0)

# Fonts
font = pygame.font.Font(None, 40)

# Question and Answers Storage
current_question = ""
answers = {}
correct_answer = ""
time_left = 10  # 10 seconds for each question

def generate_question():
    """Fetches a math question and answers from OpenAI API."""
    global current_question, answers, correct_answer, time_left

    while True:  # Loop to ensure valid data
        prompt = (
            "Create a simple math multiple-choice question with exactly 3 answer choices. "
            "Format it as follows:\n"
            "Question: [Write the math question here]\n"
            "Choices:\n"
            "A) [First option]\n"
            "B) [Second option]\n"
            "C) [Third option]\n"
            "Answer: [Write only A, B, or C as the correct answer]"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content
        print(f"Response: {text}")  # Print the response for debugging

        # Parsing AI Response
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        print(f"Parsed lines: {lines}")  # Print the parsed lines for debugging
        if len(lines) < 5:  # Ensure we have at least 1 question, 3 choices, and an answer
            print("Invalid response, regenerating...")
            continue

        try:
            current_question = lines[0].replace("Question: ", "").strip()

            print("current_question", current_question)
            answers = {
                "A": lines[2].split(") ")[1].strip(),
                "B": lines[3].split(") ")[1].strip(),
                "C": lines[4].split(") ")[1].strip()
            }
            
           

            # Ensure exactly 3 answers
            if len(answers) != 3:
                print("Error: AI response did not provide exactly 3 choices, regenerating...")
                continue

            correct_answer = lines[-1].replace("Answer: ", "").strip()

            # Ensure correct_answer is A, B, or C
            if correct_answer not in ["A", "B", "C"]:
                print("Error: Invalid correct answer format, regenerating...")
                continue

            time_left = 10  # Reset timer for new question
            break  # Exit loop once a valid question is generated
        except IndexError:
            print("Error: Parsing response failed, regenerating...")
            continue

# # Generate first question
# generate_question()

def draw_game():
    """Renders the question and answers on the Pygame screen."""
    screen.fill(WHITE)
    

    # Display question
    question_surface = font.render(current_question, True, BLACK)
    screen.blit(question_surface, (50, 50))

    # Skip line after question
    skip_line_height = 50

    # Display answers as buttons
    button_rects = []
    positions = [(100, 150 + skip_line_height), (100, 220 + skip_line_height), (100, 290 + skip_line_height)]
    for i, (key, pos) in enumerate(zip(answers.keys(), positions)):
        color = BLUE if i == 0 else BLACK
        text_surface = font.render(f"{key}) {answers[key]}", True, color)
        button_rect = text_surface.get_rect(topleft=pos)
        button_rects.append(button_rect)
        pygame.draw.rect(screen, GREEN, button_rect.inflate(10, 10))
        screen.blit(text_surface, pos)

    # Display timer
    timer_surface = font.render(f"Time left: {time_left}", True, RED)
    screen.blit(timer_surface, (WIDTH - 200, 50))

    pygame.display.flip()
    return button_rects


def main():
    print("hello main")
    """Main game loop."""
    global correct_answer, time_left
    running = True
    clock = pygame.time.Clock()
    question_count = 0
    max_questions = 5  # Limit to 5 questions

    generate_question()
    while running and question_count < max_questions:
        button_rects = draw_game()
  


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        chosen_letter = list(answers.keys())[i]
                        print(f"Chosen: {chosen_letter}", f"Correct: {correct_answer}")
                        if chosen_letter == correct_answer:
                            print("Correct!")
                        else:
                            print("Wrong!")

                        # Generate next question
                        question_count += 1
                        if question_count < max_questions:
                            generate_question()
                        else:
                            running = False  # Stop the loop after 5 questions
                        break

        # Update timer
        time_left -= clock.tick(30) / 1000  # 30 FPS
        if time_left <= 0:
            print("Time's up!")
            question_count += 1
            if question_count < max_questions:
                generate_question()
            else:
                running = False  # Stop the loop after 5 questions
        
        

        pygame.display.flip()

    print("Game Over! Thanks for playing.")
    pygame.quit()

if __name__ == "__main__":
    main()
