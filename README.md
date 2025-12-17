# 🗞️ News Classification API

An AI-powered FastAPI application that automatically categorizes news articles using Google's Gemini AI model. The system intelligently classifies scientific and technological news into predefined categories with multi-label support.

## 🌟 Features

- **AI-Powered Classification**: Automatic categorization using Google Gemini 2.5 Flash
- **Multi-Label Support**: Articles can belong to multiple categories (max 3)
- **Fallback System**: Keyword-based classification if AI fails
- **RESTful API**: Complete CRUD operations for news management
- **PostgreSQL Database**: Persistent storage with SQLAlchemy ORM
- **CORS Enabled**: Ready for frontend integration

## 📋 Categories

The system classifies news into these categories:

- **AI** - Artificial Intelligence, Machine Learning, Neural Networks
- **Robotics** - Robots, Automation, Autonomous Systems
- **Space** - Astronomy, Space Exploration, Satellites
- **Aeronautics** - Aircraft, Aviation, Flight Technology
- **Physics** - Quantum Mechanics, Particle Physics
- **Engineering** - Civil, Mechanical, Electrical Systems
- **Biology** - Genetics, Ecology, Evolution
- **Medical Science** - Healthcare, Treatments, Pharmaceuticals
- **Environment** - Climate, Conservation, Sustainability
- **Other** - Miscellaneous topics

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Google Gemini API key

### Installation

1. **Clone the repository**
```bash
git clone <https://github.com/Asifmahmud436/news_analyzer>
cd news_analyzer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv google-generativeai typing-extensions
```

4. **Set up environment variables**

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/news_db
GEMINI_API_KEY=your_gemini_api_key_here
```

5. **Run the application**
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## 📚 API Documentation

### Interactive Docs
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Endpoints

#### Create News Article
```bash
POST /news
```

**Request Body:**
```json
{
  "headline": "SpaceX Successfully Lands Starship",
  "body": "The massive rocket completed its flight test and touched down vertically on the pad."
}
```

**Response:**
```json
{
  "id": 1,
  "headline": "SpaceX Successfully Lands Starship",
  "body": "The massive rocket completed its flight test...",
  "categories": ["Space", "Engineering"],
  "created_at": "2025-12-18T01:00:00",
  "updated_at": "2025-12-18T01:00:00"
}
```

#### Get All News
```bash
GET /news
```

#### Get Specific News
```bash
GET /news/{news_id}
```

#### Update News
```bash
PUT /news/{news_id}
```

**Request Body:**
```json
{
  "headline": "Updated Headline",
  "body": "Updated content"
}
```

#### Delete News
```bash
DELETE /news?id={news_id}
```

## 🧪 Testing

### Example cURL Commands

**Create a medical news article:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/news' \
  -H 'Content-Type: application/json' \
  -d '{
  "headline": "Breakthrough in Cancer Treatment",
  "body": "Scientists discover a new immunotherapy drug that targets cancer cells with 90% success rate."
}'
```

**Create an AI + Medical Science article:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/news' \
  -H 'Content-Type: application/json' \
  -d '{
  "headline": "AI Revolutionizes Medical Diagnosis",
  "body": "A new artificial intelligence system can detect diseases from X-rays faster than human doctors."
}'
```

**Get all news:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/news'
```

## 🏗️ Project Structure

```
news-classification-api/
├── main.py           # FastAPI application & routes
├── ai.py             # Gemini AI classification logic
├── models.py         # SQLAlchemy database models
├── schema.py         # Pydantic schemas
├── database.py       # Database configuration
├── .env              # Environment variables (not in git)
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## 🔧 Configuration

### Database Setup

1. Create PostgreSQL database:
```sql
CREATE DATABASE news_db;
```

2. Update `DATABASE_URL` in `.env` file

### Gemini API Setup

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env` file as `GEMINI_API_KEY`

### CORS Configuration

Update `origins` list in `main.py` to include your frontend URLs:

```python
origins = [
    "http://localhost:3000",    # React
    "http://localhost:5173",    # Vite
    "https://your-app.vercel.app"
]
```

## 🤖 AI Classification Details

### How It Works

1. **Primary Method**: Gemini AI analyzes article text with detailed prompt engineering
2. **Fallback Method**: If AI fails, keyword-based classification kicks in
3. **Post-Processing**: Removes redundant "Other" category if specific categories exist

### Classification Logic

- Combines headline + body for better context
- Maximum 3 categories per article
- Prioritizes specific categories over "Other"
- Special handling for medical content

## 📊 Database Schema

```sql
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    headline TEXT NOT NULL,
    body TEXT NOT NULL,
    categories JSON,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## 🛠️ Requirements

```txt
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.23
psycopg2-binary>=2.9.9
python-dotenv>=1.0.0
google-generativeai>=0.3.1
typing-extensions>=4.8.0
```

## 🚨 Error Handling

The API includes comprehensive error handling:

- **AI Failures**: Automatic fallback to keyword-based classification
- **Database Errors**: Proper rollback and error messages
- **404 Errors**: Clear messages for missing resources
- **Validation**: Pydantic schema validation

## 🔐 Security Considerations

- API keys stored in environment variables
- CORS configured for specific origins
- SQL injection protected by SQLAlchemy ORM
- Input validation via Pydantic schemas

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Gemini AI for classification
- FastAPI for the web framework
- SQLAlchemy for database ORM

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Contact: safaandsafa4@example.com

---

**Built with ❤️ using FastAPI and Google Gemini AI**