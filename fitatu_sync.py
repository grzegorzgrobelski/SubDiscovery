from datetime import datetime
from db_service import DbService
from fitatu_helper import FitatuHelper


class FitatuSync:

    @staticmethod
    def _macros_changed(new, old):
        if not old:
            return True

        fields = ["energy", "protein", "fat", "carbohydrate", "fiber", "sugars", "salt"]

        for f in fields:
            if float(new.get(f, 0)) != float(old.get(f, 0)):
                return True

        return False

    @staticmethod
    def _is_new_day(db_row):
        if not db_row:
            return True

        created = db_row.get("created_at")
        if not created:
            return True

        return created != datetime.now().date()

    @staticmethod
    def sync_today():
        print("🔄 Sync macros...")

        new_macros = FitatuHelper.get_today_macros()
        last = DbService.get_latest_daily_macros()

        # nowy dzień
        if FitatuSync._is_new_day(last):
            print("📅 Nowy dzień → zapis")
            DbService.add_daily_macros(**new_macros)
            return

        # zmiana wartości
        if FitatuSync._macros_changed(new_macros, last):
            print("📊 Zmiana wartości → update")
            DbService.add_daily_macros(**new_macros)
        else:
            print("✅ Brak zmian")