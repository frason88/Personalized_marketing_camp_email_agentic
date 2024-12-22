# Personalized Marketing Campaigns with Multi-Agent Framework

## Overview

This project leverages a **multi-agent architecture powered by generative AI (Gen AI)** to automate the creation of personalized marketing campaigns. By connecting specialized AI agents, the system streamlines the entire marketing process—from data collection and analysis to content creation—ensuring optimized engagement and conversion rates. Utilizing customer data from a SQLite database, the system generates highly targeted, dynamic email campaigns tailored to individual preferences.

**Video walkthrough:** https://drive.google.com/file/d/1JfM00RJxKCPuntYc68-uLhBgRp6Kn9dg/view?usp=sharing

---

## Key Features

- **Multi-Agent Collaboration**: Specialized agents collaborate to retrieve, analyze, and process customer data efficiently.
- **Personalized Email Content**: Automatically generates dynamic, engaging email content tailored to specific customer segments.
- **Database Integration**: Utilizes a SQLite database to fetch customer data, ensuring campaigns are customized based on actual user behavior and preferences.
- **Data-Driven Insights**: Segments customers based on engagement metrics like total spending, loyalty program participation, and transaction frequency to drive campaign strategies.
- **Real-Time Adaptation**: Dynamically adjusts campaigns based on feedback, optimizing emails for conversions.
- **User-Friendly Interface**: Includes an interactive `panel`-based chat interface to trigger the AI pipeline and manage tasks seamlessly.

---

## Architecture

The system is composed of **five primary agents**, each responsible for a specific task in the pipeline:

1. **User Proxy Agent**:
   - Acts as the interface for human inputs and coordinates communication between agents.
   - Initiates tasks and manages the flow of information across the system.

2. **Data Retriever Agent**:
   - Fetches customer data from the SQLite database based on user IDs.
   - Retrieves attributes like `total_spent`, `transaction_frequency`, `loyalty_points_balance`, and more.

3. **Analyst Agent**:
   - Segments customer data into distinct groups based on spending habits, engagement rates, and communication preferences.
   - Provides actionable insights to optimize marketing strategies.

4. **Code Interpreter Agent**:
   - Handles data processing and code execution for advanced analysis, such as deriving additional insights from customer behavior.

5. **Email Agent**:
   - Generates complete, personalized email content tailored to each audience segment.
   - Incorporates placeholders like `[DISCOUNT]`, `[PRODUCT_NAME]`, and `[MSP]` to ensure dynamic content creation.

---

## Workflow

1. **Data Retrieval**:
   - The `Data Retriever Agent` queries the SQLite database (`customer_netcore.db`) for specific user data.

2. **Analysis**:
   - The `Analyst Agent` segments customers based on metrics such as spending habits, engagement rates, and loyalty program status.

3. **Content Generation**:
   - The `Email Agent` crafts personalized email content using insights from the analyst, dynamically tailoring each email for the target audience.

4. **Interaction and Feedback**:
   - Users interact with the system via an intuitive `panel`-based chat interface to input tasks, monitor progress, and trigger pipeline execution.

---

## Technologies Used

- **Python**: Backbone of the project, providing flexibility and compatibility with AI frameworks.
- **SQLite**: Lightweight relational database for storing and retrieving customer data.
- **`autogen`**: A custom agent orchestration framework managing agent communication and workflows.
- **Panel**: Provides an interactive, web-based interface for task management and interaction.

---

## Setup

### Prerequisites
- Python 3.10 or higher installed on your system.
- SQLite installed (or available as part of Python).

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd AI-Marketing-Agents
