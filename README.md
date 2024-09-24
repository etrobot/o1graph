# o1graph
Using LangGraph to create o1-like reasoning chains.

This is an early prototype of using prompting to create o1-like reasoning chains to improve LLM output accuracy. It is not perfect and accuracy has yet to be formally evaluated.

Inspired by the [groq-g1 project](https://github.com/bklieger-groq/g1).



https://github.com/user-attachments/assets/bd03cfa0-c530-4e64-9ee1-f4e29a5cd7ea

### Quickstart
~~~
Rename .env_example to .env and fill out the necessary information.
~~~
~~~
python3 -m venv venv
~~~
~~~
source venv/bin/activate
~~~
~~~
pip3 install -r requirements.txt
~~~
~~~
streamlit run app.py
~~~
