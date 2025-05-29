import streamlit as st
from app.llm import get_ai_response, get_ai_response_stream


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "called_agent" not in st.session_state:
    st.session_state.called_agent = False
if "suggestions" not in st.session_state:
    st.session_state.suggestions = None
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""  # To track last prompt used for suggestions

def call_agent(prompt: str):
    st.session_state.last_prompt = prompt  # Store the last prompt
    st.session_state.called_agent = True
    
    response_stream = get_ai_response_stream(prompt)
    
    response_text = ""
    with st.spinner("🤔 Thinking..."):
        for i in response_stream:
            response_text += i.content

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response_text}
    )
    
    st.session_state.suggestions = None
    

def render_suggestions(prompt:str):
    cols = st.columns(2)
    
    if st.session_state.suggestions is None:
        st.session_state.suggestions = get_ai_response(prompt)
    
    for i, q in enumerate(st.session_state.suggestions):
        if cols[i % 2].button(q, key=f"sugg_{q}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": q})
            call_agent(q)
            st.rerun()


# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Show suggested questions only if it's the first message
if len(st.session_state.messages) == 0 and not st.session_state.called_agent:
    st.markdown("### 💡 Suggested Questions", unsafe_allow_html=True)
    render_suggestions("Suggest 4 short starting questions strictly based on knowledge base to ask the agent.")

# Chat input at the bottom
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    call_agent(prompt)
    st.rerun()  # Rerun to update chat history

# After displaying chat history and handling chat input
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    st.markdown("**Try another question:**")
    render_suggestions(f"Suggest 2 short follow-up prompt recommendations relevant to chat history and 2 other suggestions based on knowledge base.")