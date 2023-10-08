"""
Author: Von Davis
Date: 10/8/2023

User will be prompted for a question and option guidance on how they want the answer to be (funny, witty, concise, etc.)
The agent will then generate an initial response to the question.
The initial response will be passed to the editor, who will provide feedback on how to improve the response to the agent
The agent will then generate a revised response based on the feedback from the editor.
The initial response, editor feedback, and revised response will be saved to a file for comparison

Program is meant to be easily repurposed for other use cases
"""

import openai
import os

DEBUG = False

if DEBUG:
    print("Debug mode enabled.")

MAX_TOKENS = "1000"

with open("keys.txt", "r") as f:
    openai.api_key1 = f.readline().strip()
    openai.api_key2 = f.readline().strip()



def get_response(user_input=None, editor_feedback=None, answer_guidance=""):
    if DEBUG:
        print("Getting response from agent...")

    guidance = ("Also, consider the following guidance on how to answer: " + answer_guidance + "\n\n")

    if editor_feedback is not None:
        prompt = (
            "Review the question posed to the writer, the writer's initial response as well as the feedback from the "
            "editor and revise the initial response accordingly. Do not include the feedback or anything like "
            "\"Revised response:\" in your response.")
        content = editor_feedback
    else:
        prompt = ("Answer the following question as best as you can. Balance concision with the quality of the answer "
                  f"and tacit user needs implied by the question, if they exist. {guidance if answer_guidance else ''}")
        content = user_input

    raw_response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace with the actual ChatGPT-4 engine name once it's available
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    )

    agent_response = raw_response.choices[0]['message']['content']

    if DEBUG:
        print("Agent response: " + agent_response)

    return agent_response


def get_feedback(response, answer_guidance=""):
    guidance = ("Also, consider the following editorial guidance: " + answer_guidance + "\n\n")

    prompt = ("You are a writing editor. Review the question and response, and make suggestions to improve the quality "
              " and clarity of the writing. Your job IS NOT to revise the writing, but instead to provide feedback to "
              f"the writer, who will incorporate your feedback into a revised response. {guidance if answer_guidance else ''}")
    content = str(response)

    raw_response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace with the actual ChatGPT-4 engine name once it's available
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    )

    agent_response = raw_response.choices[0]['message']['content']

    if DEBUG:
        print("Agent response: " + agent_response)

    return agent_response


def find_unique_filename():
    counter = 0

    if os.path.exists("output.txt"):
        counter += 1
        while os.path.exists("output" + str(counter) + ".txt"):
            counter += 1
        return "output" + str(counter) + ".txt"
    else:
        return "output.txt"


def save_to_file(initial_response, editor_feedback, revised_response):

    filename = find_unique_filename()

    with open(filename, 'w') as f:
        f.write("Initial response: \"" + str(initial_response) + "\"" + "\n\n")
        f.write("Editor feedback: \"" + str(editor_feedback) + "\"" + "\n\n")
        f.write("Revised response: \"" + str(revised_response) + "\"")


def main():
    print("Ask agent a question: ")
    user_input = input()
    print("Give specific guidance on how you want the answer to be (funny, witty, concise, etc.): ")
    answer_guidance = input()
    initial_response = get_response(user_input, None, answer_guidance)
    to_be_edited = ("User question: " + user_input + "\n\nThe response you must edit: " + initial_response)
    editor_feedback = get_feedback(to_be_edited, answer_guidance)
    revised_response = get_response(to_be_edited, editor_feedback)
    print("Initial response: \"" + str(initial_response) + "\"" + "\n")
    print("Editor feedback: \"" + str(editor_feedback) + "\"" + "\n")
    print("Revised response: \"" + str(revised_response) + "\"")
    save_to_file(initial_response, editor_feedback, revised_response)


if __name__ == '__main__':
    main()
