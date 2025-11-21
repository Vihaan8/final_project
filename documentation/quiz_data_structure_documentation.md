# DineLike Quiz & Data Structure Documentation

## Overview
This document outlines the questionnaire design, tag taxonomy, and JSON payload formats for the DineLike restaurant recommendation system.

---

## 1. User Questionnaire Design

### Quiz Structure
The quiz consists of 5 categories with multiple-choice questions. Users can select multiple options per category.

### Categories & Questions

#### Category 1: Cuisine Preferences
**Question:** "What types of cuisine do you enjoy? (Select all that apply)"

**Options:**
- Italian
- Mexican
- Chinese
- Japanese/Sushi
- Thai
- Vietnamese
- Indian
- American/Burgers
- Mediterranean
- Korean
- French
- BBQ/Steakhouse
- Seafood
- Pizza
- Breakfast/Brunch

#### Category 2: Dining Atmosphere
**Question:** "What kind of dining atmosphere do you prefer? (Select all that apply)"

**Options:**
- Casual & Relaxed
- Fine Dining / Upscale
- Trendy / Modern
- Cozy / Intimate
- Lively / Bustling
- Outdoor Seating
- Romantic
- Family-Friendly
- Quick Service
- Bar Scene

#### Category 3: Dietary Preferences & Restrictions
**Question:** "Do you have any dietary preferences or restrictions? (Select all that apply)"

**Options:**
- Vegetarian-Friendly
- Vegan Options
- Gluten-Free Options
- Halal
- Kosher
- Keto-Friendly
- Healthy Options
- Organic/Farm-to-Table
- No Restrictions

#### Category 4: Price Range
**Question:** "What's your typical price range per person?"

**Options:**
- $ (Under $15)
- $$ ($15-30)
- $$$ ($30-60)
- $$$$ (Over $60)

#### Category 5: Special Features
**Question:** "What features matter most to you? (Select all that apply)"

**Options:**
- Happy Hour Specials
- Weekend Brunch
- Late Night Dining
- Takeout/Delivery
- Pet-Friendly
- Live Music/Entertainment
- Wine Selection
- Craft Cocktails
- Craft Beer Selection
- Private Dining Available
- Parking Available
- Good for Groups

---

## 2. Tag Taxonomy

### Tag Structure
All tags are stored as lowercase strings with hyphens for multi-word tags.

### Master Tag List

#### Cuisine Tags
```
italian, mexican, chinese, japanese, sushi, thai, vietnamese, indian, 
american, burgers, mediterranean, korean, french, bbq, steakhouse, 
seafood, pizza, breakfast, brunch
```

#### Atmosphere Tags
```
casual, fine-dining, upscale, trendy, modern, cozy, intimate, 
lively, bustling, outdoor-seating, romantic, family-friendly, 
quick-service, bar-scene
```

#### Dietary Tags
```
vegetarian-friendly, vegan-options, gluten-free, halal, kosher, 
keto-friendly, healthy, organic, farm-to-table
```

#### Price Tags
```
budget, moderate, expensive, luxury
```

#### Feature Tags
```
happy-hour, brunch, late-night, takeout, delivery, pet-friendly, 
live-music, wine-selection, craft-cocktails, craft-beer, 
private-dining, parking, good-for-groups
```

---

## 3. JSON Payload Templates

### 3.1 Quiz Submission (Frontend → Backend)
```json
{
  "display_name": "Vihaan",
  "tags": {
    "cuisine": ["italian", "sushi", "mexican"],
    "atmosphere": ["casual", "trendy", "outdoor-seating"],
    "dietary": ["vegetarian-friendly", "healthy"],
    "price": ["moderate", "expensive"],
    "features": ["happy-hour", "brunch", "parking"]
  },
  "city": "Durham",
  "state": "NC"
}
```

### 3.2 Kafka Message Format (Backend → Kafka)
```json
{
  "display_name": "Vihaan",
  "quiz_tags": {
    "cuisine": ["italian", "sushi", "mexican"],
    "atmosphere": ["casual", "trendy", "outdoor-seating"],
    "dietary": ["vegetarian-friendly", "healthy"],
    "price": ["moderate", "expensive"],
    "features": ["happy-hour", "brunch", "parking"]
  },
  "city": "Durham",
  "state": "NC",
  "submitted_at": "2025-11-21T12:00:00.000Z"
}
```

### 3.3 Community Feed Response (Backend → Frontend)
```json
{
  "submissions": [
    {
      "submission_id": 1,
      "display_name": "Vihaan",
      "top_twin_name": "The Cheesecake Factory",
      "match_score": 85.5,
      "city": "Durham",
      "state": "NC",
      "created_at": "2025-11-21T12:00:00.000Z"
    },
    {
      "submission_id": 2,
      "display_name": "Sarah",
      "top_twin_name": "Olive Garden",
      "match_score": 78.3,
      "city": "Santa Barbara",
      "state": "CA",
      "created_at": "2025-11-21T11:55:00.000Z"
    }
  ]
}
```

### 3.4 Restaurant Data Structure (Database)
```json
{
  "restaurant_id": 123,
  "name": "The Cheesecake Factory",
  "address": "123 Main St",
  "city": "Durham",
  "state": "NC",
  "cuisine_type": "American",
  "price_range": "$$",
  "rating": 4.5,
  "tags": [
    "american", "casual", "family-friendly", "moderate", 
    "brunch", "parking", "good-for-groups"
  ]
}
```

---

## 4. Tag Mapping (User Selection → Database Tags)

### Cuisine Mapping
| User Selection | Database Tag |
|---------------|--------------|
| Italian | italian |
| Mexican | mexican |
| Chinese | chinese |
| Japanese/Sushi | japanese, sushi |
| Thai | thai |
| Vietnamese | vietnamese |
| Indian | indian |
| American/Burgers | american, burgers |
| Mediterranean | mediterranean |
| Korean | korean |
| French | french |
| BBQ/Steakhouse | bbq, steakhouse |
| Seafood | seafood |
| Pizza | pizza |
| Breakfast/Brunch | breakfast, brunch |

### Atmosphere Mapping
| User Selection | Database Tag |
|---------------|--------------|
| Casual & Relaxed | casual |
| Fine Dining / Upscale | fine-dining, upscale |
| Trendy / Modern | trendy, modern |
| Cozy / Intimate | cozy, intimate |
| Lively / Bustling | lively, bustling |
| Outdoor Seating | outdoor-seating |
| Romantic | romantic |
| Family-Friendly | family-friendly |
| Quick Service | quick-service |
| Bar Scene | bar-scene |

### Price Mapping
| User Selection | Database Tag |
|---------------|--------------|
| $ (Under $15) | budget |
| $$ ($15-30) | moderate |
| $$$ ($30-60) | expensive |
| $$$$ (Over $60) | luxury |

### Feature Mapping
| User Selection | Database Tag |
|---------------|--------------|
| Happy Hour Specials | happy-hour |
| Weekend Brunch | brunch |
| Late Night Dining | late-night |
| Takeout/Delivery | takeout, delivery |
| Pet-Friendly | pet-friendly |
| Live Music/Entertainment | live-music |
| Wine Selection | wine-selection |
| Craft Cocktails | craft-cocktails |
| Craft Beer Selection | craft-beer |
| Private Dining Available | private-dining |
| Parking Available | parking |
| Good for Groups | good-for-groups |

---

## 5. Matching Algorithm

### Tag Similarity Calculation
The system uses **Jaccard Similarity** to match users with restaurants:
```
Similarity Score = (Intersection of Tags / Union of Tags) × 100
```

### Example Calculation
**User Tags:** `[italian, casual, vegetarian-friendly, moderate]`
**Restaurant Tags:** `[italian, casual, family-friendly, moderate, parking]`
```
Intersection: [italian, casual, moderate] = 3 tags
Union: [italian, casual, vegetarian-friendly, moderate, family-friendly, parking] = 6 tags

Similarity = (3 / 6) × 100 = 50%
```

### Match Quality Thresholds
- **Excellent Match:** 70-100%
- **Good Match:** 50-69%
- **Fair Match:** 30-49%
- **Poor Match:** 0-29%

---

## 6. API Endpoints

### POST /api/quiz/submit
Submit quiz responses

**Request Body:**
```json
{
  "display_name": "string",
  "tags": {
    "cuisine": ["string"],
    "atmosphere": ["string"],
    "dietary": ["string"],
    "price": ["string"],
    "features": ["string"]
  },
  "city": "string",
  "state": "string"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Quiz submitted! Processing your taste twin match..."
}
```

### GET /api/community/feed?limit=20
Get recent quiz submissions

**Response:**
```json
[
  {
    "submission_id": 1,
    "display_name": "Vihaan",
    "top_twin_name": "The Cheesecake Factory",
    "match_score": 85.5,
    "city": "Durham",
    "state": "NC",
    "created_at": "2025-11-21T12:00:00.000Z"
  }
]
```

### GET /api/community/stats
Get community statistics

**Response:**
```json
{
  "total_submissions": 150,
  "today_submissions": 12,
  "average_match_score": 72.5
}
```

---

## 7. Frontend Implementation Notes

### Quiz Component Structure
```javascript
const quizCategories = {
  cuisine: {
    question: "What types of cuisine do you enjoy?",
    options: ["Italian", "Mexican", "Chinese", ...],
    multiple: true
  },
  atmosphere: {
    question: "What kind of dining atmosphere do you prefer?",
    options: ["Casual & Relaxed", "Fine Dining", ...],
    multiple: true
  },
  // ... other categories
};
```

### State Management
```javascript
const [quizAnswers, setQuizAnswers] = useState({
  cuisine: [],
  atmosphere: [],
  dietary: [],
  price: [],
  features: []
});
```

### Submission Handler
```javascript
const handleSubmit = async () => {
  const payload = {
    display_name: userName,
    tags: {
      cuisine: quizAnswers.cuisine.map(tag => tag.toLowerCase()),
      atmosphere: quizAnswers.atmosphere.map(tag => tag.toLowerCase()),
      dietary: quizAnswers.dietary.map(tag => tag.toLowerCase()),
      price: quizAnswers.price.map(tag => mapPriceTag(tag)),
      features: quizAnswers.features.map(tag => tag.toLowerCase())
    },
    city: userCity,
    state: userState
  };
  
  await fetch('/api/quiz/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
};
```

---

## 8. Database Schema

### quiz_submissions table
```sql
CREATE TABLE quiz_submissions (
    submission_id SERIAL PRIMARY KEY,
    display_name VARCHAR(100) DEFAULT 'Anonymous',
    quiz_tags JSONB NOT NULL,
    top_twin_user_id VARCHAR(50) NOT NULL,
    top_twin_name VARCHAR(100) NOT NULL,
    match_score DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    city VARCHAR(100) DEFAULT 'Santa Barbara',
    state VARCHAR(50) DEFAULT 'CA',
    processing_status VARCHAR(20) DEFAULT 'completed'
);
```

### restaurants table
```sql
CREATE TABLE restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    cuisine_type VARCHAR(100),
    price_range VARCHAR(10),
    rating DECIMAL(3,2),
    tags TEXT[] NOT NULL
);
```

---

## 9. Testing Examples

### Test Quiz Submission (curl)
```bash
curl -X POST http://localhost:8000/api/quiz/submit \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "TestUser",
    "tags": {
      "cuisine": ["italian", "sushi"],
      "atmosphere": ["casual", "trendy"],
      "dietary": ["vegetarian-friendly"],
      "price": ["moderate"],
      "features": ["happy-hour", "parking"]
    },
    "city": "Durham",
    "state": "NC"
  }'
```

### Test Community Feed (curl)
```bash
curl http://localhost:8000/api/community/feed?limit=10
```

---

## 10. Future Enhancements

- Add user authentication and profiles
- Implement collaborative filtering
- Add restaurant photos and reviews
- Real-time notifications for new taste twins
- Geographic proximity weighting
- Time-based recommendations (breakfast, lunch, dinner)
- Social sharing features
- Favorite restaurants tracking

EOF

# Also create a simple text version
cat > docs/QUIZ_QUICK_REFERENCE.txt << 'EOF'
DINELIKE QUIZ - QUICK REFERENCE
================================

QUIZ CATEGORIES:
1. Cuisine Preferences (15 options)
2. Dining Atmosphere (10 options)
3. Dietary Preferences (9 options)
4. Price Range (4 options)
5. Special Features (12 options)

JSON PAYLOAD TEMPLATE:
{
  "display_name": "YourName",
  "tags": {
    "cuisine": ["italian", "sushi", "mexican"],
    "atmosphere": ["casual", "trendy"],
    "dietary": ["vegetarian-friendly"],
    "price": ["moderate"],
    "features": ["happy-hour", "brunch"]
  },
  "city": "YourCity",
  "state": "YourState"
}

TAG EXAMPLES:
Cuisine: italian, mexican, chinese, sushi, thai, indian, american, burgers, pizza
Atmosphere: casual, fine-dining, trendy, cozy, romantic, family-friendly
Dietary: vegetarian-friendly, vegan-options, gluten-free, healthy
Price: budget, moderate, expensive, luxury
Features: happy-hour, brunch, late-night, parking, live-music

API ENDPOINTS:
POST /api/quiz/submit          - Submit quiz
GET  /api/community/feed       - Get recent submissions
GET  /api/community/stats      - Get statistics
GET  /api/restaurants          - Get restaurants

MATCHING ALGORITHM:
Jaccard Similarity = (Intersection / Union) × 100
Score 70-100% = Excellent Match
Score 50-69%  = Good Match
Score 30-49%  = Fair Match
