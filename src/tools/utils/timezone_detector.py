import pytz
from geopy import Nominatim
from datetime import datetime
from requests import get
from timezonefinder import TimezoneFinder


def get_utc_offset(location):
    geolocator = Nominatim(user_agent="get_timezone")
    loc = geolocator.geocode(location)
    time_finder = TimezoneFinder()

    if loc is None:
        return None

    lat, long = loc.latitude, loc.longitude
    country_code = time_finder.timezone_at(lng=long, lat=lat)

    try:
        if country_code == "Etc/GMT":
            # Handle GMT as UTC
            return 0
        else:
            # Get the UTC offset for the location
            timezone_info = pytz.timezone(country_code)
            utc_offset = (
                timezone_info.utcoffset(datetime.now()).total_seconds() / 3600.0
            )
            return utc_offset
    except KeyError:
        # No timezone found
        return None


# Example usage:
def get_differance(loc):
    try:
        utc_offset = get_utc_offset(loc)
        if utc_offset is not None:
            yerevan = 4
            if utc_offset >= yerevan:
                return f"Yerevan +{utc_offset-yerevan}"
            elif utc_offset <= 0:
                return f"Yerevan -{-1*utc_offset + yerevan}"
            elif utc_offset < yerevan:
                return f"Yerevan -{yerevan - utc_offset}"
            else:
                return "Yerevan"
        return " "
    except:
        return " "