# 🤖 GoAified – HR & IT Helpdesk AI Agent

An intelligent, AI-powered HR and IT Helpdesk Assistant designed to answer employee queries using company policies and internal documentation.

GoAified helps employees quickly find accurate information about leave management, work-from-home policies, employee guidelines, and IT security procedures through a conversational interface.

The system uses Large Language Models (LLMs) and a document-based knowledge source to provide relevant, context-aware responses.

---

## 🚀 Project Overview

Employees frequently need information about company policies, HR procedures, and IT support guidelines. Finding this information manually across multiple documents can be time-consuming.

**GoAified** aims to simplify this process by providing a centralized AI-powered helpdesk agent that allows employees to ask questions in natural language and receive relevant answers based on organizational documentation.

### Key Objectives

- Automate responses to common HR and IT queries.
- Provide quick access to company policies.
- Retrieve relevant information from multiple documents.
- Reduce repetitive HR and IT support requests.
- Deliver consistent and context-aware responses.

---

## ✨ Key Features

- **AI-Powered Conversations:** Interact with the helpdesk using natural language.
- **HR Policy Assistance:** Answer questions about annual leave, casual leave, sick leave, and leave approval procedures.
- **Remote Work Assistance:** Provide information about work-from-home eligibility, approvals, and expectations.
- **Employee Handbook Support:** Answer questions about working hours, attendance, onboarding, and HR procedures.
- **IT Security Assistance:** Explain password requirements, device security, phishing prevention, and incident reporting.
- **Document-Based Knowledge:** Use internal policy documents as the source of information.
- **LLM Integration:** Leverage Groq-powered LLM inference for generating responses.
- **Centralized Configuration:** Manage application settings and API credentials using environment variables.

---

## 🧠 Knowledge Base

The agent uses fictional company policies maintained as separate text documents.

| Document | Description |
|---|---|
| `leave_policy.txt` | Annual, casual, and sick leave policies and approval procedures. |
| `work_from_home_policy.txt` | Remote work eligibility, approval, and expectations. |
| `employee_handbook.txt` | Working hours, attendance, onboarding, and HR procedures. |
| `it_security_policy.txt` | Password management, device security, phishing, and incident reporting. |

**Source of Truth:** These documents serve as the authoritative knowledge base for the demonstration organization, GoAified Demo Organization.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Groq API | LLM inference |
| Llama 3.3 70B Versatile | Language model |
| Pydantic Settings | Application configuration |
| python-dotenv | Environment variable support |
| TXT Documents | Policy knowledge base |

---

## 📁 Project Structure

```text
GoAified-HR-IT-Helpdesk/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── agents/
│   │   └── helpdesk_agent.py
│   │
│   ├── knowledge_base/
│   │   ├── leave_policy.txt
│   │   ├── work_from_home_policy.txt
│   │   ├── employee_handbook.txt
│   │   └── it_security_policy.txt
│   │
│   └── services/
│       └── ...
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: Adjust the directory structure to match your actual implementation.*

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd GoAified-HR-IT-Helpdesk
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
APP_NAME="GoAified HR IT Helpdesk"
APP_ENV=development
DEBUG=True

DATABASE_URL=your_database_url

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

Get your Groq API key from:

https://console.groq.com/keys

**Important:** Never commit your `.env` file or expose API credentials in your repository.

### 5. Run the Application

```bash
python app/main.py
```

Update the command according to your application entry point.

---

## 💬 Example Queries

Employees can interact with the helpdesk using questions such as:

**HR & Leave Management**
- How many annual leave days are available?
- How many sick leave days can employees take?
- How do I apply for leave?
- How can I check my remaining leave balance?

**Work From Home**
- Who is eligible for remote work?
- How can I request work from home?
- What are the expectations when working remotely?

**Employee Handbook**
- What are the standard working hours?
- How should I report an absence?
- What happens during employee onboarding?
- Whom should I contact for HR-related queries?

**IT Security**
- What are the password requirements?
- How should I report a phishing email?
- What should I do if my company laptop is stolen?
- How do I report a security incident?

---

## 🔐 Security Considerations

- Store API keys and credentials in environment variables.
- Exclude `.env` files from version control.
- Avoid exposing sensitive employee information in LLM prompts or logs.
- Use approved and secure channels for handling internal documents.
- Validate user inputs and handle API errors appropriately.

---

## 🔮 Future Enhancements

- Implement Retrieval-Augmented Generation (RAG) for intelligent document retrieval.
- Integrate vector databases for semantic search.
- Add conversation memory for contextual interactions.
- Implement an agentic workflow for handling complex employee requests.
- Integrate HR databases for employee-specific information.
- Develop a FastAPI-based backend.
- Build a web-based chat interface.
- Implement role-based access control and authentication.
- Add source citations to responses for improved transparency.

---

## 🎯 Project Goal

To build an intelligent, reliable, and scalable AI-powered employee support system that bridges the gap between employees and organizational knowledge.

**GoAified – Making Employee Support Smarter with AI.**

---

## ⚠️ Disclaimer

GoAified Demo Organization and its policies are fictional and created exclusively for demonstration, development, and testing purposes. They do not represent the actual internal policies of any organization.

---

## 👨‍💻 Author

Developed as an AI-powered HR and IT Helpdesk Agent project.

**Technologies:** Python | Generative AI | LLMs | Groq | Document-Based Retrieval

