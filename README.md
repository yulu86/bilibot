# 哔哩哔哩聊天机器人

由[哔哩哔哩](https://bilibili.com)用户评论微调训练而成的本地聊天机器人。支持文字聊天，也可以通过 questions.txt 生成针对给定问题的语音对话。

本项目文字生成使用的基础模型为 [Qwen1.5-32B-Chat](https://huggingface.co/Qwen/Qwen1.5-32B-Chat)，借助苹果 [mlx-lm LORA 示例项目](https://github.com/ml-explore/mlx-examples/blob/main/llms/mlx_lm/LORA.md) 对基础模型进行微调训练。语音生成部分基于开源项目 [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)，问题语音来自 B 站用户[白菜工厂1145号员工](https://space.bilibili.com/518098961)训练的派蒙语音模型。

### 文件结构

项目主要脚本存放在 `main/` 文件夹下，模型存放于 `models/` 文件夹。提示词模板、问题列表存放在 `text/` 文件夹下。`tools/compress_model.py` 可以对完整模型进行量化压缩，大大加快模型内容生成速度。

## 运行指南

本项目基于 Python 编程语言，程序运行使用的 Python 版本为 3.10，建议使用 [Anaconda](https://www.anaconda.com) 配置 Python 环境。以下配置过程已在 macOS 系统测试通过。


### 配置环境

```
conda create -n bilibot python=3.10
conda activate bilibot
cd bilibot
python3 -m pip install -r requirements.txt
```

### 模型微调训练与推理测试

使用控制台指令，借助 [mlx-lm](https://github.com/ml-explore/mlx-examples/blob/main/llms/mlx_lm/LORA.md) 对 Qwen1.5-32B-Chat 进行微调：

```
python3 -m mlx_lm.lora --model models/Qwen1.5-32B-Chat --data data/ --train --iters 1000 --batch-size 16 --lora-layers 12

python3 -m mlx_lm.lora --model models/Qwen1.5-1.8B --data data/ --train --iters 1000 --batch-size 16 --lora-layers 12
```

将微调后的 `adapters` 文件与基础模型合并：

```
python3 -m mlx_lm.fuse --model models/Qwen1.5-32B-Chat --save-path models/Qwen1.5-32B-Chat-FT --adapter-path models/Qwen1.5-32B-Chat-Adapters
```

对合并后的模型进行量化加速：
python3 tools/compress_model.py

对微调训练后的模型进行对话测试：
python3 chat.py

### 语音生成
本项目借助开源项目 [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) 进行语音生成。

首先参考 [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) 的官方指南配置环境并运行语音生成程序。

```
conda create -n GPTSOVITS python=3.9
conda activate GPTSOVITS
cd GPT-SoVITS
python3 -m pip install -r requirements.txt
python3 webui.py
```

运行 api 程序，分别使用端口 9880 与 9881 提供派蒙与林亦的语音生成服务，以下请使用 GPT-SoVITS 代码库完成：
```
python3 api.py -s SoVITS_weights/XiaoNingZi_v1_e15_s225.pth -g GPT_weights/XiaoNingZi_v1-e15.ckpt -dr samples/XiaoNingZi/content2.wav -dt "要感谢一键三连的小伙伴们，也要感谢陪我，从几百粉走到现在的老朋友们，谢谢你们。" -dl "zh" -a 127.0.0.1 -p 9881

python3 api.py -s SoVITS_weights/XiaoNingZi_v1_e15_s225.pth -g GPT_weights/XiaoNingZi_v1-e15.ckpt -dr samples/XiaoNingZi/content.wav -dt "好，视频的最后祝大家新年快乐，龙年走大运" -dl "zh" -a 127.0.0.1 -p 9880
```

运行问答生成程序：
```
python3 start_qa_dialogue.py
```

## 参考

1. 机器学习框架 MLX，来自苹果机器学习研究组：https://github.com/ml-explore/mlx
2. 阿里通义千问 Qwen1.5：https://qwenlm.github.io/zh/blog/qwen1.5/
3. 开源文本转语音项目 GPT-SoVITS，作者[花儿不哭](https://space.bilibili.com/5760446)：https://github.com/RVC-Boss/GPT-SoVITS
4. 派蒙语音模型，作者[白菜工厂1145号员工](https://space.bilibili.com/518098961)：[【GPT-SoVITS】30小时超大数据集测试，堆时长真的有用吗？](https://www.bilibili.com/video/BV1Yu4m1N79m)