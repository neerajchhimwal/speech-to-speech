'''
Run this to test translation from En to Indic after running s2s_installs as mentioned in README
'''

from fairseq import checkpoint_utils, distributed_utils, options, tasks, utils
from indicTrans.inference.engine import Model
en2indic_model = Model(expdir='./en-indic')

# import gradio as gr

def run_translate(en_sent):
    if en_sent.strip():
        return en2indic_model.translate_paragraph(en_sent, 'en', 'hi')
    else:
        return ' '

'''
textbox = gr.inputs.Textbox(placeholder="Enter English text here", default="", label="Translation")
iface = gr.Interface(fn=run_translate, inputs=textbox, outputs="text")
iface.launch(share=True)
'''

    
if __name__ == "__main__":
    print(run_translate('hey, how are you?'))
