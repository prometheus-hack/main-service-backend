from django.contrib.gis.geos.point import Point
from django.conf import settings
import requests

from business.repositories import QRCodeUsingRepository
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
                        coords=Point(float(obj['latitude']), float(obj['longitude'])),
                        address=obj['street'] + obj['housenumber']
                    ),
                    name=obj['name'],
                    phone=obj['phone'],
                    website=obj['website'],
                    description=obj['description'],
                    category=CategoryRepository.get_by_name(MAPPING_DATA[obj['category']])
                )
            except Exception:
                pass


def send_locations_to_recommend_service():
    for org in OrganizationRepository.all():
        requests.post(url=settings.RECOMMEND_BASE_API_URL + 'add_location/', data={
            "location_id": org.location.pk,
            "category_id": org.category.pk,
            "latitude": org.location.coords[0],
            "longitude": org.location.coords[1]
        })


def get_recommendation(user, now_location):
    data = []
    for org_id in QRCodeUsingRepository.get_organizations(user).values_list('organization__pk', flat=True):
        organization = OrganizationRepository.get(org_id)
        data.append({
            "location_id": organization.location.pk,
            "category_id": organization.category.pk,
            "latitude": organization.location.coords[0],
            "longitude": organization.location.coords[1]
        })
    if now_location:
        data.append({
            "location_id": -1,
            "category_id": -1,
            "latitude": now_location[0],
            "longitude": now_location[1]
        })
    requests.post(url=settings.RECOMMEND_BASE_API_URL + '', data=data)
