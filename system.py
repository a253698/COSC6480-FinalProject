import openai
import random

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = ''
    
def get_ai_response(messages):
    """Function to get responses from OpenAI's GPT-3.5 Turbo model using chat-based interaction."""
    try:
        # Making the API call to get chat completions
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages
        )
        # Correctly accessing the response to get the text content of the message
        if completion and completion.choices:
            return completion.choices[0].message.content
        else:
            return "No response generated."
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def main():
    print("This system is built for medical role-play.")
    role = input("Please enter your role (student/professional): ").lower()
    
    if role not in ["student", "professional"]:
        print("Invalid role specified. Exiting the simulator.")
        return
    
    # Generate the initial scenario
    messages = [
        {"role": "system", "content": f"Let's Role play, The LLM will simulate various medical scenarios and allow users to role-play as healthcare professionals, making decisions and taking actions based on presented situations. Suppose the user is a medical student still in the early learning stage of medical knowledge, the model should give more suggestions and instructions on the next steps and more feedback on the user’s action. If the user is a more experienced medical professional, the model should not give any suggestions for the next steps. Generate a detailed emergency medical scenario suitable for a {role}. Include the patient's age, symptoms, and immediate medical needs."}
    ]
    
    scenario_response = get_ai_response(messages)
    if scenario_response:
        print(f"Here is your scenario:\n{scenario_response}\nWhat would you like to do?")
    else:
        print("Failed to generate a scenario. Please try again.")
        return
    
    history = [messages[0], {"role": "system", "content": scenario_response}]
    
    while True:
        user_action = input("Your action: ")
        if user_action.lower() == 'exit':
            print("Exiting the simulator.")
            break
        
        history.append({"role": "user", "content": user_action})

        # Evaluate the user's action with feedback
        messages.append({"role": "system", "content": "Evaluate the user's action and suggest the next steps based on the medical scenario. If the user's action is approate, generate a feedback of user's action, continue with the story, and what will be the pateint next needs. If the user's action is not approate, generate feedback and ask the patient's action again"})
        
        feedback = get_ai_response(history)
        if feedback:
            print("AI Response:", feedback)
            # Update history with system's feedback and continue the scenario
            history.append({"role": "system", "content": feedback})
        else:
            print("Failed to provide feedback. Please try again.")

if __name__ == "__main__":
    main()
# def main():
#     print("This system is built for medical role-play.")
#     role = input("Please enter your role (student/professional): ").lower()
    
#     if role not in ["student", "professional"]:
#         print("Invalid role specified. Exiting the simulator.")
#         return
    
#     # Create an initial system message for generating a scenario
#     messages = [
#         {"role": "system", "content": f"Generate a detailed emergency medical scenario suitable for a {role}. Include the patient's age, symptoms, and immediate medical needs."}
#     ]
    
#     # Get the scenario from the model
#     scenario_response = get_ai_response(messages)
#     if scenario_response and scenario_response != "No response generated.":
#         print(f"Here is your scenario:\n{scenario_response}\nWhat would you like to do?")
#     else:
#         print("Failed to generate a scenario. Please try again.")
#         return
    
#     # Continue the interaction with action evaluation
#     while True:
#         user_action = input("Your action: ")
#         if user_action.lower() == 'exit':
#             print("Exiting the simulator.")
#             break

#         # Add user's action to the conversation history
#         messages.append({"role": "user", "content": user_action})
        
#         # Request the model to evaluate the action
#         messages.append({"role": "system", "content": "Evaluate the user's action and suggest the next steps based on the medical scenario."})
        
#         feedback = get_ai_response(messages)
#         if feedback and feedback != "No response generated.":
#             print("AI Response:", feedback)
#         else:
#             print("Failed to provide feedback. Please try again.")

# if __name__ == "__main__":
#     main()