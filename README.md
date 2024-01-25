# Building a Multi-Document Question-Answering App

Your goal is to implement a multi-document QA application with a RAG pipeline for company earnings calls. Your app should have basic frontend capabilities, and it should be using Python as a backend.

More specifically, implement the following parts:

## Basic RAG Pipeline
Your goal for this section is to set up a basic Retrieval Augmented Generation (RAG) pipeline with LLamaindex (https://docs.llamaindex.ai/en/stable/) that you can use in the backend to fetch relevant document chunks. We recommend using Qdrant (https://qdrant.tech/) as the vector DB provider, but feel free to use something else. For the LLM, feel free to use the OpenAI API with one of our API keys. We also provide a file `example_user_questions.txt` which contains a non-exhaustive list of representative questions a user might ask.

A representative sample set of documents that a user might upload is provided via the `earnings_call_project.zip`. Your RAG pipeline only needs to support `.txt` files in the provided `earnings_calls.zip` file, and you can assume that the file names will always have semantic meaning, i.e., you can use the filenames to reason about the relevancy of a document given a question.

Your retrieval pipeline should operate over the entire space of documents and not just a single one, meaning part of building the pipeline is figuring out how to select relevant documents for a given question as well.

**Tasks**:

1. Sketch out a system design for the RAG pipeline with all relevant components & highlighting the interaction flows.
2. Implement the RAG pipeline as proposed with the provided documents in `earnings_call_project.zip`
3. Test your final pipeline with the example questions we provide in `example_user_questions.txt`. How does it perform?

Bonus: Can you think of any improvements you can make to your pipeline to improve the results?

## Building the App
For this section, build the actual multi-doc QA application. You can use frameworks of your choice, but your backend needs to be built in Python.

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