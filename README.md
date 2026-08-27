# HCL NorthStar Assessment

AI-powered Sales & Policy Question Answering Agent for NorthStar Retail.

## Overview

This project implements a local AI-style question-answering agent for NorthStar Retail.

The agent can answer questions using:

- Sales data from the provided CSV dataset
- NorthStar Retail policy documents
- Product and category information
- Customer support information
- Shipping and delivery policies
- Returns and refunds policies
- Loyalty program rules
- Warranty information
- Product sizing information
- Promotions and stationery FAQs

The agent also provides the source document used for policy-based answers.

---

## Workflow

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
