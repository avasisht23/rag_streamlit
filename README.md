# Multi-Document Question-Answering App

The chatbot uses a Retrieval Augmented Generation (RAG) pipeline to answer questions about company earnings calls. Core technologies include [LlamaIndex](https://docs.llamaindex.ai/en/stable) for the query engine, [Qdrant](https://qdrant.tech) for the vector database, and [StreamLit](https://share.streamlit.io/) for hosting the Python-based web application.

The application demo is available [here](https://avasisht23-rag-demo.streamlit.app/) to try!

To learn more, check out [this notion doc](https://ultra-blarney-71a.notion.site/RFC-Document-Based-Q-A-Chatbot-d0fb35d64e794326a31ae4b45eb120e5?pvs=4).

## Setup the Dev Environment

The required Python version is at least `3.9`. The demo was built with `3.9.12` using a Python virutal environment.

To replicate the development environment, execute the following commands on your terminal from the root folder of the repo.

First, create a Python virtual environment and activate it.
```
python -m venv venv
source venv/bin/activate
```

Then, install all dependencies in this environment:
```
pip install -r requirements.txt
```

Lastly, copy `.streamlit/sample.secrets.toml` into `.streamlit/secrets.toml`, and `sample.env` into `.env` and paste in your environment variables. These will include the OpenAI API key, Qdrant API key, and Qdrant hosted database URL for connection.

## Initialize the Vector DB

Qdrant enables both local and cloud-hosted connections to a vector database. 

To run a Qdrant vector database locally, download [Docker Desktop](https://www.docker.com/products/docker-desktop/) and then execute the following commands to download the Docker image and run it on a container:

```
docker pull qdrant/qdrant
docker run -p 6333:6333 qdrant/qdrant
```

Otherwise, ensure you have in `QDRANT_API_KEY` and `QDRANT_URL` in your `.env` folder to populate the vector database.

Then, from the root folder of the repo, run:
```
python src/populate_vector_db.py
```

This script will populate multiple collections of vectors, with each collection corresponding to a different company across all earnings calls. This ensures the vector database has an index on company, which will speed up queries from the chatbot's query engine.

If you try to populate your cloud-hosted vector database on a Qdrant free tier account, you may experience rate limits. You will need to retry the script as necessary. This will not be an issue on the local DB instance, however, so you may even want to compare the collections to ensure each of their vector counts match their corresponding local connection.

## Run the Application

Ensure you have in `QDRANT_API_KEY` and `QDRANT_URL` in your `.streamlit/.secrets.toml` file to initialize the vector database.

To start the application locally, run:
```
streamlit run src/app.py
```

This will use Streamlit to render a UI for the chatbot application. You now have all the pieces you need to try the app and even contribute new features!

## Deploying the Application

If you choose to fork this repo into your Github account, you can deploy a replica application.

Make sure to create an account on [StreamLit](https://share.streamlit.io/). Follow the instructions to sign up / sign in, and then deploy this application using Python `3.9`. Remember to also include the secret variables from `.streamlit/.secrets.toml`.

Streamlit will then host the app and provide you with a URL to share.

**App Requirements**:

1. A user can ask a question for the ingested `.txt` files, the system retrieves the relevant chunks/documents and answers the user question.
2. The app keeps track of the chat history with a given user and takes it into account when answering questions.
3. The app is only expected to answer questions using information from uploaded documents & the user chat history.
4. The app should be stateful in terms of uploaded documents & chat history.
5. The app should be hosted & accessible via a URL

**Deliverables**

1. The URL of the hosted app
2. Provide instructions on how to run access/use the app
3. Provide systems diagram of all components of your app, and a small writeup explaining it