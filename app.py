import gradio as gr
from query import ask


def handle_query(question):
    if not question or not question.strip():
        return "Please enter a question.", ""

    result = ask(question.strip())

    answer = result["answer"]
    sources = "\n".join(f"• {source}" for source in result["sources"])

    return answer, sources


with gr.Blocks() as demo:
    gr.Markdown("# Unofficial UH Mānoa CS Professor Guide")
    gr.Markdown(
        "Ask a question about CS professor research interests or student review information. "
        "Answers are generated only from the retrieved documents."
    )

    question = gr.Textbox(
        label="Your question",
        placeholder="Example: What do students say about Andrey Popov's exams?",
        lines=2,
    )

    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=6)

    ask_button.click(
        handle_query,
        inputs=question,
        outputs=[answer, sources],
    )

    question.submit(
        handle_query,
        inputs=question,
        outputs=[answer, sources],
    )


if __name__ == "__main__":
    demo.launch()
