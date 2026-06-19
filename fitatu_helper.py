import json
from datetime import date

from Fitatu.auth import FitatuAuthContext
from Fitatu.client import FitatuApiClient
from Fitatu.facade import FitatuLibrary


class FitatuHelper:

    @staticmethod
    def _load_session_data(filename="session_data.json"):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except Exception as e:
            print("❌ Nie udało się wczytać pliku:", e)
            return None

    @staticmethod
    def get_today_macros(session_file="session_data.json"):
        session_data = FitatuHelper._load_session_data(session_file)

        if not session_data:
            raise RuntimeError("Brak session_data")

        auth = FitatuAuthContext.from_session_data(session_data)
        client = FitatuApiClient(auth=auth)  # opcjonalne, ale zostawiłem

        lib = FitatuLibrary(session_data=session_data)

        macros = lib.get_day_macros_via_api(
            target_date=date.today(),
            include_meal_breakdown=True,
        )

        return macros["result"]["totals"]