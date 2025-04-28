# llm-rag-demo
A demo on running prompt against your private data

## Overview

This code demonstrates how the RAG works. It is not a highly optimized or sophisticated solution but provides a straightforward explanation of the RAG's concept.


### How it Works
This program reads pdf file where the pages are in image format. Files are located at `/data/story2.pdf`. 

`src/01_pdf_reader.py` -> reads pdf file and convert to text. Store text file at `data/text` folder

`src/02_split_and_chunk.py` -> reads all files in `data/text` folder. Split, create chunks and store in `chromadb` at `data/chormadb`

`src/03_vector_search.py` -> reads question in `.env` file , search vector db and prompt Gemini LLM for the answer.



## Prerequisites

- Docker must be installed and running locally.
- `Google Gemini API KEY` created in your gen AI Studio.

## Usage

Run a docker build from root directory. It take approximately 5 - 10 mins to build
```bash
docker build -t rag1 -f deploy/dockerfile .
```


Shell into docker container

```bash
docker run -it  -v ${PWD}/:/app rag1  bash
```


Export GEN AIP key and execute all three programs one after the other:

```bash
export GENAI_API_KEY=AIzaSyBU.....BZr92FAIOHM
root@adc7990ddc56:/app# python src/01_pdf_reader.py
root@adc7990ddc56:/app# python src/02_split_and_chunk.py
root@adc7990ddc56:/app# python src/03_vector_search.py
```

### Example Output

```
root@adc7990ddc56:/app# python src/03_vector_search.py
Question: What is the Story summary of Magic Sword ?
 Answer: A man named Sasank used a magic sword obtained from a yogi. It was just a coincidence that the sword has magic powers. As word spreads that the crown-princess’s fiancé possesses a sword with magic sword capable of winning any battle, he obtained the sword unfairly and does not deserve to become king.
```


### How to get Gemini API Key

- Go to aistudio https://aistudio.google.com/prompts/new_chat
- Click on `Get API key`
- Create API key

API_KEY format `AIzaSyBUi2SZq.......wAli8CxbdBZr92FAI`

### How to change question
To change question update `.env` file

```

# export GENAI_API_KEY=AIza.....IOHM

# GENERAL
...
QUESTION=What is the Story summary of Magic Sword ?  # change this
...
```
