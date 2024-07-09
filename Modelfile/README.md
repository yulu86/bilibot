# 创建ollama model

## 执行
```
ollama create qwen:32b-chat-v1.5-q4_0_bilibot -f ./Modelfile/Modelfile_qwen1.5-32B-chat-q4_bili

ollama create qwen:32b-chat-v1.5-q4_0_stable_diffusion -f ./Modelfile/Modelfile_qwen1.5-32B-chat-q4_stable_diffusion

ollama create qwen:32b-chat-v1.5-q4_0_xiaohongshu -f ./Modelfile/Modelfile_qwen1.5-32B-chat-q4_xiaohongshu

ollama create qwen:32b-chat-v1.5-q4_0_zhihu -f ./Modelfile/Modelfile_qwen1.5-32B-chat-q4_zhihu

ollama create qwen:32b-chat-v1.5-q4_0_weibo -f ./Modelfile/Modelfile_qwen1.5-32B-chat-q4_weibo

ollama create llama3-70b-chinese_bili -f ./Modelfile/Modelfile_llama3-70b-chinese-chat_bili
ollama create llama3-70b-chinese_weibo -f ./Modelfile/Modelfile_llama3-70b-chinese-chat_weibo
ollama create llama3-70b-chinese-instruct_coder -f ./Modelfile/Modelfile_llama3-70b-chinese-instruct_coder

ollama create codestral-harmoneyos-next:22b -f ./Modelfile/Modelfile_codestral-22b-harmoneyos_next
```