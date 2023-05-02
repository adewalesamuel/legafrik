from sqlalchemy.orm import Query

def paginate(query: Query, page=1, pagesize=10) -> dict:
    if page is None or page == "" or int(page) == 0: page = 1

    paginated_query = query.offset((int(page) - 1) * pagesize).limit(pagesize).all()

    return {
        'result': paginated_query, 
        'total': query.count(), 
        'page': int(page), 
        'pagesize': len(paginated_query)
        }