import io
import re
import json
import time
import wave
import requests
import simpleaudio as sa
import ollama

from mlx_lm import load, generate

# 是否使用OLLMA
USE_OLLAMA = True
# OLLMA模型
OLLMA_MODEL = 'qwen:32b-chat-v1.5-q4_0'
# safetensors模型
SAFETENSORS_MODEL = 'Qwen1.5-32B-Chat-4Bit'

def generate_speech(text, port):
    time_ckpt = time.time()
    data={
        "text": text,
        "text_language": "zh"
    }
    response = requests.post("http://127.0.0.1:{}".format(port), json=data)
    if response.status_code == 400:
        raise Exception(f"GPT-SoVITS ERROR: {response.message}")
    audio_data = io.BytesIO(response.content)
    with wave.open(audio_data, 'rb') as wave_read:
        audio_frames = wave_read.readframes(wave_read.getnframes())
        audio_wave_obj = sa.WaveObject(audio_frames, wave_read.getnchannels(), wave_read.getsampwidth(), wave_read.getframerate())
    play_obj = audio_wave_obj.play()
    play_obj.wait_done()
    print("Audio Generation Time: %d ms\n" % ((time.time() - time_ckpt) * 1000))

def split_text(text):
    sentence_endings = ['！', '。', '？']
    for punctuation in sentence_endings:
        text = text.replace(punctuation, punctuation + '\n')
    pattern = r'\[.*?\]'
    text = re.sub(pattern, '', text)
    return text

def generate_by_ollama(question):
    response = ollama.chat(model=OLLMA_MODEL, messages=[
          {
            'role': 'user',
            'content': question,
          },
        ],
        stream=False
    )    
    return response['message']['content']

if __name__ == "__main__":
    if not USE_OLLAMA:
        with open('../models/' + SAFETENSORS_MODEL + '/tokenizer_config.json', 'r') as file:
            tokenizer_config = json.load(file)
        
        model, tokenizer = load(
            "../models/" + SAFETENSORS_MODEL + "/",
            tokenizer_config=tokenizer_config
        )

    questions = []
    with open('../text/questions.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                questions.append(line)

    sys_msg = 'You are a helpful assistant'

    template = ''
    if not USE_OLLAMA:
        with open('../text/chat_template.txt', 'r') as template_file:
            template = template_file.read()

    for question in questions:
        prompt = template.replace("{usr_msg}", question)
        print("%s: %s" % ("问题", question))
        question = split_text(question)
        generate_speech(question, 9880)
        

        time_ckpt = time.time()
        if USE_OLLAMA:
            response = generate_by_ollama(question)            
        else:            
            response = generate(
                model,
                tokenizer,
                prompt=prompt,
                temp=0.3,
                max_tokens=500,
                verbose=False
            )
    

        print("%s: %s (Time %d ms)\n" % ("哔友", response, (time.time() - time_ckpt) * 1000))
        response = split_text(response)
        generate_speech(response, 9881)