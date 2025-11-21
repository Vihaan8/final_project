import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import '../styles/Quiz.css'

const Quiz = () => {
  const navigate = useNavigate()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState({
    priorities: [],
    dining_style: [],
    meal_timing: [],
    cuisines: [],
    adventure_level: '',
    price_sensitivity: ''
  })

  const questions = [
    {
      id: 'cuisines',
      title: 'Pick your favorite cuisine!',
      max: 4,
      options: [
        { value: 'mexican', label: 'Mexican', image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400' },
        { value: 'seafood', label: 'Seafood', image: 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400' },
        { value: 'italian', label: 'Italian', image: 'https://images.unsplash.com/photo-1595295333158-4742f28fbd85?w=400' },
        { value: 'american', label: 'American', image: 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=400' },
        { value: 'japanese', label: 'Japanese', image: 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400' },
        { value: 'thai', label: 'Thai', image: 'https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400' },
        { value: 'cajun', label: 'Cajun', image: 'https://images.unsplash.com/photo-1604908815453-3b4c0f1f7e66?w=400' },
        { value: 'indian', label: 'Indian', image: 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400' }
      ]
    },
    {
      id: 'dining_style',
      title: 'What kind of dining atmosphere do you prefer?',
      max: 2,
      options: [
        { value: 'upscale', label: 'Fine dining', image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400' },
        { value: 'casual', label: 'Casual cafe', image: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=400' },
        { value: 'lively', label: 'Food truck', image: 'https://images.unsplash.com/photo-1565123409695-7b5ef63a2efb?w=400' },
        { value: 'cozy', label: 'Cozy & intimate', image: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400' }
      ]
    },
    {
      id: 'priorities',
      title: 'What matters most to you?',
      max: 2,
      options: [
        { value: 'food_quality', label: 'Food quality' },
        { value: 'atmosphere', label: 'Atmosphere' },
        { value: 'service', label: 'Service' },
        { value: 'value', label: 'Value for money' }
      ]
    },
    {
      id: 'meal_timing',
      title: 'When do you prefer to eat out?',
      max: 4,
      options: [
        { value: 'breakfast', label: 'Breakfast' },
        { value: 'brunch', label: 'Brunch' },
        { value: 'lunch', label: 'Lunch' },
        { value: 'dinner', label: 'Dinner' }
      ]
    },
    {
      id: 'adventure_level',
      title: 'How adventurous are you with food?',
      type: 'single',
      options: [
        { value: 'traditional', label: 'Traditional - stick to familiar' },
        { value: 'moderate', label: 'Moderate - try new things occasionally' },
        { value: 'adventurous', label: 'Adventurous - love unique experiences' },
        { value: 'very_adventurous', label: 'Very adventurous - the weirder the better' }
      ]
    },
    {
      id: 'price_sensitivity',
      title: 'What is your typical price range?',
      type: 'single',
      options: [
        { value: 'budget', label: '$ (under $15)' },
        { value: 'moderate', label: '$$ ($15-30)' },
        { value: 'upscale', label: '$$$ ($30-60)' },
        { value: 'fine_dining', label: '$$$$ (over $60)' }
      ]
    }
  ]

  const handleSelect = (questionId, value) => {
    const currentQ = questions.find(q => q.id === questionId)
    
    if (currentQ.type === 'single') {
      setAnswers({ ...answers, [questionId]: value })
    } else {
      const current = answers[questionId] || []
      const max = currentQ.max || 2
      
      if (current.includes(value)) {
        setAnswers({ ...answers, [questionId]: current.filter(v => v !== value) })
      } else if (current.length < max) {
        setAnswers({ ...answers, [questionId]: [...current, value] })
      }
    }
  }

  const canProceed = () => {
    const currentQ = questions[currentQuestion]
    if (currentQ.type === 'single') {
      return !!answers[currentQ.id]
    }
    return (answers[currentQ.id] || []).length > 0
  }

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/quiz/submit', {
        priorities: answers.priorities || [],
        dining_style: answers.dining_style || [],
        meal_timing: answers.meal_timing || [],
        cuisines: answers.cuisines || [],
        adventure_level: answers.adventure_level || 'moderate',
        price_sensitivity: answers.price_sensitivity || 'moderate',
        display_name: 'Anonymous'
      })
      
      navigate('/results', { state: { data: response.data } })
    } catch (error) {
      console.error('Error submitting quiz:', error)
      alert('Error submitting quiz. Make sure API is running on port 8000.')
    }
  }

  const currentQ = questions[currentQuestion]
  const progress = ((currentQuestion + 1) / questions.length) * 100

  return (
    <div className="quiz-container">
      <div className="quiz-header">
        <h1>Find Your Restaurant Twin!</h1>
        <p>Answer {questions.length} questions and we'll match you with your dining twin</p>
      </div>

      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }}></div>
      </div>

      <div className="question-container">
        <h2 className="question-title">{currentQ.title}</h2>
        
        <div className={currentQ.options.length > 4 ? 'options-grid-large' : 'options-grid'}>
          {currentQ.options.map(option => {
            const isSelected = currentQ.type === 'single' 
              ? answers[currentQ.id] === option.value
              : (answers[currentQ.id] || []).includes(option.value)
            
            return (
              <div
                key={option.value}
                className={`option-card ${isSelected ? 'selected' : ''} ${!option.image ? 'text-only' : ''}`}
                onClick={() => handleSelect(currentQ.id, option.value)}
              >
                {option.image && <img src={option.image} alt={option.label} />}
                <span>{option.label}</span>
              </div>
            )
          })}
        </div>

        <div className="navigation-buttons">
          {currentQuestion > 0 && (
            <button className="btn-secondary" onClick={() => setCurrentQuestion(currentQuestion - 1)}>
              Back
            </button>
          )}
          {currentQuestion < questions.length - 1 ? (
            <button 
              className="btn-primary" 
              onClick={() => setCurrentQuestion(currentQuestion + 1)}
              disabled={!canProceed()}
            >
              Next ({currentQuestion + 1}/{questions.length})
            </button>
          ) : (
            <button className="btn-primary" onClick={handleSubmit} disabled={!canProceed()}>
              Find My Twins!
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default Quiz
