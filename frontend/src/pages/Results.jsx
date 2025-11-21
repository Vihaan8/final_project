import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import '../styles/Results.css'

const Results = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('twins')
  const [activeTwinIndex, setActiveTwinIndex] = useState(0)
  
  const { data } = location.state || {}
  
  if (!data) {
    navigate('/')
    return null
  }

  const twins = data.taste_twins || []
  const recommendations = data.recommendations || []
  const activeTwin = twins[activeTwinIndex]

  return (
    <div className="results-container">
      <div className="results-header">
        <div>
          <h1>Your Restaurant Twin Results</h1>
          <p>Discover restaurants perfectly matched to your taste</p>
        </div>
        <button className="retake-btn" onClick={() => navigate('/')}>
          Retake Quiz
        </button>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'twins' ? 'active' : ''}`}
          onClick={() => setActiveTab('twins')}
        >
          Your Twins
        </button>
        <button 
          className={`tab ${activeTab === 'friends' ? 'active' : ''}`}
          onClick={() => setActiveTab('friends')}
        >
          Friends
        </button>
      </div>

      {activeTab === 'twins' && (
        <>
          <div className="twins-selector">
            {twins.map((twin, index) => (
              <div
                key={twin.user_id}
                className={`twin-selector-card ${activeTwinIndex === index ? 'active' : ''}`}
                onClick={() => setActiveTwinIndex(index)}
              >
                <div className="twin-selector-avatar">
                  {twin.name.charAt(0)}
                </div>
                <div className="twin-selector-info">
                  <h4>{twin.name}</h4>
                  <span className="mini-badge">{Math.round(twin.score)}% Match</span>
                </div>
              </div>
            ))}
          </div>

          <div className="twin-profile">
            <div className="twin-avatar">
              <div className="avatar-circle">
                {activeTwin.name.charAt(0)}
              </div>
              <span className="match-badge">{Math.round(activeTwin.score)}% Match</span>
            </div>
            <div className="twin-info">
              <h2>Meet Your Twin: {activeTwin.name}</h2>
              <p>📍 Santa Barbara, CA • {activeTwin.review_count} Yelp reviews</p>
            </div>
          </div>

          <div className="twin-loves">
            <h3>👍 What {activeTwin.name} Loves</h3>
            <p className="match-summary">
              You both care about: <strong>{activeTwin.matching_priorities.join(', ')}</strong> • 
              Love <strong>{activeTwin.matching_styles.join(', ')}</strong> dining • 
              Enjoy <strong>{activeTwin.matching_cuisines.join(', ')}</strong> cuisine
            </p>
          </div>

          {activeTwin.reviews && activeTwin.reviews.length > 0 && (
            <div className="twin-reviews-section">
              <h3>Recent Reviews by {activeTwin.name}</h3>
              <div className="twin-reviews-grid">
                {activeTwin.reviews.map((review, idx) => (
                  <div key={idx} className="twin-review-card">
                    <div className="review-header">
                      <h4>{review.business_name}</h4>
                      <div className="review-stars">
                        {'⭐'.repeat(Math.round(review.stars))}
                      </div>
                    </div>
                    <p className="review-text">"{review.text.substring(0, 200)}..."</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="recommendations-section">
            <div className="section-header">
              <h2>Restaurants We Think You'll Love</h2>
              <p>Based on your quiz answers and your twins' preferences</p>
            </div>

            <div className="restaurants-grid">
              {recommendations.slice(0, 6).map((restaurant) => (
                <div key={restaurant.business_id} className="restaurant-card">
                  <div className="restaurant-image">
                    <img 
                      src={`https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&q=80`}
                      alt={restaurant.name}
                    />
                    <div className="price-badge">$$$</div>
                  </div>
                  
                  <div className="restaurant-info">
                    <h3>{restaurant.name}</h3>
                    <p className="location">📍 {restaurant.address}</p>
                    
                    <div className="ratings">
                      <div className="rating-item">
                        <span className="stars">⭐ {restaurant.overall_stars.toFixed(1)}</span>
                        <span className="label">Overall</span>
                      </div>
                      <div className="rating-item highlight">
                        <span className="stars">⭐ {restaurant.twin_avg_rating.toFixed(1)}</span>
                        <span className="label">Your twins rated it</span>
                      </div>
                    </div>

                    <div className="endorsement">
                      <strong>Endorsed by:</strong> {restaurant.endorsing_twin_names.join(', ')}
                    </div>

                    {restaurant.sample_reviews && restaurant.sample_reviews[0] && (
                      <div className="review-snippet">
                        "{restaurant.sample_reviews[0].substring(0, 120)}..."
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {activeTab === 'friends' && (
        <div className="friends-section">
          <div className="live-feed">
            <h2>👥 Community Feed</h2>
            <p>Connect with other users who found their taste twins!</p>
            
            <div className="community-message">
              <div className="community-icon">🎉</div>
              <h3>Live Feed Coming Soon!</h3>
              <p>We're building a community feature where you can:</p>
              <ul>
                <li>See who else just found their taste twins</li>
                <li>Share your favorite restaurant discoveries</li>
                <li>Connect with people with similar tastes</li>
                <li>Get updates on new restaurants your twins love</li>
              </ul>
              <p className="community-note">For now, explore your personalized recommendations above!</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Results
