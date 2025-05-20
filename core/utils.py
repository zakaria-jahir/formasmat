from geopy.geocoders import Nominatim
from django.http import JsonResponse
from functools import wraps

from geopy.geocoders import Nominatim

from geopy.geocoders import Nominatim

def get_coordinates_from_postal_code(postal_code, city_name=None):
    """
    Retourne (latitude, longitude) à partir du code postal et éventuellement du nom de la ville.
    """
    geolocator = Nominatim(user_agent="formasmat_app")
    try:
        if city_name:
            query = f"{postal_code} {city_name}, France"
        else:
            query = f"{postal_code}, France"

        location = geolocator.geocode(query)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass
    return None, None


import math

def haversine1(lat1, lon1, lat2, lon2):

    R = 6371  # Rayon de la Terre en km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
from geopy.geocoders import Nominatim

def get_coordinates_from_address(address, postal_code=None, city=None):
    geolocator = Nominatim(user_agent="formasmat_app")
    try:
        full_address = f"{address}, {postal_code or ''} {city or ''}, France"
        location = geolocator.geocode(full_address.strip())
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print("Erreur géocodage :", e)
    return None, None


def ajax_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'auth_required'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view