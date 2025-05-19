from sqlalchemy import inspect


def row_to_dict(row) -> dict:
    """SQLAchemy 객체를 도메인 객체로 매핑 """
    return {key: getattr(row, key) for key in inspect(row).attrs.keys()}
