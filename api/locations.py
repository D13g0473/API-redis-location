from client_redis import r
from geopy.distance import geodesic

# Grupos de interés válidos
VALID_GROUPS = [
    "cervecerias",
    "universidades",
    "farmacias",
    "emergencias",
    "supermercados"
]

def add_location(group, name, longitude, latitude):
    if group not in VALID_GROUPS:
        raise ValueError("Grupo inválido")
    key = f"poi:{group}"
    return r.geoadd(key, (longitude, latitude, name))

def get_nearby(group, longitude, latitude, radius_km=5):
    key = f"poi:{group}"
    return r.georadius(key, longitude, latitude, radius_km, unit='km', withdist=True, withcoord=True)

def get_distance(group, loc1, loc2):
    key = f"poi:{group}"
    return r.geodist(key, loc1, loc2, unit='km')

def save_user_location(user_id, longitude, latitude):
    key = "user_location"
    r.geoadd(key, (longitude, latitude, user_id))

def get_distance_between_user_and_place(user_id, place_name, group):
    user_key = f"user_location"
    place_key = f"poi:{group}"
    # obtenemos la ubicación del usuario
    user_location = r.geopos(user_key, user_id)
    if not user_location or user_location[0] is None:
        return None
    user_lon, user_lat = user_location[0]

    # obtenemos la ubicación del lugar
    place_location = r.geopos(place_key, place_name)
    if not place_location or place_location[0] is None:
        return None

    place_lon, place_lat = place_location[0]

    # calculamos distancia manual
    from geopy.distance import geodesic
    distance = geodesic((user_lat, user_lon), (place_lat, place_lon)).km

    return distance

def get_all_places(group):
    key = f"poi:{group}"
    names = r.zrange(key, 0, -1)
    places = []

    for name in names:
        pos = r.geopos(key, name)
        if pos and pos[0]:  # Puede venir None si no hay coordenadas
            lon, lat = pos[0]
            places.append({
                "name": name,
                "lon": float(lon),
                "lat": float(lat)
            })

    return places
