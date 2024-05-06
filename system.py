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
    
def generate_ehr(messages_list):
    """Generate an Electronic Health Record (EHR) based on the provided conversation history."""
    try:
        # Add prompt for summarizing conversation into EHR
        prompt_text = [
            {"role": "system", "content": "Generate Electronic Health Record based on the following conversation history. Extract information and list the patient demographics, detail symptoms, and detail treatments administered by the user. Only respond with the summerized EHR and no recommendation"},
            # {"role": "system", "content": "Generate an Electronic Health Record (EHR) based on the following conversation history:"}
        ]
        
        # Joining messages' content
        prompt_text += [
            {"role": msg["role"], "content": msg["content"]} for msg in messages_list
        ]

        # Prompting the model to generate EHR based on the conversation history
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt_text
        )
        
        # Extracting the response from the choices
        if response and response.choices:
            return response.choices[0].message.content
        else:
            return "Failed to generate EHR summary."
    except Exception as e:
        print(f"An error occurred while generating EHR: {e}")
        return "Failed to generate EHR summary."

def main():
    print("This system is built for medical role-play.")
    role = input("Please enter your role (student/professional): ").lower()
    
    if role not in ["student", "professional"]:
        print("Invalid role specified. Exiting the simulator.")
        return
    
    # Generate the initial scenario
    messages = [
        # {"role": "system", "content": f"Let's Role play, The LLM will simulate various medical scenarios and allow users to role-play as healthcare professionals, making decisions and taking actions based on presented situations. Suppose the user is a medical student still in the early learning stage of medical knowledge, the model should give more suggestions and instructions on the next steps and more feedback on the user’s action. If the user is a more experienced medical professional, the model should not give any suggestions for the next steps. Generate a detailed emergency medical scenario suitable for a {role}. Include the patient's age, symptoms, and immediate medical needs."}

        {"role": "system", "content": f"This system is designed for medical role-play scenarios, The LLM will simulate various medical scenarios and allow users to role-play as healthcare professionals, making decisions and taking actions based on presented situations. Generate a detailed medical scenario. Include the patient's age, symptoms, and immediate medical needs. Adjust the instruction and suggesstion amount based on the professional level of user. The user is {role}. "}

        # {"role": "system", "content": f" Objective: This system is designed for medical role-play scenarios.  Instructions:  The system will prompt you to specify your role as either a student or a professional. Once your role is determined, the system will generate a medical scenario tailored to your role. You'll be asked to respond with an action relevant to the presented scenario. The system will evaluate your action's appropriateness within the scenario and continue the narrative accordingly. If your action aligns with the scenario, the narrative will progress seamlessly. If not, the system will provide feedback and suggest corrective actions."}

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
        
        history.append({"role": "user", "content": user_action + "what is the results of the patient"})

        # Evaluate the user's action with feedback
        # messages.append({"role": "system", "content": "Evaluate the user's action and continue the story based on the medical scenario. If the user's action is appropriate, continue with the story with test result, generate feedback on the user's action, and what will be the patient's next needs. If the user's action is not appropriate, generate feedback and ask the patient's action again"})
        # messages.append({"role": "system", "content": "Simulated the user's action result to maintain the progression of the scenario. Evaluate the user's action and suggest the next steps based on the medical scenario. If the user's action is approate, generate a feedback of user's action, continue with the story, and what will be the pateint next needs. If the user's action is not approate, generate feedback and ask the patient's action again"})
        messages.append({"role": "system", "content": "Continue the scenario by simulated the user's action result. Evaluate the user's action and provide feedback based on its appropriateness within the medical context. If your action aligns with the scenario, feedback will be provided, and the story will continue, outlining the patient's subsequent needs. In case your action is deemed inappropriate, constructive feedback will be given, prompting you to reconsider your approach."})
        
        feedback = get_ai_response(history)
        if feedback:
            print("AI Response:", feedback)
            # Update history with system's feedback and continue the scenario
            history.append({"role": "system", "content": feedback})
        else:
            print("Failed to provide feedback. Please try again.")
            
    ehr_summary = generate_ehr(history)
    
    # Print the generated EHR summary
    print("Generated EHR Summary:", ehr_summary)

if __name__ == "__main__":
    main()