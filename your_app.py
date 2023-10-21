import streamlit as st
import os
from PIL import Image
import openai 

from model import get_stream_of_data, arrange_chat

os.chdir(os.path.dirname(__file__))
st.set_page_config(layout="wide")
st.markdown("### AI-Analyst ")

#### Display Image code-- edit for the initial messaging####
col1, col2=st.columns((3,1))
with col1:
    st.markdown(
    f"""
        This is a chatbot built using transcripts from [All-In Podcast -EP112](https://allintranscripts.substack.com/p/transcript-of-e112-is-davos-a-grift) :
        - `Jason`, `Chamath`, `Friedberg` and `Sacks` discuss the top Republican candidates for the 2024 election
        -  They then move on to the World Economic Forum in Davos, evaluating the current US free trade policy. 
         - Rebuilding infrastructure while avoiding the debt ceiling and immigration reform before delving into the topic of TikTok's endgame in the US. 
         - Explore the intersection of Pharma and AI, and the most successful `AI` business models.
        """)
    
with col2:## convert to relative path
    image_1=Image.open(f'{os.getcwd()}/all-in.png')
    #image_1=Image.open('../app/image/dog_img1.png')
    st.image(image_1)


if "is_auth" not in st.session_state.keys():
    st.session_state["is_auth"]=False

with st.sidebar:
    openapi_key=st.text_input('please use your openapi key to run this')
    button_op=st.button('openapi key')
    if button_op and openapi_key:
        try:
            openai.api_key=openapi_key
            openai.Model.list()
            st.session_state["is_auth"]=True

        except openai.error.AuthenticationError as e:
            st.write(str(e))
            st.warning('please enter correct openapi key')
        except openai.error.APIConnectionError as e:
            st.write(str(e))
            st.warning('please enter correct openapi key')



##################
### openai- streamlit
@st.cache_data()
def initialize_data():
    chat_data=get_stream_of_data()
    messages=[{"role": f'{item[0]}' , "content":f'{item[1]}'} for item in chat_data]
    messages.insert(0,{"role": "system", "content": "You are an expert level analyst "})

    return messages[:104]

def allow_chat():

    if "messages" not in st.session_state.keys():
        messages=initialize_data()
        st.session_state["messages"]=messages

    if "messages_len" not in st.session_state.keys():
        st.session_state["messages_len"]=len(st.session_state["messages"])

    if "openai_model" not in st.session_state.keys():
        st.session_state["openai_model"] = "gpt-3.5-turbo"


    for message in st.session_state.messages[st.session_state["messages_len"]:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Please let me know how can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            response_openai=openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0.7,
                stream=True,
            )

            for response in response_openai:
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

try: 
    if st.session_state["is_auth"]:
        allow_chat()
except Exception:
    st.warning('please enter correct openapi key ')


