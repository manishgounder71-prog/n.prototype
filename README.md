# 🎬 CineScope - Movie Sentiment Analysis & Recommendation System

An AI-powered web application that analyzes movie review sentiment and recommends films based on your current mood.

![CineScope](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)

## ✨ Features

- **🎭 Sentiment Analysis**: Analyze movie reviews using VADER NLP to detect positive, negative, or neutral sentiment with confidence scores
- **🎯 Mood-Based Recommendations**: Get personalized movie suggestions based on 6 different moods (Happy, Sad, Excited, Relaxed, Scared, Inspired)
- **🤖 AI Assistant**: Chat with an AI powered by OpenAI GPT-3.5 to get personalized movie recommendations through natural conversation
- **💎 Modern UI**: Beautiful glassmorphism design with dark theme, gradients, and smooth animations
- **📊 30-Movie Database**: Curated collection across multiple genres with ratings and descriptions
- **⚡ Real-time Analysis**: Instant sentiment feedback and dynamic recommendations

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd d:\n.prototype
pip install -r requirements.txt
```

### 2. Configure OpenAI API Key (Optional but Recommended)

To enable the AI Assistant feature, add your OpenAI API key to the `.env` file:

```bash
# Edit .env file
OPENAI_API_KEY=your_actual_openai_key_here
```

> **Note**: You can use the system without the API key, but the AI Assistant feature won't work.

### 3. Run the Server

```bash
python app.py
```

Or with full Python path:
```bash
C:\Users\manis\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe app.py
```

### 3. Open in Browser

Navigate to: **http://localhost:5000**

## 📖 How to Use

### Analyze Movie Reviews

1. Type or paste a movie review in the text area
2. Click "Analyze Sentiment"
3. View the sentiment results with confidence scores

**Example Review**:
> "This movie was absolutely incredible! The cinematography was stunning and the acting was phenomenal."

**Result**: Positive sentiment with 89% confidence

### Get Movie Recommendations

1. Select your current mood from the 6 mood cards
2. View personalized movie recommendations
3. Each recommendation includes title, rating, genres, and description

**Available Moods**:
- 😊 **Happy** - Feel-good movies (Comedy, Romance, Musical)
- 😢 **Sad** - Emotional stories (Drama, Romance)
- 🤩 **Excited** - High-energy action (Action, Thriller, Sci-Fi)
- 😌 **Relaxed** - Calming content (Documentary, Animation)
- 😱 **Scared** - Thrilling suspense (Horror, Mystery)
- 💪 **Inspired** - Motivational tales (Biography, Sports)

### Ask AI Assistant

1. Scroll to the "Ask AI Assistant" section
2. Click a quick prompt button or type your own question
3. Get personalized movie recommendations through AI conversation
4. Examples: "What should I watch tonight?", "Recommend a thriller movie"

## 🏗️ Technical Stack

**Backend**:
- Flask 3.0.0 - Web framework
- NLTK with VADER - Sentiment analysis
- TextBlob - Additional sentiment metrics

**Frontend**:
- HTML5, CSS3, JavaScript (ES6+)
- Vanilla JS with Fetch API
- Modern glassmorphism design
- Responsive grid layouts

## 📁 Project Structure

```
d:/n.prototype/
├── app.py                    # Flask server & API endpoints
├── sentiment_analyzer.py     # VADER sentiment analysis
├── recommendation_engine.py  # Mood-based recommendation logic
├── movie_database.py         # Database management
├── movies.json              # Movie dataset (30 films)
├── requirements.txt         # Python dependencies
├── index.html              # Main HTML page
├── style.css               # Complete styling system
└── script.js               # Frontend interactivity
```

## 🔌 API Endpoints

- `POST /api/analyze_sentiment` - Analyze review sentiment
- `POST /api/get_recommendations` - Get mood-based recommendations
- `GET /api/movies` - List all movies
- `GET /api/moods` - Get available moods
- `GET /api/health` - Server health check

## 🎨 Design Features

- **Glassmorphism Effects**: Semi-transparent cards with backdrop blur
- **Animated Background**: Floating gradient orbs
- **Smooth Animations**: Hover effects and transitions
- **Dark Theme**: Purple/blue gradient color scheme
- **Responsive Design**: Works on all device sizes

## 📊 Movie Database

The system includes 30 carefully selected movies:
- The Shawshank Redemption (9.3)
- The Dark Knight (9.0)
- Inception (8.8)
- Spirited Away (8.6)
- La La Land (8.0)
- And 25 more across all genres!

## 🔧 Requirements

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (first run only for NLTK data)

## 📝 Notes

- The Flask server runs in debug mode by default
- Sentiment analysis works best with complete sentences
- Recommendations are scored based on genre match and ratings
- The UI features require a modern browser with backdrop-filter support

## 🎯 What's Next

Explore the complete walkthrough for detailed information:
- See `walkthrough.md` for comprehensive documentation
- View `implementation_plan.md` for technical architecture
- Check `task.md` for development progress

## 🌟 Highlights

✅ Production-ready full-stack application  
✅ Accurate VADER sentiment analysis  
✅ Smart mood-based recommendations  
✅ Premium modern UI design  
✅ Comprehensive error handling  
✅ RESTful API architecture

---

**Built with ❤️ using Flask, VADER, and Modern Web Design**

Enjoy discovering your perfect movie match! 🎬
