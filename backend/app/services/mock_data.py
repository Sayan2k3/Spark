"""
Mock data for phones with detailed specifications and reviews
"""

def get_mock_products():
    """Get list of phones with detailed specs and reviews"""
    return [
        {
            'id': 1,
            'name': 'iPhone 13',
            'price': 29999,
            'originalPrice': 34999,
            'rating': 4.5,
            'reviews_count': 2847,
            'category': 'electronics',
            'specifications': {
                'display': '6.1 inch Super Retina XDR OLED',
                'processor': 'Apple A15 Bionic',
                'ram': '6GB',
                'storage': '128GB',
                'main_camera': '12MP Dual Camera',
                'battery': '3227 mAh',
                'os': 'iOS 15'
            },
            'reviews': [
                {'text': 'Amazing camera quality! The photos are crisp and clear even in low light. Battery life easily lasts the whole day.', 'rating': 5},
                {'text': 'Good phone but battery drains fast when gaming. Camera is excellent for photography.', 'rating': 4},
                {'text': 'Superb performance and the camera is just outstanding. Battery life is decent.', 'rating': 5},
                {'text': 'Camera quality is phenomenal. Battery could be better but overall great phone.', 'rating': 4}
            ]
        },
        {
            'id': 2,
            'name': 'OnePlus 11',
            'price': 28999,
            'originalPrice': 32999,
            'rating': 4.3,
            'reviews_count': 1923,
            'category': 'electronics',
            'specifications': {
                'display': '6.7 inch AMOLED 120Hz',
                'processor': 'Snapdragon 8 Gen 2',
                'ram': '8GB',
                'storage': '128GB',
                'main_camera': '50MP Triple Camera',
                'battery': '5000 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': 'Blazing fast performance! Gaming is smooth. Battery lasts 1.5 days with moderate use.', 'rating': 5},
                {'text': 'Excellent battery life and super fast charging. Camera is good but not the best.', 'rating': 4},
                {'text': 'Best battery life in this range. Camera quality is decent. Great for gaming.', 'rating': 4},
                {'text': 'Performance is top-notch. Battery easily lasts all day. Camera could be improved.', 'rating': 4}
            ]
        },
        {
            'id': 3,
            'name': 'Samsung Galaxy S23',
            'price': 35999,
            'originalPrice': 39999,
            'rating': 4.6,
            'reviews_count': 3214,
            'category': 'electronics',
            'specifications': {
                'display': '6.1 inch Dynamic AMOLED 2X 120Hz',
                'processor': 'Snapdragon 8 Gen 2',
                'ram': '8GB',
                'storage': '256GB',
                'main_camera': '50MP Triple Camera',
                'battery': '3900 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': 'Compact and powerful! Camera is exceptional. Battery life is good for a small phone.', 'rating': 5},
                {'text': 'Amazing display and camera. Battery life could be better but fast charging helps.', 'rating': 4},
                {'text': 'Best camera in this size. Performance is excellent. Battery is adequate.', 'rating': 5},
                {'text': 'Premium build quality. Camera is fantastic. Gaming performance is smooth.', 'rating': 5}
            ]
        },
        {
            'id': 4,
            'name': 'Xiaomi 13 Pro',
            'price': 24999,
            'originalPrice': 29999,
            'rating': 4.2,
            'reviews_count': 1567,
            'category': 'electronics',
            'specifications': {
                'display': '6.73 inch AMOLED 120Hz',
                'processor': 'Snapdragon 8 Gen 2',
                'ram': '12GB',
                'storage': '256GB',
                'main_camera': '50MP Leica Camera',
                'battery': '4820 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': 'Leica camera is amazing! Professional quality photos. Battery life is excellent.', 'rating': 5},
                {'text': 'Great value for money. Camera quality is superb. Battery easily lasts all day.', 'rating': 4},
                {'text': 'Performance is smooth. Camera with Leica is outstanding. Good battery backup.', 'rating': 4},
                {'text': 'Best camera phone under 30k. Gaming is smooth. Battery charging is super fast.', 'rating': 5}
            ]
        },
        {
            'id': 5,
            'name': 'iPhone 15 Pro',
            'price': 45999,
            'originalPrice': 49999,
            'rating': 4.8,
            'reviews_count': 4521,
            'category': 'electronics',
            'specifications': {
                'display': '6.1 inch Super Retina XDR OLED 120Hz',
                'processor': 'Apple A17 Pro',
                'ram': '8GB',
                'storage': '256GB',
                'main_camera': '48MP Triple Camera',
                'battery': '3274 mAh',
                'os': 'iOS 17'
            },
            'reviews': [
                {'text': 'Pro camera features are incredible! Battery life improved from last year. Gaming is phenomenal.', 'rating': 5},
                {'text': 'Best iPhone camera ever. Performance is unmatched. Battery life is good not great.', 'rating': 5},
                {'text': 'Action button is useful. Camera quality is professional grade. Battery could be better.', 'rating': 4},
                {'text': 'Titanium build feels premium. Camera is exceptional. Gaming performance is console-like.', 'rating': 5}
            ]
        },
        {
            'id': 6,
            'name': 'Google Pixel 7',
            'price': 22999,
            'originalPrice': 27999,
            'rating': 4.4,
            'reviews_count': 1832,
            'category': 'electronics',
            'specifications': {
                'display': '6.3 inch AMOLED 90Hz',
                'processor': 'Google Tensor G2',
                'ram': '8GB',
                'storage': '128GB',
                'main_camera': '50MP Dual Camera',
                'battery': '4355 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': 'Best camera AI! Photos come out perfect every time. Battery life is impressive.', 'rating': 5},
                {'text': 'Google software is smooth. Camera is exceptional. Battery lasts all day easily.', 'rating': 5},
                {'text': 'Camera magic eraser is amazing. Performance is good. Battery life is solid.', 'rating': 4},
                {'text': 'Pure Android experience. Camera quality is top-notch. Gaming is decent.', 'rating': 4}
            ]
        },
        {
            'id': 7,
            'name': 'Realme GT 3',
            'price': 19999,
            'originalPrice': 24999,
            'rating': 4.1,
            'reviews_count': 1245,
            'category': 'electronics',
            'specifications': {
                'display': '6.74 inch AMOLED 144Hz',
                'processor': 'Snapdragon 8+ Gen 1',
                'ram': '8GB',
                'storage': '128GB',
                'main_camera': '50MP Triple Camera',
                'battery': '4600 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': '240W charging is insane! Full charge in 10 minutes. Gaming performance is excellent.', 'rating': 5},
                {'text': 'Best gaming phone under 20k. Battery charges super fast. Camera is decent.', 'rating': 4},
                {'text': '144Hz display is smooth. Performance for gaming is top tier. Camera could be better.', 'rating': 4},
                {'text': 'Fastest charging ever! Gaming is buttery smooth. Battery life is good.', 'rating': 4}
            ]
        },
        {
            'id': 8,
            'name': 'Vivo X90',
            'price': 31999,
            'originalPrice': 35999,
            'rating': 4.3,
            'reviews_count': 987,
            'category': 'electronics',
            'specifications': {
                'display': '6.78 inch AMOLED 120Hz',
                'processor': 'MediaTek Dimensity 9200',
                'ram': '8GB',
                'storage': '256GB',
                'main_camera': '50MP Zeiss Camera',
                'battery': '4810 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': 'Zeiss camera is brilliant! Night photography is excellent. Battery backup is great.', 'rating': 5},
                {'text': 'Camera quality with Zeiss is professional. Performance is smooth. Battery lasts long.', 'rating': 4},
                {'text': 'Best camera phone for photography enthusiasts. Gaming is good. Battery life impressive.', 'rating': 5},
                {'text': 'Display is gorgeous. Camera quality is exceptional. Battery easily lasts a day.', 'rating': 4}
            ]
        },
        {
            'id': 9,
            'name': 'Nothing Phone 2',
            'price': 27999,
            'originalPrice': 31999,
            'rating': 4.0,
            'reviews_count': 756,
            'category': 'electronics',
            'specifications': {
                'display': '6.7 inch OLED 120Hz',
                'processor': 'Snapdragon 8+ Gen 1',
                'ram': '8GB',
                'storage': '128GB',
                'main_camera': '50MP Dual Camera',
                'battery': '4700 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': 'Unique design with glyph interface! Performance is smooth. Battery life is decent.', 'rating': 4},
                {'text': 'Clean software experience. Camera is good. Battery lasts all day with moderate use.', 'rating': 4},
                {'text': 'Glyph lights are actually useful. Gaming performance is good. Camera quality is decent.', 'rating': 4},
                {'text': 'Design stands out. Performance for daily use is great. Battery could be better.', 'rating': 3}
            ]
        },
        {
            'id': 10,
            'name': 'Oppo Find X6',
            'price': 33999,
            'originalPrice': 37999,
            'rating': 4.4,
            'reviews_count': 1123,
            'category': 'electronics',
            'specifications': {
                'display': '6.74 inch AMOLED 120Hz',
                'processor': 'Snapdragon 8 Gen 2',
                'ram': '12GB',
                'storage': '256GB',
                'main_camera': '50MP Hasselblad Camera',
                'battery': '4800 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': 'Hasselblad camera is phenomenal! Colors are natural and beautiful. Battery life excellent.', 'rating': 5},
                {'text': 'Camera quality is professional grade. Fast charging is super quick. Gaming is smooth.', 'rating': 5},
                {'text': 'Best camera colors. Performance is flagship level. Battery backup is impressive.', 'rating': 4},
                {'text': 'Premium build and camera. Display is vibrant. Battery easily lasts full day.', 'rating': 4}
            ]
        },
        {
            'id': 11,
            'name': 'Motorola Edge 40',
            'price': 23999,
            'originalPrice': 27999,
            'rating': 4.1,
            'reviews_count': 645,
            'category': 'electronics',
            'specifications': {
                'display': '6.55 inch pOLED 144Hz',
                'processor': 'MediaTek Dimensity 8020',
                'ram': '8GB',
                'storage': '256GB',
                'main_camera': '50MP Dual Camera',
                'battery': '4400 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': 'Curved display feels premium. Performance is snappy. Battery life is good.', 'rating': 4},
                {'text': 'Clean Android experience. Camera quality is decent. Gaming at 144Hz is smooth.', 'rating': 4},
                {'text': 'Lightweight and slim. Battery charges fast. Camera could be better in low light.', 'rating': 4},
                {'text': 'Good value for money. Display is excellent. Battery lasts a full day.', 'rating': 4}
            ]
        },
        {
            'id': 12,
            'name': 'Asus ROG Phone 7',
            'price': 38999,
            'originalPrice': 42999,
            'rating': 4.5,
            'reviews_count': 432,
            'category': 'electronics',
            'specifications': {
                'display': '6.78 inch AMOLED 165Hz',
                'processor': 'Snapdragon 8 Gen 2',
                'ram': '16GB',
                'storage': '512GB',
                'main_camera': '50MP Triple Camera',
                'battery': '6000 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': 'Ultimate gaming beast! 165Hz display is incredible. Battery lasts forever even while gaming.', 'rating': 5},
                {'text': 'Best gaming phone period. Performance is unmatched. Battery life is exceptional.', 'rating': 5},
                {'text': 'Gaming triggers are amazing. Camera is surprisingly good. Battery is massive.', 'rating': 5},
                {'text': 'Perfect for mobile gaming. Display quality is top notch. Battery easily lasts 2 days.', 'rating': 4}
            ]
        },
        {
            'id': 13,
            'name': 'Honor 90',
            'price': 21999,
            'originalPrice': 25999,
            'rating': 4.2,
            'reviews_count': 534,
            'category': 'electronics',
            'specifications': {
                'display': '6.7 inch AMOLED 120Hz',
                'processor': 'Snapdragon 7 Gen 1',
                'ram': '8GB',
                'storage': '256GB',
                'main_camera': '200MP Triple Camera',
                'battery': '5000 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': '200MP camera is insane! Details are incredible. Battery life is excellent.', 'rating': 5},
                {'text': 'Great display and camera. Performance is good for daily use. Battery lasts long.', 'rating': 4},
                {'text': 'Camera quality especially in daylight is amazing. Gaming is decent. Battery backup solid.', 'rating': 4},
                {'text': 'Value for money. Camera is the highlight. Battery easily gets through the day.', 'rating': 4}
            ]
        },
        {
            'id': 14,
            'name': 'Sony Xperia 1 V',
            'price': 41999,
            'originalPrice': 45999,
            'rating': 4.3,
            'reviews_count': 234,
            'category': 'electronics',
            'specifications': {
                'display': '6.5 inch 4K OLED 120Hz',
                'processor': 'Snapdragon 8 Gen 2',
                'ram': '12GB',
                'storage': '256GB',
                'main_camera': '48MP Triple Camera',
                'battery': '5000 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': '4K display is stunning! Professional camera features. Battery life has improved a lot.', 'rating': 5},
                {'text': 'Best display on any phone. Camera manual controls are pro level. Battery is good.', 'rating': 4},
                {'text': 'Audiophile dream phone. Display and camera are exceptional. Gaming is smooth.', 'rating': 5},
                {'text': 'Unique 21:9 aspect ratio. Camera quality is superb. Battery lasts all day now.', 'rating': 4}
            ]
        },
        {
            'id': 15,
            'name': 'Poco F5',
            'price': 18999,
            'originalPrice': 22999,
            'rating': 4.0,
            'reviews_count': 2134,
            'category': 'electronics',
            'specifications': {
                'display': '6.67 inch AMOLED 120Hz',
                'processor': 'Snapdragon 7+ Gen 2',
                'ram': '8GB',
                'storage': '256GB',
                'main_camera': '64MP Triple Camera',
                'battery': '5000 mAh',
                'os': 'Android 13'
            },
            'reviews': [
                {'text': 'Best performance under 20k! Gaming is smooth at high settings. Battery life is great.', 'rating': 4},
                {'text': 'Value for money king. Performance punches above its weight. Battery lasts long.', 'rating': 4},
                {'text': 'Great for gaming on budget. Display is good. Camera is average but battery is solid.', 'rating': 4},
                {'text': 'Fast and smooth. Good for daily use and gaming. Battery backup is impressive.', 'rating': 4}
            ]
        }
    ]