import openai
from openai import OpenAI
from playsound import playsound

RESPONSE_AUDIO_PATH = './bot_response.mp3'

# create your own file and add your own openai api
from api_key import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

client = OpenAI(
    api_key = OPENAI_API_KEY
)

# system prompt
system_prompt = "You are a student stress relief assistant. Your goal is to use your own words and stories to keep chatting with the user and help them feel better. You have to remember these chatting paradigms and generate your words:\n1. Active Listening: Encourage individuals to express their emotions without judgment, and offer validation by reflecting back on what they are saying to show empathy.\n2. The experience and effects of emotional support: Use empathetic communication, gentle reassurance, and emotional validation when offering support to someone stressed.\n3. Peer support: Make yourself a supportive peer, emphasizing shared experiences to create emotional bonds that help reduce stress."

# initialize history
conversation_history = [
    {"role": "system", "content": system_prompt}
]

def chatbot(prompt):
    ## txt --> txt
    conversation_history.append({'role': 'user', 'content': prompt})
    
    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        temperature = 1,
        messages = conversation_history
    )
    
    reply = completion.choices[0].message.content
    
    conversation_history.append({'role': 'assistant', 'content': reply})
    
    return reply

def text_chatroom():
    ## txt --> txt
    print("Hi there, welcome to the CozyRoom, chat with me about any thing you are worrying about. Type 'exit' to end the conversation")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("See you. Have a nice day, bye~")
            break
        
        reply = chatbot(user_input)
        print(f"CozyRoom: {reply}")


def text_to_audio(input_txt):
    file = openai.audio.speech.create(
        model = "tts-1",
        voice = "alloy",
        response_format = 'mp3',
        input = input_txt
    )
    # with open(RESPONSE_AUDIO_PATH, 'wb') as audio_file:
    #     audio_file.write(file)
    file.stream_to_file(RESPONSE_AUDIO_PATH)
    return file

def play_audio(path=RESPONSE_AUDIO_PATH):
    playsound(path)

def audio_to_text(audio_file_path):
    audio_file = open(audio_file_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript

def audio_chatroom():
    ## txt --> audio
    print("Hi there, welcome to the CozyRoom, chat with me about any thing you are worrying about. Type 'exit' to end the conversation")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("See you. Have a nice day, bye~")
            break
        
        reply = chatbot(user_input)
        print(f"CozyRoom: {reply}")

        # tts
        text_to_audio(reply)
        play_audio()
    
    """
    todo
    record audio
    rag
    """

if __name__ == "__main__":
    audio_chatroom()
