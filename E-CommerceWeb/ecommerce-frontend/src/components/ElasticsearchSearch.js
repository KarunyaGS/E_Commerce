// Enhanced Elasticsearch Search Component
import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { searchProducts, getSearchSuggestions, checkElasticsearchHealth } from '../services/elasticsearch';

const ElasticsearchSearch = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [elasticsearchStatus, setElasticsearchStatus] = useState(null);
  const navigate = useNavigate();

  // Check Elasticsearch health on component mount
  useEffect(() => {
    const checkHealth = async () => {
      const health = await checkElasticsearchHealth();
      setElasticsearchStatus(health);
    };
    checkHealth();
  }, []);

  // Debounced suggestions
  const getSuggestions = useCallback(
    debounce(async (query) => {
      if (query.length > 2) {
        try {
          const suggestions = await getSearchSuggestions(query);
          setSuggestions(suggestions);
          setShowSuggestions(true);
        } catch (error) {
          console.error('Failed to get suggestions:', error);
        }
      } else {
        setSuggestions([]);
        setShowSuggestions(false);
      }
    }, 300),
    []
  );

  // Handle search input change
  const handleInputChange = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    getSuggestions(value);
  };

  // Perform search
  const handleSearch = async (query = searchTerm) => {
    if (!query.trim()) return;

    setIsLoading(true);
    setShowSuggestions(false);

    try {
      // Extract price range from query
      const priceMatch = query.match(/(\d{3,7})/);
      let minPrice, maxPrice;
      
      if (priceMatch) {
        const amount = parseFloat(priceMatch[1]);
        if (query.includes('under') || query.includes('below') || query.includes('less')) {
          maxPrice = amount;
        } else if (query.includes('over') || query.includes('above') || query.includes('more')) {
          minPrice = amount;
        }
      }

      // Clean query for text search
      const cleanQuery = query.replace(/\b(under|below|less|over|above|greater|than|more|in|with|\d{3,7})\b/g, '').trim();

      const results = await searchProducts(cleanQuery, {
        minPrice,
        maxPrice,
        size: 50
      });

      // Navigate to results page with data
      navigate('/search', { 
        state: { 
          results, 
          query: query,
          searchEngine: 'elasticsearch-direct'
        } 
      });

    } catch (error) {
      console.error('Search failed:', error);
      // Fallback to API search
      navigate(`/search?q=${encodeURIComponent(query)}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle suggestion click
  const handleSuggestionClick = (suggestion) => {
    setSearchTerm(suggestion);
    setShowSuggestions(false);
    handleSearch(suggestion);
  };

  // Handle key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
    }
  };

  return (
    <div className="position-relative" style={{ width: '350px' }}>
      {/* Elasticsearch Status Indicator */}
      {elasticsearchStatus && (
        <div className="d-flex align-items-center mb-2">
          <span 
            className={`badge ${elasticsearchStatus.status === 'green' ? 'bg-success' : 'bg-warning'}`}
            title={`Elasticsearch: ${elasticsearchStatus.status} | Nodes: ${elasticsearchStatus.number_of_nodes}`}
          >
            🔍 ES: {elasticsearchStatus.status}
          </span>
        </div>
      )}

      {/* Search Input */}
      <div className="input-group">
        <input
          type="text"
          className="form-control"
          placeholder="Search electronics, clothing, laptops under 40000..."
          value={searchTerm}
          onChange={handleInputChange}
          onKeyDown={handleKeyPress}
          onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          disabled={isLoading}
        />
        <button 
          className="btn btn-primary" 
          onClick={() => handleSearch()}
          disabled={isLoading || !searchTerm.trim()}
        >
          {isLoading ? (
            <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          ) : (
            '🔍 Search'
          )}
        </button>
      </div>

      {/* Search Suggestions Dropdown */}
      {showSuggestions && suggestions.length > 0 && (
        <div 
          className="position-absolute w-100 bg-white border rounded shadow-lg mt-1" 
          style={{ zIndex: 1000, maxHeight: '200px', overflowY: 'auto' }}
        >
          {suggestions.map((suggestion, index) => (
            <div
              key={index}
              className="px-3 py-2 cursor-pointer hover-bg-light"
              onClick={() => handleSuggestionClick(suggestion)}
              onMouseDown={(e) => e.preventDefault()} // Prevent blur
              style={{ cursor: 'pointer' }}
            >
              <small className="text-muted">💡</small> {suggestion}
            </div>
          ))}
        </div>
      )}

      {/* Search Examples */}
      <div className="mt-2">
        <small className="text-muted">
          Try: 
          <span 
            className="text-primary ms-1 cursor-pointer" 
            onClick={() => handleSearch('electronics')}
            style={{ cursor: 'pointer' }}
          >
            electronics
          </span>, 
          <span 
            className="text-primary ms-1 cursor-pointer"
            onClick={() => handleSearch('cloth')}
            style={{ cursor: 'pointer' }}
          >
            cloth
          </span>, 
          <span 
            className="text-primary ms-1 cursor-pointer"
            onClick={() => handleSearch('laptops under 40000')}
            style={{ cursor: 'pointer' }}
          >
            laptops under 40000
          </span>
        </small>
      </div>
    </div>
  );
};

// Debounce utility function
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

export default ElasticsearchSearch;
