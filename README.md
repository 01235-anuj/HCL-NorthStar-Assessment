# HCL NorthStar Assessment

An AI-powered Sales & Policy Question Answering Agent built for the NorthStar Retail assessment.

## Overview

This project implements a local question-answering agent that combines structured sales data with NorthStar Retail policy and product reference documents.

The agent is designed to provide accurate answers to both **business analytics** and **policy-related** questions, along with the relevant source document for policy-based responses.

## Key Capabilities

### Sales Analytics

- Calculate total revenue
- Identify the highest-revenue region
- Identify top-performing products
- Generate revenue by region
- Generate revenue by product category
- Query revenue for specific products

### Policy & Product Information

- Customer support channels and response policies
- Shipping and delivery timelines
- Return and refund policies
- Loyalty program rules
- Warranty coverage and duration
- Product sizing information
- Seasonal promotion rules
- Stationery and bulk-order information

## How It Works

```text
                    ┌──────────────────────┐
                    │     User Question    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Question Processing │
                    │  & Intent Detection  │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌───────────────────┐       ┌────────────────────┐
       │  Sales Analytics  │       │ Policy / FAQ Query │
       │      Query        │       │                    │
       └─────────┬─────────┘       └──────────┬─────────┘
                 │                            │
                 ▼                            ▼
       ┌───────────────────┐       ┌────────────────────┐
       │ sales_clean.csv   │       │ Policy / Reference │
       │                   │       │ Documents           │
       └─────────┬─────────┘       └──────────┬─────────┘
                 │                            │
                 └─────────────┬──────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Answer Generation    │
                    │ + Source Attribution │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Final Answer       │
                    │   + Source           │
                    └──────────────────────┘

---

## Project Structure

```text
HCL-NorthStar-Assessment/
│
├── data/
│   ├── sales_clean.csv
│   └── policy/reference documents
│
├── src/
│   └── agent_local.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
