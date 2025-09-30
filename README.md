# Mini ZSeries on Odroid
A lightweight simulation of IBM ZSeries mainframe principles using an ODROID XU4 single-board computer.

## Overview

This project aims to model core concepts of IBM zSeries mainframes in a simplified environment. By using an ODROID XU4 running Ubuntu, the project demonstrates how transaction processing, batch workloads, and AI fraud detection can be realized on low cost embedded hardware.

## Mini-zSeries Architecture

                  ┌───────────────────────────────┐
                  │           Users / API          │
                  │   (HTTP requests via Flask)    │
                  └───────────────┬───────────────┘
                                  │
                    ┌─────────────▼───────────────┐
                    │   Transaction Processing    │
                    │ - Deposit / Withdraw        │
                    │ - ACID properties           │
                    │ - Threading.Lock for safety │
                    └─────────────┬───────────────┘
                                  │
                 ┌────────────────┴───────────────────┐
                 │                                    │
     ┌───────────▼────────────┐           ┌───────────▼───────────────┐
     │ Batch Logging           │           │ Fraud Detection (AI)      │
     │ - Periodic jobs         │           │ - Collect transactions    │
     │ - Simulate nightly jobs │           │ - Run ML model (e.g.      │
     │                         │           │   scikit-learn Isolation) │
     └───────────┬─────────────┘           │ - Flag anomalies          │
                 │                         └───────────┬───────────────┘
                 │                                     │
        ┌────────▼─────────┐                   ┌───────▼───────────────┐
        │ System Logs      │                   │ Fraud Reports         │
        │ /tmp/batch_log   │                   │ /tmp/fraud_log        │
        └──────────────────┘                   └───────────────────────┘
