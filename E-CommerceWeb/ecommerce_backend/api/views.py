from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.db import transaction, IntegrityError

from rest_framework import generics, filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

from django_elasticsearch_dsl.search import Search
from .documents import ProductDocument, CategoryDocument


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT login view with better error handling
    """
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'detail': 'Invalid email or password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Try to find user by email and authenticate
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
        else:
            return Response({
                'detail': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Get user profile information (JWT protected)
    """
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_joined': user.date_joined
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def bulk_create_products(request):
    """
    Accepts a JSON array of product objects and bulk-creates them.
    Each object should contain: pdt_id, pdt_name, pdt_mrp, pdt_dis_price, pdt_qty, ct_id
    """
    data = request.data
    if not isinstance(data, list):
        return Response({"error": "Expected a JSON array"}, status=status.HTTP_400_BAD_REQUEST)

    created = 0
    errors = []
    objs = []

    with transaction.atomic():
        for i, item in enumerate(data, start=1):
            try:
                # validate required fields
                for f in ("pdt_id", "pdt_name", "pdt_mrp", "pdt_qty", "ct_id"):
                    if f not in item:
                        raise ValueError(f"Missing field: {f}")

                ct_id = item.get("ct_id")
                try:
                    category = Category.objects.get(ct_id=ct_id)
                except Category.DoesNotExist:
                    raise ValueError(f"Category ct_id={ct_id} does not exist")

                # create Product instance (do not save yet)
                p = Product(
                    pdt_id = item.get("pdt_id"),
                    pdt_name = item.get("pdt_name"),
                    pdt_mrp = item.get("pdt_mrp"),
                    pdt_dis_price = item.get("pdt_dis_price"),
                    pdt_qty = item.get("pdt_qty"),
                    ct = category
                )
                objs.append(p)
            except Exception as e:
                errors.append({"index": i, "error": str(e), "item": item})

        # If there were any validation errors, roll back and return
        if errors:
            return Response({"created": 0, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Product.objects.bulk_create(objs)
            created = len(objs)
        except IntegrityError as e:
            return Response({"error": "DB integrity error", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"created": created}, status=status.HTTP_201_CREATED)



@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                return JsonResponse({"message": "Login successful"})
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "POST request required"}, status=400)

    
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('ct_id')
    serializer_class = CategorySerializer

# get single category (optional)
class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'ct_id'

# list products (optionally filter by category via query param)
class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['pdt_name']

    def get_queryset(self):
        qs = Product.objects.select_related('ct').all().order_by('pdt_id')
        ct_id = self.request.query_params.get('ct_id')  # ?ct=1
        if ct_id:
            qs = qs.filter(ct__ct_id=ct_id)
        return qs

# product detail
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related('ct').all()
    serializer_class = ProductSerializer
    lookup_field = 'pdt_id'

#new
@api_view(['GET'])
def search_products(request):
    import re
    from django.db.models import Q as DJQ

    q = request.GET.get('q', '').strip()
    if not q:
        return Response({"products": [], "categories": []}, status=status.HTTP_200_OK)

    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 100))  # Increased to show more results
    start = (page - 1) * size

    # --- Extract price filter and color/attributes ---
    q_lower = q.lower()
    price_filter = None
    color_filter = None
    
    # Extract price with better regex
    price_match = re.search(r'(\d{3,7})', q_lower)
    if price_match:
        amount = float(price_match.group(1))
        if any(word in q_lower for word in ["under", "below", "less", "upto", "up to"]):
            price_filter = ("lte", amount)
        elif any(word in q_lower for word in ["over", "above", "greater", "more than"]):
            price_filter = ("gte", amount)

    # Extract color (if mentioned)
    colors = ["black", "white", "red", "blue", "green", "yellow", "pink", "grey", "gray", "brown", "purple", "orange"]
    for color in colors:
        if color in q_lower:
            color_filter = color
            break

    # Clean query for better text search - remove price and filter words
    search_query = re.sub(r'\b(under|below|less|over|above|greater|than|upto|up to|more than|more|in|with|\d{3,7})\b', '', q_lower).strip()
    if color_filter:
        search_query = search_query.replace(color_filter, '').strip()
    
    # Remove extra spaces
    search_query = ' '.join(search_query.split())
    
    if not search_query:
        search_query = q_lower  # Fallback to original query
    
    # --- Try Elasticsearch first ---
    try:
        from elasticsearch_dsl import Q
        
        ps = ProductDocument.search()
        
        # Build a bool query with should clauses for better semantic matching
        # This allows matching on product name OR category name with synonyms
        bool_query = Q('bool', should=[
            # Match in product name with high boost and synonym support
            Q('match', pdt_name={'query': search_query, 'boost': 3.0, 'fuzziness': 'AUTO'}),
            
            # Match in category name with very high boost (for category-based searches)
            Q('match', **{'ct.ct_name': {'query': search_query, 'boost': 5.0, 'fuzziness': 'AUTO'}}),
            
            # Match in category description
            Q('match', **{'ct.ct_description': {'query': search_query, 'boost': 1.0}}),
            
            # Wildcard match for partial matches
            Q('wildcard', pdt_name={'value': f'*{search_query}*', 'boost': 1.5}),
            Q('wildcard', **{'ct.ct_name': {'value': f'*{search_query}*', 'boost': 2.0}}),
        ], minimum_should_match=1)
        
        ps = ps.query(bool_query)
        
        # Apply price filter
        if price_filter:
            op, val = price_filter
            ps = ps.filter("range", **{"pdt_dis_price": {op: val}})
        
        # Apply color filter if specified
        if color_filter:
            ps = ps.query("match", pdt_name=color_filter)
        
        # Sort by relevance score (default) and limit results
        ps = ps[start:start + size]
        presults = ps.execute()

        products = []
        for hit in presults:
            
            ct = getattr(hit, "ct", None)
            category_name = None
            if ct:
                try:
                    category_name = ct.get("ct_name") if hasattr(ct, "get") else getattr(ct, "ct_name", None)
                except Exception:
                    pass
            
            product_data = {
                "pdt_id": getattr(hit, "pdt_id", None),
                "pdt_name": getattr(hit, "pdt_name", None),
                "pdt_mrp": getattr(hit, "pdt_mrp", None),
                "pdt_dis_price": getattr(hit, "pdt_dis_price", None),
                "pdt_qty": getattr(hit, "pdt_qty", None),
                "category": category_name,
                "score": hit.meta.score if hasattr(hit.meta, 'score') else None,
            }
            products.append(product_data)

        return Response({"products": products, "categories": [], "using": "elasticsearch", "total": len(products)}, status=200)
    
    except Exception as e:
        import traceback
        print(f"❌ Elasticsearch error: {str(e)}")
        print(f"❌ Traceback: {traceback.format_exc()}")
        # --- Fallback to simple DB icontains search ---
        from django.db.models import Case, When, Value, IntegerField
        
        # Search in product name AND category name
        # If category matches, show all products in that category
        pqs = Product.objects.select_related('ct').filter(
            DJQ(pdt_name__icontains=search_query) |
            DJQ(ct__ct_name__icontains=search_query)
        ).annotate(
            relevance=Case(
                # Exact match in category name = highest priority (show all products)
                When(ct__ct_name__iexact=search_query, then=Value(100)),
                # Exact match in product name = very high priority
                When(pdt_name__iexact=search_query, then=Value(90)),
                # Starts with search query in product name = high priority
                When(pdt_name__istartswith=search_query, then=Value(80)),
                # Contains in product name = medium priority
                When(pdt_name__icontains=search_query, then=Value(60)),
                # Contains in category name = low priority
                When(ct__ct_name__icontains=search_query, then=Value(40)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('-relevance', 'pdt_id')
        
        # Apply price filter
        if price_filter:
            op, val = price_filter
            if op == "lte":
                pqs = pqs.filter(pdt_dis_price__lte=val)
            else:
                pqs = pqs.filter(pdt_dis_price__gte=val)
        
        # Apply color filter
        if color_filter:
            pqs = pqs.filter(pdt_name__icontains=color_filter)
        
        pqs = pqs[start:start + size]
        products = [{
            "pdt_id": p.pdt_id,
            "pdt_name": p.pdt_name,
            "pdt_mrp": float(p.pdt_mrp),
            "pdt_dis_price": float(p.pdt_dis_price) if p.pdt_dis_price is not None else None,
            "pdt_qty": p.pdt_qty,
            "category": p.ct.ct_name if p.ct else None,
        } for p in pqs]

        # Return only products (no categories) in fallback mode
        return Response({"products": products, "categories": [], "using": "database_fallback"}, status=200)


@api_view(['GET'])
def elasticsearch_fulltext_search(request):
    """
    Enhanced Elasticsearch full-text search endpoint using multi_match queries.
    Returns top results ranked by relevance score.
    
    Query Parameters:
    - q: Search query (required)
    - page: Page number (default: 1)
    - size: Results per page (default: 20)
    - fields: Comma-separated fields to search (default: pdt_name,ct.ct_name)
    - min_price: Minimum price filter
    - max_price: Maximum price filter
    
    Example: /api/elasticsearch-search/?q=laptop&size=10&min_price=500&max_price=2000
    """
    from elasticsearch_dsl import Q
    
    # Get query parameters
    query = request.GET.get('q', '').strip()
    if not query:
        return Response({
            "error": "Query parameter 'q' is required",
            "products": [],
            "total": 0
        }, status=status.HTTP_400_BAD_REQUEST)
    
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 20))
    start = (page - 1) * size
    
    # Get search fields (default to product name and category name)
    fields_param = request.GET.get('fields', 'pdt_name,ct.ct_name')
    search_fields = [f.strip() for f in fields_param.split(',')]
    
    # Price filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    try:
        # Initialize search
        search = ProductDocument.search()
        
        # Build multi_match query for full-text search across multiple fields
        # This uses Elasticsearch's relevance scoring algorithm
        search = search.query(
            "multi_match",
            query=query,
            fields=search_fields,
            type="best_fields",  # Uses the best matching field's score
            fuzziness="AUTO",     # Handles typos automatically
            operator="or",        # Match any of the terms
            minimum_should_match="75%"  # At least 75% of terms should match
        )
        
        # Apply price range filters if provided
        if min_price or max_price:
            price_range = {}
            if min_price:
                price_range['gte'] = float(min_price)
            if max_price:
                price_range['lte'] = float(max_price)
            search = search.filter("range", pdt_dis_price=price_range)
        
        # Get total count before pagination
        total_count = search.count()
        
        # Apply pagination and execute
        search = search[start:start + size]
        results = search.execute()
        
        # Format results with relevance scores
        products = []
        for hit in results:
            ct = getattr(hit, "ct", None)
            category_name = None
            if ct:
                try:
                    category_name = ct.get("ct_name") if hasattr(ct, "get") else getattr(ct, "ct_name", None)
                except Exception:
                    pass
            
            product_data = {
                "pdt_id": getattr(hit, "pdt_id", None),
                "pdt_name": getattr(hit, "pdt_name", None),
                "pdt_mrp": getattr(hit, "pdt_mrp", None),
                "pdt_dis_price": getattr(hit, "pdt_dis_price", None),
                "pdt_qty": getattr(hit, "pdt_qty", None),
                "category": category_name,
                "relevance_score": hit.meta.score if hasattr(hit.meta, 'score') else None,
            }
            products.append(product_data)
        
        return Response({
            "query": query,
            "total": total_count,
            "page": page,
            "size": size,
            "products": products,
            "search_engine": "elasticsearch",
            "search_type": "multi_match_fulltext"
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Elasticsearch error: {str(e)}")
        print(f"❌ Traceback: {error_trace}")
        
        return Response({
            "error": "Elasticsearch search failed",
            "detail": str(e),
            "products": [],
            "total": 0
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)