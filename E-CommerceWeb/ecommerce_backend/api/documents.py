from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer
from .models import Product, Category

# 🔹 Define a lowercase analyzer
lowercase_analyzer = analyzer(
    'lowercase_analyzer',
    tokenizer="standard",
    filter=["lowercase"]
)

# 🔹 Create and configure a separate index for categories
categories_index = Index('categories')
categories_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
    analysis={
        "analyzer": {
            "lowercase_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase"]
            }
        }
    }
)

# 🔹 Create and configure the index with synonym analyzer for better semantic search
products_index = Index('products')
products_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
    analysis={
        "filter": {
            "synonym_filter": {
                "type": "synonym",
                "synonyms": [
                    # Electronics synonyms
                    "mobile, phone, smartphone, cellphone, mobiles, phones",
                    "laptop, notebook, ultrabook, laptops, computer",
                    "tv, television, smart tv, televisions",
                    "headphone, earphone, earphones, headphones, earbuds, headset",
                    "tablet, ipad, tabs",
                    "watch, smartwatch, wearable",
                    "camera, dslr, camcorder",
                    
                    # Clothing synonyms
                    "clothing, clothes, apparel, wear, garment, garments, dress, attire",
                    "shirt, tshirt, t-shirt, top, blouse",
                    "pant, pants, trouser, trousers, jeans, bottom",
                    "shoe, shoes, footwear, sneaker, sneakers",
                    "jacket, coat, hoodie, sweatshirt",
                    "dress, gown, frock",
                    
                    # Accessories
                    "bag, backpack, handbag, purse",
                    "belt, belts, strap",
                    "wallet, purse",
                    
                    # Home & Kitchen
                    "furniture, furnishing",
                    "appliance, appliances, device, devices",
                ]
            }
        },
        "analyzer": {
            "lowercase_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase"]
            },
            "synonym_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase", "synonym_filter"]
            }
        }
    }
)

@registry.register_document
class ProductDocument(Document):
    # 🔹 Embed related Category fields with synonym support
    ct = fields.ObjectField(properties={
        'ct_id': fields.IntegerField(),
        'ct_name': fields.TextField(
            analyzer='synonym_analyzer',
            fields={'raw': fields.KeywordField()}
        ),
        'ct_description': fields.TextField(analyzer='synonym_analyzer'),
    })

    # 🔹 Define product fields with synonym support
    pdt_id = fields.IntegerField()
    pdt_name = fields.TextField(
        analyzer='synonym_analyzer',
        fields={'raw': fields.KeywordField()}
    )
    pdt_mrp = fields.FloatField()
    pdt_dis_price = fields.FloatField()
    pdt_qty = fields.IntegerField()

    class Index:
        name = 'products'
        settings = products_index._settings

    class Django:
        model = Product
        fields = []
        related_models = [Category]

    # 🔹 Prepare category data for indexing
    def prepare_ct(self, instance):
        if instance.ct:
            return {
                'ct_id': instance.ct.ct_id,
                'ct_name': instance.ct.ct_name,
                'ct_description': instance.ct.ct_description or '',
            }
        return None

    # 🔁 Reindex products when a related category changes
    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            return related_instance.products.all()


# 🔹 Category document for ES search
@registry.register_document
class CategoryDocument(Document):
    ct_id = fields.IntegerField()
    ct_name = fields.TextField(analyzer=lowercase_analyzer)
    ct_description = fields.TextField(analyzer=lowercase_analyzer)

    class Index:
        name = 'categories'
        settings = categories_index._settings

    class Django:
        model = Category
        fields = []
