# URL Routing Guide

## Current Configuration

### Base Setup
- **Development Server**: http://localhost:3001
- **Base Path**: /quick-commerce
- **Full Base URL**: http://localhost:3001/quick-commerce

### Router Configuration
The app uses React Router v7 with BrowserRouter configured with basename="/quick-commerce"

## All Routes

| Page | Route Path | Full URL | Component |
|------|-----------|----------|-----------|
| Home | `/` | http://localhost:3001/quick-commerce/ | Home |
| Welcome | `/welcome` | http://localhost:3001/quick-commerce/welcome | Welcome |
| Sign In | `/signin` | http://localhost:3001/quick-commerce/signin | SignIn |
| Sign Up | `/signup` | http://localhost:3001/quick-commerce/signup | SignUp |
| Category Products | `/category/:id` | http://localhost:3001/quick-commerce/category/1 | CategoryProducts |
| Category Page | `/e-commerce/category/:ct_id` | http://localhost:3001/quick-commerce/e-commerce/category/1 | CategoryPage |
| All Products | `/all-products` | http://localhost:3001/quick-commerce/all-products | AllProducts |
| Search Results | `/search?q=query` | http://localhost:3001/quick-commerce/search?q=laptop | SearchResults |

## Navigation Best Practices

### Using Link Component
```javascript
import { Link } from 'react-router-dom';

// Correct - relative path
<Link to="/all-products">View All Products</Link>

// Incorrect - don't include basename
<Link to="/quick-commerce/all-products">View All Products</Link>
```

### Using navigate() Hook
```javascript
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();

// Correct - relative path
navigate('/category/1');

// Incorrect - don't include basename
navigate('/quick-commerce/category/1');
```

## Troubleshooting

### URLs Not Updating
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+Shift+R)
3. Clear React dev server cache: `rm -rf node_modules/.cache`
4. Restart development server

### Page Not Found (404)
- Verify the route exists in App.js
- Check that basename is set correctly in index.js
- Ensure navigation uses relative paths (no /quick-commerce prefix)

### Navigation Works But URL Doesn't Change
- Make sure you're using `navigate()` or `<Link>` from react-router-dom
- Don't use `<a href>` tags for internal navigation
- Don't use `window.location.href` for internal navigation

## Current Issues Fixed

✅ Navbar hidden on sign-in/sign-up pages
✅ Duplicate search bar removed from Home page
✅ All routes properly configured with basename
✅ Navigation using React Router components

## Testing Navigation

To test if routing is working:

1. Start the development server
2. Navigate to: http://localhost:3001/quick-commerce/
3. Click on any category - URL should change to /quick-commerce/category/X
4. Click "View All Products" - URL should change to /quick-commerce/all-products
5. Use search - URL should change to /quick-commerce/search?q=...
6. Check browser address bar - it should always show the full path

If URLs are not updating, try:
- Hard refresh the browser (Ctrl+Shift+R)
- Open browser DevTools and disable cache
- Restart the development server
