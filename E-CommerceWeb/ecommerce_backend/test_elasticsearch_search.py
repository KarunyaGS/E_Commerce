#!/usr/bin/env python
"""
Test script for Elasticsearch full-text search functionality.
Run this after setting up Elasticsearch and populating the indices.

Usage:
    python test_elasticsearch_search.py
"""

import requests
import json
from typing import Dict, Any

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def print_separator():
    """Print a visual separator."""
    print("\n" + "="*80 + "\n")

def test_search(endpoint: str, params: Dict[str, Any], test_name: str):
    """
    Test a search endpoint with given parameters.
    
    Args:
        endpoint: API endpoint path
        params: Query parameters
        test_name: Name of the test for display
    """
    print(f"🔍 TEST: {test_name}")
    print(f"Endpoint: {endpoint}")
    print(f"Parameters: {json.dumps(params, indent=2)}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=10)
        
        print(f"\n📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Display results based on endpoint
            if 'total' in data:
                print(f"✅ Total Results: {data['total']}")
                print(f"📄 Page: {data.get('page', 'N/A')}")
                print(f"📦 Results Returned: {len(data.get('products', []))}")
                
                if data.get('search_engine'):
                    print(f"🔧 Search Engine: {data['search_engine']}")
                if data.get('search_type'):
                    print(f"🎯 Search Type: {data['search_type']}")
            else:
                print(f"✅ Results Returned: {len(data.get('products', []))}")
                if data.get('using'):
                    print(f"🔧 Using: {data['using']}")
            
            # Display top 3 results with relevance scores
            products = data.get('products', [])
            if products:
                print(f"\n📋 Top {min(3, len(products))} Results:")
                for i, product in enumerate(products[:3], 1):
                    print(f"\n  {i}. {product.get('pdt_name', 'N/A')}")
                    print(f"     ID: {product.get('pdt_id', 'N/A')}")
                    print(f"     Category: {product.get('category', 'N/A')}")
                    print(f"     Price: ₹{product.get('pdt_dis_price', product.get('pdt_mrp', 'N/A'))}")
                    
                    # Show relevance score if available
                    if 'relevance_score' in product:
                        print(f"     Relevance Score: {product['relevance_score']:.4f}")
                    elif 'score' in product:
                        print(f"     Score: {product['score']}")
            else:
                print("\n⚠️  No products found")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Django server is running on http://localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print_separator()

def main():
    """Run all test cases."""
    print("="*80)
    print("🚀 ELASTICSEARCH FULL-TEXT SEARCH TEST SUITE")
    print("="*80)
    
    # Test 1: Basic search using new Elasticsearch endpoint
    test_search(
        endpoint="/elasticsearch-search/",
        params={"q": "laptop", "size": 5},
        test_name="Basic Elasticsearch Full-Text Search"
    )
    
    # Test 2: Search with price range filter
    test_search(
        endpoint="/elasticsearch-search/",
        params={"q": "phone", "min_price": 10000, "max_price": 30000, "size": 5},
        test_name="Search with Price Range Filter"
    )
    
    # Test 3: Search in specific fields (category name)
    test_search(
        endpoint="/elasticsearch-search/",
        params={"q": "electronics", "fields": "ct.ct_name", "size": 5},
        test_name="Search in Category Name Only"
    )
    
    # Test 4: Fuzzy search (with typo)
    test_search(
        endpoint="/elasticsearch-search/",
        params={"q": "lapto", "size": 5},
        test_name="Fuzzy Search (Typo Handling)"
    )
    
    # Test 5: Multi-word search
    test_search(
        endpoint="/elasticsearch-search/",
        params={"q": "wireless headphones", "size": 5},
        test_name="Multi-Word Search"
    )
    
    # Test 6: Pagination test
    test_search(
        endpoint="/elasticsearch-search/",
        params={"q": "phone", "page": 1, "size": 3},
        test_name="Pagination - Page 1"
    )
    
    test_search(
        endpoint="/elasticsearch-search/",
        params={"q": "phone", "page": 2, "size": 3},
        test_name="Pagination - Page 2"
    )
    
    # Test 7: Compare with existing search endpoint
    test_search(
        endpoint="/search/",
        params={"q": "laptop", "size": 5},
        test_name="Existing Search Endpoint (for comparison)"
    )
    
    # Test 8: Search with no results
    test_search(
        endpoint="/elasticsearch-search/",
        params={"q": "nonexistentproduct12345", "size": 5},
        test_name="Search with No Results"
    )
    
    # Test 9: Empty query (should return error)
    test_search(
        endpoint="/elasticsearch-search/",
        params={"size": 5},
        test_name="Empty Query (Error Case)"
    )
    
    print("✅ All tests completed!")
    print("\n📝 SUMMARY:")
    print("   - The new /elasticsearch-search/ endpoint uses Elasticsearch multi_match queries")
    print("   - Results are ranked by relevance score")
    print("   - Supports fuzzy matching for typos")
    print("   - Allows price range filtering")
    print("   - Supports field-specific searches")
    print("   - Includes pagination support")

if __name__ == "__main__":
    main()
