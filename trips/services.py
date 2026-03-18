import requests


def validate_artwork(external_id: int) -> bool:
    try:
        response = requests.get(
            f"https://api.artic.edu/api/v1/artworks/{external_id}",
            timeout=10
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False