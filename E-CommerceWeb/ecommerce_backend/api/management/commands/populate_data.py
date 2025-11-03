from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Category, Product
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with 15 categories and 300 products (20 per category)'

    def handle(self, *args, **options):
        self.stdout.write('Starting data population...')
        
        # Clear existing data
        with transaction.atomic():
            Product.objects.all().delete()
            Category.objects.all().delete()
            
        # Category data with descriptions
        categories_data = [
            ("Electronics", "Smartphones, laptops, tablets and electronic gadgets"),
            ("Fashion", "Clothing, shoes, accessories for men and women"),
            ("Home & Kitchen", "Furniture, appliances, cookware and home decor"),
            ("Books", "Fiction, non-fiction, educational and reference books"),
            ("Sports & Fitness", "Exercise equipment, sportswear and outdoor gear"),
            ("Beauty & Personal Care", "Cosmetics, skincare, haircare and wellness products"),
            ("Automotive", "Car accessories, tools and automotive parts"),
            ("Toys & Games", "Children's toys, board games and educational toys"),
            ("Health & Wellness", "Vitamins, supplements and health monitoring devices"),
            ("Garden & Outdoor", "Plants, gardening tools and outdoor furniture"),
            ("Office Supplies", "Stationery, office furniture and business equipment"),
            ("Pet Supplies", "Pet food, toys, accessories and care products"),
            ("Music & Instruments", "Musical instruments, audio equipment and accessories"),
            ("Travel & Luggage", "Suitcases, travel accessories and outdoor gear"),
            ("Art & Crafts", "Art supplies, craft materials and creative tools")
        ]
        
        # Create categories
        categories = []
        for name, description in categories_data:
            category = Category.objects.create(
                ct_name=name,
                ct_description=description
            )
            categories.append(category)
            self.stdout.write(f'Created category: {name}')
        
        # Product templates for each category
        product_templates = {
            "Electronics": [
                "Smartphone", "Laptop", "Tablet", "Headphones", "Smart Watch", "Camera", "Speaker", "Monitor",
                "Keyboard", "Mouse", "Charger", "Power Bank", "USB Cable", "Webcam", "Microphone", "Router",
                "Hard Drive", "Memory Card", "Gaming Console", "Smart TV"
            ],
            "Fashion": [
                "T-Shirt", "Jeans", "Dress", "Jacket", "Sneakers", "Boots", "Hat", "Scarf",
                "Handbag", "Wallet", "Sunglasses", "Belt", "Watch", "Earrings", "Necklace", "Ring",
                "Sweater", "Shorts", "Skirt", "Blazer"
            ],
            "Home & Kitchen": [
                "Coffee Maker", "Blender", "Toaster", "Microwave", "Refrigerator", "Dishwasher", "Vacuum", "Iron",
                "Bed Sheet", "Pillow", "Curtain", "Lamp", "Mirror", "Clock", "Vase", "Candle",
                "Cookware Set", "Dinnerware", "Storage Box", "Trash Can"
            ],
            "Books": [
                "Fiction Novel", "Biography", "Cookbook", "Travel Guide", "History Book", "Science Book", "Art Book", "Poetry",
                "Self-Help", "Business Book", "Children's Book", "Comic Book", "Dictionary", "Encyclopedia", "Textbook", "Journal",
                "Mystery Novel", "Romance Novel", "Fantasy Book", "Technical Manual"
            ],
            "Sports & Fitness": [
                "Running Shoes", "Yoga Mat", "Dumbbell", "Treadmill", "Basketball", "Football", "Tennis Racket", "Golf Club",
                "Fitness Tracker", "Water Bottle", "Gym Bag", "Resistance Band", "Jump Rope", "Exercise Bike", "Protein Powder", "Swimsuit",
                "Hiking Boots", "Camping Tent", "Sleeping Bag", "Backpack"
            ],
            "Beauty & Personal Care": [
                "Face Cream", "Shampoo", "Conditioner", "Body Lotion", "Perfume", "Lipstick", "Foundation", "Mascara",
                "Toothbrush", "Toothpaste", "Soap", "Deodorant", "Hair Dryer", "Razor", "Nail Polish", "Face Mask",
                "Sunscreen", "Body Wash", "Hair Oil", "Eye Cream"
            ],
            "Automotive": [
                "Car Cover", "Floor Mats", "Air Freshener", "Phone Mount", "Dash Cam", "Jump Starter", "Tire Gauge", "Tool Kit",
                "Car Charger", "Seat Cover", "Steering Wheel Cover", "Window Tint", "Car Wax", "Oil Filter", "Brake Pads", "Headlight",
                "Car Battery", "GPS Navigator", "Backup Camera", "Car Vacuum"
            ],
            "Toys & Games": [
                "LEGO Set", "Doll", "Action Figure", "Board Game", "Puzzle", "Remote Car", "Teddy Bear", "Building Blocks",
                "Art Set", "Musical Toy", "Educational Toy", "Ball", "Kite", "Yo-Yo", "Card Game", "Video Game",
                "Toy Train", "Dollhouse", "Robot Toy", "Playdough"
            ],
            "Health & Wellness": [
                "Vitamin C", "Multivitamin", "Protein Supplement", "Blood Pressure Monitor", "Thermometer", "First Aid Kit", "Massage Gun", "Essential Oil",
                "Meditation Cushion", "Air Purifier", "Humidifier", "Scale", "Pulse Oximeter", "Heating Pad", "Ice Pack", "Compression Socks",
                "Sleep Mask", "Earplugs", "Posture Corrector", "Stress Ball"
            ],
            "Garden & Outdoor": [
                "Garden Hose", "Lawn Mower", "Plant Pot", "Garden Tools", "Fertilizer", "Seeds", "Watering Can", "Pruning Shears",
                "Outdoor Chair", "Patio Table", "Umbrella", "Fire Pit", "Garden Light", "Sprinkler", "Compost Bin", "Garden Gloves",
                "Bird Feeder", "Wind Chime", "Garden Statue", "Greenhouse"
            ],
            "Office Supplies": [
                "Notebook", "Pen", "Pencil", "Marker", "Stapler", "Paper Clips", "Folder", "Binder",
                "Desk Organizer", "Office Chair", "Desk Lamp", "Calculator", "Printer Paper", "Sticky Notes", "Tape", "Scissors",
                "Whiteboard", "Cork Board", "File Cabinet", "Shredder"
            ],
            "Pet Supplies": [
                "Dog Food", "Cat Food", "Pet Bed", "Leash", "Collar", "Pet Toy", "Litter Box", "Pet Carrier",
                "Food Bowl", "Water Bowl", "Pet Shampoo", "Pet Brush", "Pet Treats", "Scratching Post", "Pet Gate", "Pet Camera",
                "Aquarium", "Bird Cage", "Hamster Wheel", "Pet Blanket"
            ],
            "Music & Instruments": [
                "Guitar", "Piano Keyboard", "Drums", "Violin", "Microphone", "Audio Interface", "Studio Monitor", "Headphones",
                "Guitar Pick", "Music Stand", "Metronome", "Capo", "Guitar Strings", "Piano Bench", "Drum Sticks", "Music Sheet",
                "Amplifier", "Audio Cable", "Pop Filter", "Acoustic Foam"
            ],
            "Travel & Luggage": [
                "Suitcase", "Backpack", "Travel Pillow", "Luggage Tag", "Passport Holder", "Travel Adapter", "Packing Cubes", "Duffel Bag",
                "Travel Mug", "Portable Charger", "Travel Lock", "Compression Socks", "Eye Mask", "Neck Pillow", "Travel Blanket", "Toiletry Bag",
                "Money Belt", "Travel Journal", "Luggage Scale", "Travel Umbrella"
            ],
            "Art & Crafts": [
                "Paint Set", "Canvas", "Paintbrush", "Colored Pencils", "Markers", "Sketchbook", "Clay", "Glue",
                "Scissors", "Craft Paper", "Beads", "Yarn", "Knitting Needles", "Embroidery Kit", "Stickers", "Glitter",
                "Fabric Paint", "Craft Knife", "Cutting Mat", "Ruler"
            ]
        }
        
        # Create products for each category
        all_products = []
        for category in categories:
            templates = product_templates.get(category.ct_name, ["Generic Product"] * 20)
            
            for i, template in enumerate(templates[:20], 1):
                # Generate realistic prices
                base_price = random.randint(50, 5000)
                mrp = Decimal(str(base_price))
                discount_percent = random.randint(5, 40)
                dis_price = mrp * (100 - discount_percent) / 100
                
                product = Product(
                    pdt_name=f"{template} {random.choice(['Pro', 'Plus', 'Max', 'Elite', 'Premium', 'Standard', 'Basic', 'Deluxe'])}",
                    pdt_mrp=mrp,
                    pdt_dis_price=dis_price,
                    pdt_qty=random.randint(10, 100),
                    ct=category
                )
                all_products.append(product)
        
        # Bulk create all products
        with transaction.atomic():
            Product.objects.bulk_create(all_products, batch_size=50)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(categories)} categories and {len(all_products)} products!'
            )
        )
        
        # Print summary
        for category in categories:
            count = Product.objects.filter(ct=category).count()
            self.stdout.write(f'{category.ct_name}: {count} products')
