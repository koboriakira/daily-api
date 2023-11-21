from pydantic import BaseModel
from typing import Optional
from datetime import date as DateObject
from datetime import timedelta
from abc import abstractmethod

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


class RecursiveCondition(BaseModel):
    """ RecursiveCondition is a class that represents recursive condition.
    """
    next_date: Optional[DateObject] = None
    cond_text: Optional[str] = None
    is_valid: bool = False

    @staticmethod
    def of(cond_text: Optional[str] = None, date: Optional[DateObject] = None) -> 'RecursiveCondition':
        """ of is a factory method that returns RecursiveCondition instance.
        """
        if cond_text is None:
            return RecursiveCondition()
        cond_text = cond_text.lower()
        if cond_text.endswith("days"):
            return RecursiveConditionDays.of(cond_text=cond_text, date=date)
        if cond_text.startswith("next"):
            return RecursiveConditionNextDate.of(cond_text=cond_text, date=date)

    def get_next_date(self) -> DateObject:
        return self.next_date

class RecursiveConditionNextDate(RecursiveCondition):
    """ RecursiveConditionNextDate is a class that represents recursive condition for next date.
    """
    next_date: DateObject
    @staticmethod
    def of(cond_text: str, date: DateObject) -> 'RecursiveConditionNextDate':
        """ of is a factory method that returns RecursiveConditionNextDate instance.
        """
        next_recursive_cond  = cond_text.replace("next", "").strip()

        # next_recursive_confが数値だった場合
        if next_recursive_cond.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").isdecimal():
            # 次の月のn日
            n = next_recursive_cond.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
            next_date = DateObject(year=date.year, month=date.month + 1, day=int(n))
            return RecursiveConditionNextDate(is_valid=True, cond_text=cond_text, next_date=next_date)

        # next_recursive_condが曜日だった場合
        if next_recursive_cond in DAYS:
            # 次のn曜日
            next_date = _get_next_weekday(date, next_recursive_cond)
            return RecursiveConditionNextDate(is_valid=True, cond_text=cond_text, next_date=next_date)


class RecursiveConditionDays(RecursiveCondition):
    """ RecursiveConditionDays is a class that represents recursive condition for days.
    """
    @staticmethod
    def of(cond_text: str, date: DateObject) -> 'RecursiveConditionDays':
        """ of is a factory method that returns RecursiveConditionDays instance.
        """
        days = cond_text.replace("days", "").strip()
        next_date = date + timedelta(days=int(days))
        return RecursiveConditionDays(is_valid=True, cond_text=cond_text, next_date=next_date)


def _get_next_weekday(date: DateObject, day: str) -> DateObject:
    """ 指定された日付以降の、指定された曜日に該当する最も近い日付を計算する """
    day_index = DAYS.index(day)
    target_date = date
    while True:
        target_date = target_date + timedelta(days=1)
        if target_date.weekday() == day_index:
            return target_date
    # ↓ ありえないけど一応
    return None
