import openai

openai.api_key = ""

person_desc = """
You are a storyteller, telling your chat partner an interactive story.

The story takes place in a mysterious castle. 
The castle consists of only 5 rooms: The main hall, the kitchen, the dining room, the dance hall and the dungeon.
There are no other rooms in the castle.
The main hall is the entrance to the castle and connected to the kitchen, the dining room and the dance hall.
The dungeon can be accessed from a hidden entrance in the dance hall. Do not tell about the dungeon and the hidden entrance until the person has entered the dance hall and searched it.
I repeat, do not reveal that there is a dungeon.
In the dungeon, there is a deadly dragon.
In the kitchen, there is a sharp sword.
In the dining room, there lives a friendly vampire who likes to gives help on how to solve this adventure, however the advice the vampire is giving is absolutely not helpful.
In the kitchen, there lives a friedly misterious wizard, very old and senile.
The person win, if they kill the dragon with the sword.
The person has 10 health points. If they have 0 health points, they die.
"""

reccurrent_system_prompt = f"This is the setting of interest: {person_desc}."

intention_analyis_system_prompt = """
From the above conversation, what does the storyteller think happens to the person?
1. the person stays alive
2. the person dies a quick death
3. the person dies a horrible and painful death
4. the person wins the adventure

Just give the number.
If uncertain, simply state 'None'.
"""

current_prompt = """
"Complete what the storyteller would say in a style and grammar that matches the background, but only a single sentence or a few sentences.
Do not reveal information that is not directly observable by the person.
Offer several options what the person could do (make a list, each item in a new line).
The options should be something like going to another room, inspecting something or using something.
Don't offer options that are not possible in the story.
It is important, that you let the person in the story only do things that have been offered to do by you before."
"""

chat_messages=[]

running = True

def message2string(m):
    name = "Other" if m['role'] == "user" else "Person"
    return f"{name}: {m['content']}"

while running is True:
    user_input = input("you: ")

    chat_messages.append({"role": "user", "content": user_input})
    chat_messages.append({"role": "system", "content": reccurrent_system_prompt})
    

    chat_history = "\n".join([message2string(m) for m in chat_messages if m['role'] != "system"])

    messages = []
    
    messages.append({"role": "system", "content": reccurrent_system_prompt + "\n" + "Also, this chat history is given: \n" + chat_history + "\nPerson: "})
    messages.append({"role": "user", "content": current_prompt})
    

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages,  temperature=0.3)
    response = completion["choices"][0]["message"]["content"]
    print(response)
    chat_messages.append({"role": "assistant", "content": response})

    mood_analysis_chat_history = "\n".join([message2string(m) for m in chat_messages if m['role'] != "system"])

    intention_analysis_prompt = mood_analysis_chat_history + "\n" + intention_analyis_system_prompt

    intention_analysis_messages = [{"role": "user", "content": intention_analysis_prompt}]

    intention_analysis_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=intention_analysis_messages,  temperature=0.)
    intention_analysis_response = intention_analysis_completion["choices"][0]["message"]["content"]

    if "2" in intention_analysis_response:
        print("You died!")
        exit(0)

    if "3" in intention_analysis_response:
        print("You died a horrible and painful death!")
        exit(0)

    if "4" in intention_analysis_response:
        print("You made it!")
        exit(0)
