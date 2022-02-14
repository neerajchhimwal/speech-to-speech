from punctuate.punctuate_text import Punctuation

# import gradio as gr

english = Punctuation('en')
# hindi = Punctuation('hi')
def punct(text):
    if text:
        return ' '.join(english.punctuate_text([text]))
    else:
        return ' '
'''   
textbox = gr.inputs.Textbox(lines=5, placeholder='Enter unpunctuated English sentences here', default="", label="Punctuation")
iface = gr.Interface(fn=punct, inputs=textbox, outputs="text", server_port=8888, server_name="0.0.0.0")
iface.launch(share=True)
'''

    
if __name__ == "__main__":
    print(punct('hello how are you doing'))
