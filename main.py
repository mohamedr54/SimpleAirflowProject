

url = "https://api.open-meteo.com/v1/forecast"
parameters = { "latitude" : 34.668138,
           "longitude" : 104.16580199999999,
           "temperature_unit" : "celsius",
           "wind_speed_unit" : "kmh",
           "precipitation_unit" :"mm",
           "hourly": ["temperature_2m", "cloud_cover", "wind_speed_10m", "wind_speed_80m", "wind_direction_10m",
                      "wind_direction_80m", "snowfall", "precipitation_probability"],
           "daily": ["temperature_2m_max", "temperature_2m_min", "daylight_duration", "uv_index_max", "uv_index_clear_sky_max",
                     "wind_direction_10m_dominant", "rain_sum", "precipitation_sum", ] }




