import streamlit as st
from graph import generate_response_graph
import streamlit_mermaid as stmd
import time

def main():
    st.set_page_config(page_title="g1 prototype", page_icon="🧠", layout="wide")
    
    st.title("o1graph: Using Langgraph to create o1-like reasoning chains")
    
    st.markdown("""
    This is an early prototype of using prompting to create o1-like reasoning chains to improve LLM output accuracy. It is not perfect and accuracy has yet to be formally evaluated.
    The inspiration for [o1graph](https://github.com/etrobot/o1graph) is the [groq-g1](https://github.com/bklieger-groq/g1) project.
    """)

    mermaid_base = """
    graph TD;
        __start__([<p>__start__</p>])
        initialize(Initialize)
        process_step(Process Step)
        condition_node(Final Answer or Loop)
        __end__([<p>__end__</p>])
        __start__ --> initialize;
        condition_node --> __end__;
        initialize -.-> process_step;
        process_step -.-> condition_node;
        condition_node -.-> process_step;
        style {current_node} stroke:#23b883,stroke-width:8px
    """

    # Create a placeholder for the Mermaid chart
    sidebar_mermaid = st.sidebar.empty()

    # Initialize a counter for unique keys
    if 'mermaid_counter' not in st.session_state:
        st.session_state.mermaid_counter = 0

    # Function to update the Mermaid chart
    def update_mermaid(current_node):
        mermaid_code = mermaid_base.format(current_node=current_node)
        with sidebar_mermaid:
            stmd.st_mermaid(mermaid_code, height="500px", key=f"mermaid_{st.session_state.mermaid_counter}")
            st.session_state.mermaid_counter += 1


    # Initial state
    update_mermaid("__start__")

    # Text input for user query
    user_query = st.text_input("Enter your query:", placeholder="For example, how many 'r's are in the word 'strawberry'?")
    
    if user_query:
        st.write("Generating response...")
        
        # Create empty elements to hold the generated text and total time
        response_container = st.empty()
        time_container = st.empty()
        
        # Generate and display the response
        app = generate_response_graph()
        for result in app.stream({"message": user_query}):
            current_node = list(result.keys())[0]
            with response_container.container():
                if 'initialize' in result:
                    continue
                elif 'process_step' in result:
                    update_mermaid(current_node)
                    steps = result['process_step']['steps']
                    for step in steps:
                        title, content, thinking_time = step
                        with st.expander(f"{title} ({thinking_time:.2f} seconds)", expanded=True):
                            st.markdown(content, unsafe_allow_html=True)
                elif 'condition_node' in result and 'Final Answer' in result['condition_node']['steps'][-1]:
                    steps = result['condition_node']['steps']
                    for step in steps:
                        title, content, thinking_time = step
                        with st.expander(f"{title} ({thinking_time:.2f} seconds)", expanded=True):
                            st.markdown(str(content), unsafe_allow_html=True)
                    final_step = steps[-1]
                    st.markdown(f"### Final Answer")
                    content = final_step[1]
                    st.markdown(str(content), unsafe_allow_html=True)
                    total_thinking_time = result['condition_node']['total_thinking_time']
                    time_container.markdown(f"**Total thinking time: {total_thinking_time:.2f} seconds**")

        update_mermaid("__end__")

if __name__ == "__main__":
    main()