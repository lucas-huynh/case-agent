![Python](https://img.shields.io/badge/python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-app-red)
![License](https://img.shields.io/badge/license-MIT-green)

# Hospital Surge Staffing Simulator

An interactive AI-powered stakeholder simulation designed to teach **operations research problem formulation in healthcare operations**.

Students interview simulated hospital stakeholders, gather operational evidence, and construct a formal decision problem.

The system uses **LLM personas + semantic retrieval (RAG)** grounded in real research papers to produce realistic stakeholder responses.

---

## Overview

Emergency departments must make staffing decisions under uncertainty.

This simulator places students in the role of an analyst tasked with understanding how nurse staffing decisions are made during demand surges.

Students interact with multiple stakeholders, including:

- Chief Financial Officer
- Emergency Department Physician Leader
- Emergency Department Operations Manager

Through conversation, students extract key operational insights and build a formal operations research problem.

---

## Learning Objectives

Students learn how to:

- Identify **decision variables**
- Distinguish **objectives vs constraints**
- Recognize **uncertainty in operational systems**
- Extract evidence from stakeholder interviews
- Formulate **operations research decision problems**

The simulator emphasizes **problem formulation**, which is often the hardest part of operations research.

---

## Features

### Stakeholder Simulation

Interactive AI personas represent hospital stakeholders with different priorities.

Examples:

- CFO → cost control
- Physician → patient safety and wait times
- Operations Manager → staffing feasibility

---

### Evidence-Based Responses

The system uses **semantic retrieval (RAG)** over curated research sources including:

- Hu et al. Prediction-Driven Surge Planning
- Hu et al. Real-Time ED Arrival Prediction
- Hu et al. Implementation of ED Staffing Frameworks
- American Hospital Association Surge Guidance
- American Nurses Association Staffing Recommendations

Stakeholder responses include **citations to these sources**.

---

### Problem Formulation Canvas

Students organize insights into structured categories:

- Decisions
- Objectives
- Constraints
- Uncertainties
- State Variables
- Operational Insights
- Trade-offs
- Evidence

---

### Automated Formulation Builder

Students can generate a structured **operations research formulation**, including:

- decision variables
- objective function
- constraints
- uncertainty sources

---

### Instructor Evaluation

The simulator evaluates student formulations using a rubric defined in the case configuration.

---

## System Architecture

Student Question  
↓  
Persona Router  
↓  
Semantic Retrieval (RAG)  
↓  
Persona Engine  
↓  
Evidence-grounded response  
↓  
Problem Formulation Canvas  
↓  
Formulation Builder + Evaluation  

---

## Project Structure

case-agent  
│  
├ backend  
│   ├ engine  
│   │   └ persona_engine.py  
│   ├ retrieval  
│   │   └ semantic_retriever.py  
│   ├ case_loader.py  
│   ├ llm_adapter.py  
│   └ config.py  
│  
├ frontend  
│   └ app.py  
│  
├ cases  
│   └ hospital_surge_v1  
│       ├ case.yaml  
│       ├ chunks.yaml  
│       └ personas  
│  
├ requirements.txt  
└ README.md  

---

## Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/case-agent.git  
cd case-agent  

Install Python dependencies:

pip install -r requirements.txt  

---

## Local LLM Setup (Ollama)

This project uses **Ollama to run a local LLaMA model** for stakeholder responses.

### Install Ollama

Download Ollama from:

https://ollama.com/download

Verify installation:

ollama --version

### Download the LLM

ollama pull llama3.1

### Start the Ollama server

ollama serve

The simulator will automatically connect to:

http://localhost:11434

No API keys are required.

---

## Running the Simulator

Start the Streamlit app:

streamlit run frontend/app.py

Then open the app in your browser:

http://localhost:8501

---

## Example Student Workflow

1. Ask stakeholders about the staffing system
2. Extract operational insights
3. Organize findings in the formulation canvas
4. Generate a decision problem formulation
5. Receive instructor feedback

---

## Example Research Sources

The simulator includes insights derived from:

- Hu et al. (2021) Prediction-Driven Surge Planning
- Hu et al. (2023) Real-Time ED Arrival Prediction
- Hu et al. (2025) Implementation of Staffing Framework
- American Hospital Association Surge Guidance
- American Nurses Association Staffing Recommendations

---

## Technologies Used

- Python
- Streamlit
- Sentence Transformers
- FAISS vector search
- Local LLM inference via Ollama
- YAML-based case design

---

## Future Improvements

Possible extensions include:

- multi-session classroom deployment
- instructor dashboards
- automated grading analytics
- additional healthcare operations cases
- more advanced retrieval and reasoning

---

## License

MIT License

---

## Author

Lucas Huynh  
Carnegie Mellon University  
Heinz College – Data Analytics & Information Technology
