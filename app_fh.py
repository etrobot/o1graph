from fasthtml.common import *
from graph import generate_response_graph
import time
from asyncio import sleep

hdrs = (Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),)
app, rt = fast_app(hdrs=hdrs)

@rt("/")
def get():
    return Titled("o1graph: Create o1 reasoning chain using Langgraph",
        Form(method="post", action="/query", hx_post="/query", hx_target="#response-container")(
            Group(
                Input(name="user_query", placeholder="For example, how many 'r' are in the word 'strawberry'?"),
                Button("Go", type="submit")
            )
        ),
        Div(id="response-container", 
                             hx_ext="sse", 
                             sse_connect="",  # SSE connection path will be dynamically set
                             sse_close="close",
                             hx_swap="beforeend", 
                             sse_swap="message")
    )

@rt("/query")
def post(user_query: str):
    return Div(id="response-container", 
            hx_ext="sse", 
            sse_connect=f"/query-stream?query={user_query}", 
            sse_close="close",
            hx_swap="beforeend",
            sse_swap="message"
        )

async def response_generator(user_query: str):
    app = generate_response_graph()
    if not user_query:
        yield 'event: close\ndata:\n\n'
        return
    
    rendered_steps = set()  # Used to track rendered steps
    
    try:
        for result in app.stream({"message": user_query}):
            current_node = list(result.keys())[0]
            if 'initialize' in result:
                continue
            elif 'process_step' in result or ('condition_node' in result and 'Final Answer' in result['condition_node']['steps'][-1]):
                steps = result.get('process_step', {}).get('steps') or result['condition_node']['steps']
                for step in steps:
                    if isinstance(step, (list, tuple)) and len(step) == 3:
                        title, content, thinking_time = step
                    else:
                        # Handle unexpected step format
                        title = "Unknown Step"
                        content = str(step)
                        thinking_time = 0.0
                    
                    step_key = f"{title}:{content[:50]}"  # Create a unique step identifier
                    if step_key not in rendered_steps:
                        yield sse_message(
                            Details(
                                Summary(f"{title} ({thinking_time:.2f} seconds)"),
                                P(content)
                            )
                        )
                        rendered_steps.add(step_key)
                        await sleep(0.1)  # Small delay to simulate gradual updates
                
                if 'condition_node' in result:
                    final_step = steps[-1]
                    if isinstance(final_step, (list, tuple)) and len(final_step) >= 2:
                        yield sse_message(
                            H3("Final Answer"),
                            P(final_step[1])
                        )
                    total_thinking_time = result['condition_node'].get('total_thinking_time', 0.0)
                    yield sse_message(P(f"Total thinking time: {total_thinking_time:.2f} seconds"))
    except Exception as e:
        yield sse_message(
            H3("Error"),
            P(f"An error occurred: {str(e)}")
        )
    
    yield 'event: close\ndata:\n\n'

@rt("/query-stream")
async def get(query: str):
    return EventStream(response_generator(query))

serve()