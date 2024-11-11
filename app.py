import streamlit as st
import hmac

import os
import time
from helpers import text_to_speech, autoplay_audio, speech_to_text
from generate_answer import base_model_chatbot, with_pdf_chatbot
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

def main():
    float_init()

    def initialize_session_state():
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi there, welcome to the CozyRoom, chat with me about any thing you are worrying about"}
            ]
        if "button_flag" not in st.session_state:
            st.session_state.button_flag = False
        if "audio_bytes" not in st.session_state:
            st.session_state.audio_bytes = None


    initialize_session_state()

    st.title("CoZY Room")             

    
    footer_container = st.container()
    with footer_container:
        col1, col2 = st.columns([4,3])
        with col1:
            st.session_state.audio_bytes = audio_recorder(
                text='Click the Mic and begin speaking', 
                icon_name='microphone', 
                icon_size='2x'
            )
        with col2:
            new_button_flag = st.toggle("Ask for specific info")
            if new_button_flag != st.session_state.button_flag:
                st.session_state.audio_bytes = None
            st.session_state.button_flag = new_button_flag

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


    if st.session_state.audio_bytes:
        with st.spinner("Transcribing..."):
            webm_file_path = "temp_audio.mp3"
            with open(webm_file_path, "wb") as f:
                f.write(st.session_state.audio_bytes)

            transcript = speech_to_text(webm_file_path)
            if transcript:
                st.session_state.messages.append({"role": "user", "content": transcript})
                with st.chat_message("user"):
                    st.write(transcript)
                os.remove(webm_file_path)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking🤔..."):
                if not st.session_state.button_flag:
                    print('--------->', st.session_state.messages)
                    final_response = base_model_chatbot(st.session_state.messages)
                elif st.session_state.button_flag:
                    print('--------->', st.session_state.messages)
                    final_response = with_pdf_chatbot(st.session_state.messages)
            # with st.spinner("Generating audio response..."):
            #     audio_file = text_to_speech(final_response)
            #     autoplay_audio(audio_file)
            st.write(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})
            # os.remove(audio_file)

    # Float the footer container and provide CSS to target it with
    footer_container.float("bottom: 0rem;")
 
if __name__ == "__main__":

    main()