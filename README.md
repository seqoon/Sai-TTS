# Egyptian  Colloquial Arabic Text-to-Speech <!-- omit in toc -->

[![GitHub](https://img.shields.io/badge/GitHub-SeqoonTTS-blue?style=flat-square)](https://github.com/AbdoKhaled-2021/SeqoonTTS)
[![License](<https://img.shields.io/badge/License-Proprietary-darkred.svg>)](./LICENSE)
[![Python](<https://img.shields.io/badge/Python-3.12-blue>)](https://www.python.org/)
[![PyTorch](<https://img.shields.io/badge/PyTorch-2.5.1+cu124-FF5733>)](https://pytorch.org/)
[![TTS](<https://img.shields.io/badge/TTS-0.25.1-green>)](https://github.com/idiap/coqui-ai-TTS)
[![Transformers](<https://img.shields.io/badge/Transformers-4.46.2-yellow>)](https://github.com/huggingface/transformers)

## Table of Contents <!-- omit in toc -->

- [Getting Started](#getting-started)
- [Project structure](#project-structure)
- [TTS Data Pre-processing](#tts-data-pre-processing)
- [Exploratory Training Data Analysis](#exploratory-training-data-analysis)
- [TTS Model Training](#tts-model-training)
- [TTS Model Evaluation](#tts-model-evaluation)
- [TTS Model Deployment](#tts-model-deployment)
- [Requirements and Dependencies](#requirements-and-dependencies)
- [References](#references)
  - [Project Resources](#project-resources)
  - [XTTSv2](#xttsv2)


## Getting Started

> Train and Evaluate a TTS Model **(i.e. XTTSv2)** on **automatically collected Egyptian colloquial Arabic weakly labeled speech data**. The Trained TTS model should be of **high enough quality** to be used as the **First high quality TTS Model in the EGP dialect**.


## Project structure

```txt
.
├── api
├── assets
├── data
├── notebooks
├── scripts
└── src
```


## TTS Data Pre-processing

- TBC

## Exploratory Training Data Analysis

- TBC

## TTS Model Training

- TBC

## TTS Model Evaluation

- TBC

## TTS Model Deployment

- TBC

## Requirements and Dependencies

- Ubuntu 24.04 **OR** Ubuntu 22.04
- [miniconda3](https://docs.anaconda.com/miniconda/install/)
- A CUDA-Enabled NVIDIA GPU
- CUDA 12.4

```bash
# Quick miniconda3 command line install [OPTIONAL]

mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

```bash
# Project Dependencies

sudo apt update && sudo apt upgrade -y

sudo apt install build-essential git curl wget
sudo apt install gcc gcc-multilib g++ g++-multilib libboost-dev cmake
sudo apt install ffmpeg sox libsox-fmt-mp3 libsox-dev libavcodec-dev libsndfile1 pulseaudio

sudo apt clean && sudo apt autoremove

conda create -n tts python=3.12 -y
conda activate tts

python -m pip install --upgrade pip

conda install -c conda-forge ffmpeg sox
pip install --no-deps -r requirements.txt
```


## References

### Project Resources

- [Egyptian Speech Dataset](https://www.kaggle.com/datasets/iraqyomar/egyspeech/data)
- [400K Egyptian Arabic Lines](https://www.kaggle.com/datasets/fadisarwat/egyptian-arabic-lines)
- [Project's Github repository](https://github.com/AbdoKhaled-2021/SeqoonTTS)

### XTTSv2

- [XTTS: a Massively Multilingual Zero-Shot Text-to-Speech Model](https://arxiv.org/pdf/2406.04904)
- [coqui-tts docs](https://coqui-tts.readthedocs.io/en/latest/)
- [coqui-tts github](https://github.com/idiap/coqui-ai-TTS)
- [Auralis TTS Engine](https://www.astramind.ai/post/auralis)
- [Auralis TTS Engine Github Repository](https://www.astramind.ai/post/auralis)
