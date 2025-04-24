from geopy.geocoders import Nominatim

def get_coordinates_from_postal_code(postal_code, city_name=None):
    geolocator = Nominatim(user_agent="formasmat_app")
    try:
        location = geolocator.geocode(f"{postal_code} {city_name}")
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass
    return None, None
import math

def haversine1(lat1, lon1, lat2, lon2):
    """
    Calcule la distance en kilomètres entre deux points donnés par 
    leur latitude et leur longitude avec la formule de Haversine.
    """
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
