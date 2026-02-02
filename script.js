// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State Management
let currentMood = null;

// DOM Elements
const reviewInput = document.getElementById('reviewInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const sentimentResults = document.getElementById('sentimentResults');
const sentimentEmoji = document.getElementById('sentimentEmoji');
const sentimentLabel = document.getElementById('sentimentLabel');
const confidenceFill = document.getElementById('confidenceFill');
const confidenceValue = document.getElementById('confidenceValue');
const scorePositive = document.getElementById('scorePositive');
const scoreNeutral = document.getElementById('scoreNeutral');
const scoreNegative = document.getElementById('scoreNegative');
const moodCards = document.querySelectorAll('.mood-card');
const recommendationsSection = document.getElementById('recommendationsSection');
const recommendationsSubtitle = document.getElementById('recommendationsSubtitle');
const moviesGrid = document.getElementById('moviesGrid');
const loadingOverlay = document.getElementById('loadingOverlay');

/* ============================================
   SENTIMENT ANALYSIS
   ============================================ */

// Analyze sentiment when button is clicked
analyzeBtn.addEventListener('click', async () => {
    const text = reviewInput.value.trim();

    if (!text) {
        showNotification('Please enter a movie review to analyze', 'warning');
        return;
    }

    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/analyze_sentiment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (data.error) {
            showNotification(data.error, 'error');
            hideLoading();
            return;
        }

        displaySentimentResults(data);
        hideLoading();

        // Scroll to results
        sentimentResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    } catch (error) {
        console.error('Error analyzing sentiment:', error);
        showNotification('Failed to analyze sentiment. Make sure the server is running!', 'error');
        hideLoading();
    }
});

// Display sentiment analysis results
function displaySentimentResults(data) {
    // Show results section
    sentimentResults.classList.remove('hidden');

    // Update emoji and label
    sentimentEmoji.textContent = data.emoji;
    sentimentLabel.textContent = data.sentiment.charAt(0).toUpperCase() + data.sentiment.slice(1);

    // Update confidence bar
    confidenceFill.style.width = `${data.confidence}%`;
    confidenceValue.textContent = `${data.confidence}%`;

    // Update sentiment scores
    scorePositive.textContent = `${Math.round(data.scores.positive * 100)}%`;
    scoreNeutral.textContent = `${Math.round(data.scores.neutral * 100)}%`;
    scoreNegative.textContent = `${Math.round(data.scores.negative * 100)}%`;

    // Apply color based on sentiment
    const sentimentColors = {
        'positive': 'var(--gradient-success)',
        'negative': 'var(--gradient-secondary)',
        'neutral': 'var(--gradient-accent)'
    };

    confidenceFill.style.background = sentimentColors[data.sentiment] || 'var(--gradient-success)';
}

/* ============================================
   MOOD SELECTION & RECOMMENDATIONS
   ============================================ */

// Handle mood card clicks
moodCards.forEach(card => {
    card.addEventListener('click', async () => {
        const mood = card.dataset.mood;

        // Update active state
        moodCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');

        currentMood = mood;

        // Get recommendations
        await getRecommendations(mood);
    });
});

// Fetch recommendations based on mood
async function getRecommendations(mood) {
    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/get_recommendations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mood: mood,
                limit: 6
            })
        });

        const data = await response.json();

        if (data.error) {
            showNotification(data.error, 'error');
            hideLoading();
            return;
        }

        displayRecommendations(data);
        hideLoading();

    } catch (error) {
        console.error('Error fetching recommendations:', error);
        showNotification('Failed to fetch recommendations. Make sure the server is running!', 'error');
        hideLoading();
    }
}

// Display movie recommendations
function displayRecommendations(data) {
    // Show recommendations section
    recommendationsSection.classList.remove('hidden');

    // Update subtitle
    const moodEmojis = {
        'happy': '😊',
        'sad': '😢',
        'excited': '🤩',
        'relaxed': '😌',
        'scared': '😱',
        'inspired': '💪'
    };

    recommendationsSubtitle.textContent = `${moodEmojis[data.mood]} ${data.description}`;

    // Clear previous movies
    moviesGrid.innerHTML = '';

    // Add movie cards
    data.recommendations.forEach(movie => {
        const movieCard = createMovieCard(movie);
        moviesGrid.appendChild(movieCard);
    });

    // Scroll to recommendations
    setTimeout(() => {
        recommendationsSection.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

// Create a movie card element
function createMovieCard(movie) {
    const card = document.createElement('div');
    card.className = 'movie-card';

    // Create genres HTML
    const genresHTML = movie.genres
        .map(genre => `<span class="genre-tag">${genre}</span>`)
        .join('');

    card.innerHTML = `
        <img src="${movie.poster}" alt="${movie.title}" class="movie-poster" 
             onerror="this.src='https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=300&h=450&fit=crop'">
        <div class="movie-info">
            <h3 class="movie-title" title="${movie.title}">${movie.title}</h3>
            <div class="movie-meta">
                <span class="movie-year">${movie.year}</span>
                <span class="movie-rating">${movie.rating}</span>
            </div>
            <div class="movie-genres">
                ${genresHTML}
            </div>
            <p class="movie-description">${movie.description}</p>
        </div>
    `;

    // Add click animation
    card.addEventListener('click', () => {
        card.style.transform = 'scale(0.98)';
        setTimeout(() => {
            card.style.transform = '';
        }, 150);
    });

    return card;
}

/* ============================================
   UTILITY FUNCTIONS
   ============================================ */

// Show loading overlay
function showLoading() {
    loadingOverlay.classList.remove('hidden');
}

// Hide loading overlay
function hideLoading() {
    loadingOverlay.classList.add('hidden');
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'error' ? 'var(--gradient-secondary)' : 'var(--gradient-primary)'};
        color: white;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-lg);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Remove after 4 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 4000);
}

// Add slide out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
`;
document.head.appendChild(style);

// Allow Enter key to submit in textarea (with Ctrl/Cmd)
reviewInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        analyzeBtn.click();
    }
});

/* ============================================
   INITIALIZATION
   ============================================ */

// Check server health on load
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        if (data.status === 'healthy') {
            console.log('✅ Server is healthy');
            console.log(`📊 Loaded ${data.movie_count} movies`);
            console.log(`🎭 Available moods: ${data.available_moods.join(', ')}`);
        }
    } catch (error) {
        console.warn('⚠️ Server is not running. Please start the Flask server with: python app.py');
        showNotification('Server is offline. Start it with: python app.py', 'error');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkServerHealth();
    console.log('🎬 CineScope initialized!');
});
