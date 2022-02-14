from infer_asr import *

import os
from tempfile import NamedTemporaryFile
# from flask import Flask, request, jsonify
import sys
# from flask_cors import CORS, cross_origin
# import json
# import cgi
# import contextlib
# import wave

import os
import subprocess

import nnresample
from timestamp_generator import extract_time_stamps
import gradio as gr
import requests
import base64
import time

from scipy.io.wavfile import read, write
import io

from punctuate_wrapper import punct
from translate import run_translate
from tts_inference import run_tts_paragraph


def wav_to_pcm16(wav):
    ints = (wav * 32768).astype(np.int16)
    little_endian = ints.astype('<u2')
    wav_bytes = little_endian.tobytes()
    return wav_bytes

def infer_with_gradio(wav_file):
    t1 = time.time()
    signal, sr = sf.read(wav_file.name)
    signal = signal.mean(-1)
    resampled_signal = nnresample.resample(signal, 16000, 44100)
    
    wav_bytes = wav_to_pcm16(resampled_signal)
    start_times, end_times = extract_time_stamps(wav_bytes)
    stt_output = []

    for i in range(len(start_times)):
        chunk = resampled_signal[int(start_times[i]*16000): int(end_times[i]*16000)]
        result = wav2vec_obj.get_results(wav_path=chunk, use_cuda=True)        
        stt_output.append(result)

    asr_result = ' '.join(stt_output)
    punct_result = punct(asr_result)
    translate_result = run_translate(punct_result)
    #num_to_words_on_translation_result = normalize_nums(translate_result, lang='hi')

    tts_result = run_tts_paragraph(translate_result, lang='hi')

    return asr_result, punct_result, translate_result, tts_result

def run_gradio():
    audio = gr.inputs.Audio(source="microphone", type="file")
    # dropdown = gr.inputs.Dropdown(choices=['Hi-Female', 'Hi-Male'], type="value", default='Hi-Male', label=None)
    output = [gr.outputs.Textbox(label="Speech to Text"), gr.outputs.Textbox(label="Punctuation"), gr.outputs.Textbox(label="Translation"), gr.outputs.Audio(type="numpy", label="TTS")]
    # output = gr.outputs.Textbox(label="Speech to Text")
    iface = gr.Interface(fn=infer_with_gradio, inputs=[audio], outputs=output,
    server_port=8889, server_name="0.0.0.0", enable_queue=True, theme='huggingface', layout='vertical', title='Speech to Speech Translation: En to Hi')

    iface.launch(share=True)

if __name__ == "__main__":
    global wav2vec_obj, cuda
    parser = argparse.ArgumentParser(description='Run')
    parser.add_argument('-m', '--model', type=str, help="Custom model path")
    parser.add_argument('-d', '--dict', type=str, help="Dict path")
    parser.add_argument('-w', '--wav', type=str, help= "Wav file path")
    parser.add_argument('-c', '--cuda', default=False, type=bool, help="CUDA True or False")
    parser.add_argument('-D', '--decoder', type=str, help= "Which decoder to use kenlm or viterbi")
    parser.add_argument('-l', '--lexicon', default=None, type=str, help= "Lexicon path if decoder is kenlm")
    parser.add_argument('-L', '--lm-path', default=None, type=str, help= "Language mode path if decoder is kenlm")
    parser.add_argument('-H', '--half', default=False, type=bool, help="Half True or False")
    #parser.add_argument('-T', '--tts-model', default=None, type=str, help= "TTS: can be 'Hi-Male' or 'Hi-Female'")

    
    args_local = parser.parse_args()
    print("Dictionary Loaded")
    target_dict = Dictionary.load(args_local.dict)
    print("Model Loaded")
    model = get_model(args_local.cuda, args_local.model, args_local.half)
    print("Generator Loaded")
    generator = get_decoder(target_dict, args_local.decoder, args_local.lexicon, args_local.lm_path)
    
    cuda = args_local.cuda
    wav2vec_obj = customWav2vec(model, target_dict, generator, args_local.half)
    # result = wav2vec_obj.get_results(args_local.wav_path, args_local.cuda)
    # print(result)
    # app.run(host='localhost', port=8888, debug=True, use_reloader=False)
    run_gradio()
