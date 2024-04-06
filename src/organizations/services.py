from django.contrib.gis.geos.point import Point

from .repositories import LocationRepository, OrganizationRepository, CategoryRepository


MAPPING_DATA = {
    'alpine_hut': 'Домики в горах',
    'apartment': 'Апартаменты',
    'aquarium': 'Океанариумы',
    'artwork': 'Паблик-арты',
    'attraction': 'Достопримечательности',
    'camp_pitch': 'Места для палатки',
    'camp_site': 'Кемпинги',
    'caravan_site': 'Караванинги',
    'chalet': 'Коттеджи',
    'gallery': 'Художественные галереи',
    'guest_house': 'Гостевые дома',
    'hostel': 'Хостелы',
    'hotel': 'Отели',
    'information': 'Информационные центры',
    'motel': 'Мотели',
    'museum': 'Музеи',
    'wilderness_hut': 'Лесные домики',
    'zoo': 'Зоопарки',
    'beach': 'Пляжи',
    'fuel': 'Заправки',
    'parking': 'Парковки',
    'restaurant': 'Рестораны',
    'picnic_site': 'Места для пикника',
    'viewpoint': 'Смотровые площадки',
    'shop': 'Магазины',
    'winery': 'Винодельни',
    'brewery': 'Пивоварни',
    'bicycle_rental': 'Места с арендой велосипедов',
    'theme_park': 'Парки аттракционов',
    'farm': 'Фермы',
    'trail_riding': 'Ранчо',
    'charging_station': 'Зарядные станции'
}


def parse_organizations_to_db(data):
    for k in data.keys():
        for obj in data[k]:
            try:
                OrganizationRepository.create(
                    location=LocationRepository.get_or_create(
                        coords=Point(obj['latitude'], obj['longitude']),
                        address=obj['address']
                    ),
                    name=obj['name'],
                    phone=obj['phone'],
                    website=obj['website'],
                    description=obj['description'],
                    category=CategoryRepository.get_by_name(MAPPING_DATA[obj['category']])
                )
            except Exception:
                pass
