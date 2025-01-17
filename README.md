# Ceterni-Bot

![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat)
![MySQL](https://img.shields.io/badge/-MySQL-4479A1?logo=mysql&logoColor=white&style=flat)
![Twilio](https://img.shields.io/badge/-Twilio-008CFF?logo=twilio&logoColor=white&style=flat)
![OpenAI](https://img.shields.io/badge/-OpenAI-FF4B4B?logo=openai&logoColor=white&style=flat)
![LangChain](https://img.shields.io/badge/-LangChain-4C51BF?logo=langchain&logoColor=white&style=flat)
![Pinecone](https://img.shields.io/badge/-Pinecone-2F2F2F?logo=pinecone&logoColor=white&style=flat)

Ceterni-Bot is a trustable assistant designed to assess anxiety levels through a series of five carefully crafted questions. This project was presented at the Hackathon 2023 and leverages multiple technologies to provide an insightful analysis. 

**Ceterni-Bot** is implemented using OpenAI technology, and it has been specifically trained to operate as Ceterni, providing accurate anxiety assessments through its advanced capabilities.


## Overview

Ceterni-Bot is an innovative solution for identifying anxiety in individuals. It uses a combination of modern Python libraries and frameworks to deliver accurate and meaningful assessments. The bot interacts with users through a series of five questions and analyzes their responses to gauge anxiety levels.

## Features

- **Anxiety Assessment**: Utilizes five specific questions to determine the anxiety level of a person.
- **Integration with Twilio**: Provides SMS-based interactions.
- **Advanced Language Processing**: Employs OpenAI and LangChain for natural language understanding.
- **Data Storage**: Uses Pinecone and MySQL for efficient data management and retrieval.

## Technologies Used

- **Python**: Programming language used for the development.
- **Poetry**: Dependency management and packaging.
- **Twilio**: Communication via SMS.
- **OpenAI**: Natural language processing.
- **LangChain**: Language model chaining.
- **Pinecone Client**: Vector database for similarity search.
- **Python-dotenv**: Environment variable management.
- **Tiktoken**: Tokenization library.
- **Flask**: Web framework for building the API.
- **ChromaDB**: Database for managing document embeddings.
- **MySQL Connector**: Database connector for MySQL.

## Installation

To get started with Ceterni-Bot, clone the repository and install the dependencies using Poetry:

```bash
git clone https://github.com/micode1502/Ceterni-Bot.git
cd ceterni-bot
poetry install
```

## Running the Bot

After installation, you can run the bot using the following command:

```bash
poetry run python main.py
```

## Author

- **Dara Elizabeth**
- **Dilmer Altamirano**