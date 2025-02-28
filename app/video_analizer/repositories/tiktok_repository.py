from bson import ObjectId
from dataclouder_core.models.models import FiltersConfig

# from app.tiktoks.models.tiktok_model import tiktokModel
from app.modules.mongo.mongo import db

col_name = "tiktoks_aweme"


def find_tiktoks(id: str) -> dict:
    """Get words"""
    collection = db[col_name]
    result = collection.find_one({"_id": ObjectId(id)})

    return result


def find_filtered_tiktoks(filters: FiltersConfig) -> list:
    """Get words"""
    print(filters)
    collection = db[col_name]
    result = collection.find(filters.model_dump())
    return result


# def save_tiktok(tiktok: tiktokModel) -> tiktokModel:
#     """Save tiktok insert if not exists, or update if exists"""
#     collection = db[col_name]
#     print("antes de insertar")
#     result = collection.find_one_and_replace({"_id": ObjectId()}, tiktok.model_dump(), upsert=True, return_document=True)
#     result["_id"] = str(result["_id"])
#     return result


# def delete_tiktok(id: str) -> tiktokModel:
#     """Delete tiktok"""
#     collection = db[col_name]
#     collection.delete_one({"_id": ObjectId(id)})
#     return {"message": "tiktok deleted"}


def get_author_post_counts() -> list:
    """
    Get the count of posts per author using their unique_id.
    Returns a list of dictionaries containing author unique_id and their post count.
    """
    collection = db[col_name]
    pipeline = [{"$group": {"_id": "$author.unique_id", "count": {"$sum": 1}}}]
    result = list(collection.aggregate(pipeline))
    return result


def get_posts_by_day_of_week() -> dict:
    """
    Get the count of posts grouped by day of week in a format suitable for Chart.js
    Returns a dictionary with labels and data arrays for easy frontend charting
    """
    collection = db[col_name]
    pipeline = [
        {
            "$addFields": {
                "dayOfWeek": {
                    "$dayOfWeek": "$create_time"  # 1 for Sunday through 7 for Saturday
                }
            }
        },
        {"$group": {"_id": "$dayOfWeek", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]

    result = list(collection.aggregate(pipeline))

    # Map MongoDB's dayOfWeek (1-7, Sunday=1) to more readable names
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # Initialize counts for all days (even if they have 0 posts)
    day_counts = {day: 0 for day in days}

    # Fill in the actual counts
    for entry in result:
        day_index = entry["_id"] - 1  # Convert 1-7 to 0-6 index
        day_counts[days[day_index]] = entry["count"]

    # Structure the data for Chart.js
    chart_data = {"labels": days, "datasets": [{"label": "Posts per Day of Week", "data": [day_counts[day] for day in days]}]}

    return chart_data


def get_comprehensive_analytics() -> dict:
    """
    Get comprehensive TikTok analytics including post distribution by day,
    boolean field statistics, and numeric field summaries.
    Returns a structured dictionary suitable for multiple Chart.js visualizations.
    """
    collection = db[col_name]

    # Get total document count for percentage calculations
    total_docs = collection.count_documents({})

    # Boolean fields analysis
    boolean_fields_pipeline = [
        {
            "$group": {
                "_id": None,
                "is_delete_false": {"$sum": {"$cond": [{"$eq": ["$is_delete", False]}, 1, 0]}},
                "allow_share_true": {"$sum": {"$cond": [{"$eq": ["$allow_share", True]}, 1, 0]}},
                "allow_comment_true": {"$sum": {"$cond": [{"$eq": ["$allow_comment", True]}, 1, 0]}},
                "is_private_false": {"$sum": {"$cond": [{"$eq": ["$is_private", False]}, 1, 0]}},
                "with_goods_false": {"$sum": {"$cond": [{"$eq": ["$with_goods", False]}, 1, 0]}},
                "in_reviewing_false": {"$sum": {"$cond": [{"$eq": ["$in_reviewing", False]}, 1, 0]}},
                "self_see_false": {"$sum": {"$cond": [{"$eq": ["$self_see", False]}, 1, 0]}},
                "is_prohibited_false": {"$sum": {"$cond": [{"$eq": ["$is_prohibited", False]}, 1, 0]}},
            }
        }
    ]

    # Numeric fields analysis
    numeric_fields_pipeline = [
        {"$group": {"_id": None, "private_status": {"$push": "$private_status"}, "reviewed": {"$push": "$reviewed"}, "download_status": {"$push": "$download_status"}}}
    ]

    # Execute pipelines
    boolean_results = list(collection.aggregate(boolean_fields_pipeline))[0]
    numeric_results = list(collection.aggregate(numeric_fields_pipeline))[0]

    # Get posts by day of week (reusing existing function)
    posts_by_day = get_posts_by_day_of_week()

    # Structure all data for frontend
    analytics_data = {
        "totalPosts": total_docs,
        "booleanFields": {
            "labels": [
                "Is Delete (False)",
                "Allow Share (True)",
                "Allow Comment (True)",
                "Is Private (False)",
                "With Goods (False)",
                "In Reviewing (False)",
                "Self See (False)",
                "Is Prohibited (False)",
            ],
            "datasets": [
                {
                    "label": "Boolean Fields Distribution",
                    "data": [
                        boolean_results["is_delete_false"],
                        boolean_results["allow_share_true"],
                        boolean_results["allow_comment_true"],
                        boolean_results["is_private_false"],
                        boolean_results["with_goods_false"],
                        boolean_results["in_reviewing_false"],
                        boolean_results["self_see_false"],
                        boolean_results["is_prohibited_false"],
                    ],
                }
            ],
        },
        "numericFields": {
            "privateStatus": {"labels": ["Value 0"], "datasets": [{"label": "Private Status Distribution", "data": [numeric_results["private_status"].count(0)]}]},
            "reviewed": {
                "labels": ["Value 0", "Value 1"],
                "datasets": [{"label": "Reviewed Status Distribution", "data": [numeric_results["reviewed"].count(0), numeric_results["reviewed"].count(1)]}],
            },
            "downloadStatus": {"labels": ["Value 0"], "datasets": [{"label": "Download Status Distribution", "data": [numeric_results["download_status"].count(0)]}]},
        },
        "postsByDayOfWeek": posts_by_day,
    }

    return analytics_data
