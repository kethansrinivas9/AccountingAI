# AccountingAI

AccountingAI is a Generative AI platform using OpenAI and LangChain APIs to answer queries releated to Accounting/Bills/Balance sheets/Documents submitted to it. 

## Technologies Used

### Backend
- **LangChain**: Framework for developing applications powered by language models
- **OpenAI**: AI models for natural language processing and document understanding
- **FastAPI**: High-performance web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library
- **Neon DB**: Serverless PostgreSQL database for efficient data storage

### Frontend
- **React**: JavaScript library for building user interfaces
- **Next.js**: React framework for production-grade applications
- **TailwindCSS**: Utility-first CSS framework for rapid UI development

### DevOps & Infrastructure
- **AWS EC2**: Cloud computing service for hosting the application
- **AWS CloudFormation**: Infrastructure as code to provision AWS resources
- **AWS IAM**: Identity and access management for secure resource access
- **AWS KMS**: Key Management Service for encryption of sensitive data
- **AWS Systems Manager Parameter Store**: Secure storage for configuration data
- **NGINX**: Web server used as a reverse proxy
- **PM2**: Process manager for applications to create startup scripts for Systemd automatically

## Project Setup and Local Deployment

### Prerequisites
- Python
- OpenAI API key
- Neon DB account and database credentials

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/kethansrinivas9/AccountingAI.git
cd AccountingAI
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies after changing directory to backend**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Edit the `.env` file with your configuration details including:
- OpenAI API key
- Neon DB connection string
- update the value of NEXT_PUBLIC_API_BASE_URL to localhost:<your_front_end_port>


5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start the FastAPI server locally**
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. **Navigate to the frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run the development server**
```bash
npm run dev
```

## Cloud Deployment

### AWS Deployment

1. **Deploy infrastructure using CloudFormation**
```bash
aws cloudformation create-stack --stack-name accounting-ai --template-body file://deploy.yaml --capabilities CAPABILITY_NAMED_IAM
```

2. **Configure AWS Systems Manager Parameter Store**
Set up the following parameters (encrypted with KMS) which are being used in env_helper.py:
- `OPENAI_API_KEY`
- `DATABASE_URL`





## Usage

1. Access the application at `http://localhost:3000` (local development) or your deployed domain
2. Upload financial documents (supports UTF-8 encoded text files such as CSV, TXT, etc.)
3. Run queries to analyze and understand the submitted docs/bills/balance sheets
4. Generate reports and insights based on the processed information

## API Documentation

Once the server is running, access the API documentation at:
- Local: `http://localhost:8000/docs`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
