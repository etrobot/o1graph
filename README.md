# o1graph
Using LangGraph to create o1-like reasoning chains.

This is an early prototype of using prompting to create o1-like reasoning chains to improve LLM output accuracy. It is not perfect and accuracy has yet to be formally evaluated.

Inspired by the [groq-g1 project](https://github.com/bklieger-groq/g1).

### Flow

graph TD;
        __start__([<p>__start__</p>]):::first
        initialize(initialize)
        process_step(process_step)
        generate_final_answer(generate_final_answer)
        __end__([<p>__end__</p>]):::last
        __start__ --> initialize;
        generate_final_answer --> __end__;
        initialize -.-> process_step;
        generate_final_answer -.-> process_step;
        process_step -.-> generate_final_answer;


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