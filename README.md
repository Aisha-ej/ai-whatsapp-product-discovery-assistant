# AI-Powered WhatsApp Product Discovery Assistant

## Overview

An AI-powered conversational shopping assistant that enables users to discover products using natural language queries through WhatsApp and a Streamlit web interface.

The system combines Retrieval-Augmented Generation (RAG), semantic vector search, structured filtering, and Gemini LLM-powered recommendations to provide intelligent product discovery experiences.

## Features

* Natural language product search
* WhatsApp integration using Twilio
* Retrieval-Augmented Generation (RAG)
* Semantic search using vector embeddings
* Structured product filtering
* AI-generated product recommendations
* Product image delivery via WhatsApp
* Search analytics and click tracking
* Streamlit dashboard

## Tech Stack

* Python
* FastAPI
* Streamlit
* Gemini API
* ChromaDB
* Twilio WhatsApp API
* PostgreSQL
* Pandas

## Architecture

User Query → WhatsApp/Streamlit → FastAPI → Product Retrieval → ChromaDB Semantic Search → Gemini Recommendation Engine → Product Recommendation Response

## Example Queries

* Show me black handbags
* Leather wallet under 1000
* Red bag
* Black leather handbags under 2000

## Key AI Concepts

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Embeddings
* Conversational AI
* Prompt Engineering

## Future Improvements

* Conversation memory
* Multi-product comparison
* Personalized recommendations
* WhatsApp Business Catalog Integration
