// Browser-compatible Elasticsearch service using fetch API
const ELASTICSEARCH_URL = 'http://localhost:9200';

// Helper function to make HTTP requests to Elasticsearch
const elasticsearchRequest = async (endpoint, method = 'GET', body = null) => {
  try {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    if (body) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(`${ELASTICSEARCH_URL}${endpoint}`, options);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Elasticsearch request failed:', error);
    throw error;
  }
};

// Search products using Elasticsearch
export const searchProducts = async (query, options = {}) => {
  try {
    const {
      page = 1,
      size = 20,
      minPrice,
      maxPrice,
      category
    } = options;

    const from = (page - 1) * size;

    // Build Elasticsearch query
    const searchBody = {
      query: {
        bool: {
          should: [
            // Match in product name with high boost
            {
              match: {
                pdt_name: {
                  query: query,
                  boost: 3.0,
                  fuzziness: 'AUTO'
                }
              }
            },
            // Match in category name with very high boost
            {
              match: {
                'ct.ct_name': {
                  query: query,
                  boost: 5.0,
                  fuzziness: 'AUTO'
                }
              }
            },
            // Match in category description
            {
              match: {
                'ct.ct_description': {
                  query: query,
                  boost: 1.0
                }
              }
            },
            // Wildcard matches for partial matching
            {
              wildcard: {
                pdt_name: {
                  value: `*${query.toLowerCase()}*`,
                  boost: 1.5
                }
              }
            },
            {
              wildcard: {
                'ct.ct_name': {
                  value: `*${query.toLowerCase()}*`,
                  boost: 2.0
                }
              }
            }
          ],
          minimum_should_match: 1,
          filter: []
        }
      },
      from: from,
      size: size,
      sort: [
        { _score: { order: 'desc' } },
        { pdt_id: { order: 'asc' } }
      ]
    };

    // Add price range filter if specified
    if (minPrice || maxPrice) {
      const priceRange = {};
      if (minPrice) priceRange.gte = minPrice;
      if (maxPrice) priceRange.lte = maxPrice;
      
      searchBody.query.bool.filter.push({
        range: {
          pdt_dis_price: priceRange
        }
      });
    }

    // Add category filter if specified
    if (category) {
      searchBody.query.bool.filter.push({
        match: {
          'ct.ct_name': category
        }
      });
    }

    const response = await elasticsearchRequest('/products/_search', 'POST', searchBody);

    // Format results
    const products = response.hits.hits.map(hit => ({
      pdt_id: hit._source.pdt_id,
      pdt_name: hit._source.pdt_name,
      pdt_mrp: hit._source.pdt_mrp,
      pdt_dis_price: hit._source.pdt_dis_price,
      pdt_qty: hit._source.pdt_qty,
      category: hit._source.ct?.ct_name,
      score: hit._score
    }));

    return {
      products,
      total: response.hits.total.value || response.hits.total,
      took: response.took,
      engine: 'elasticsearch-direct'
    };

  } catch (error) {
    console.error('Elasticsearch search error:', error);
    throw new Error(`Search failed: ${error.message}`);
  }
};

// Get search suggestions
export const getSearchSuggestions = async (query) => {
  try {
    const searchBody = {
      suggest: {
        product_suggest: {
          prefix: query,
          completion: {
            field: 'pdt_name.suggest',
            size: 5
          }
        },
        category_suggest: {
          prefix: query,
          completion: {
            field: 'ct.ct_name.suggest',
            size: 3
          }
        }
      }
    };

    const response = await elasticsearchRequest('/products/_search', 'POST', searchBody);

    const suggestions = [
      ...(response.suggest?.product_suggest?.[0]?.options?.map(opt => opt.text) || []),
      ...(response.suggest?.category_suggest?.[0]?.options?.map(opt => opt.text) || [])
    ];

    return [...new Set(suggestions)]; // Remove duplicates
  } catch (error) {
    console.error('Suggestion error:', error);
    return [];
  }
};

// Check Elasticsearch health
export const checkElasticsearchHealth = async () => {
  try {
    const response = await elasticsearchRequest('/_cluster/health');
    return {
      status: response.status,
      cluster_name: response.cluster_name,
      number_of_nodes: response.number_of_nodes
    };
  } catch (error) {
    console.error('Elasticsearch health check failed:', error);
    return null;
  }
};
