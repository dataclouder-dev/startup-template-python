import pandas as pd

from app.modules.mongo.mongo import db


def normalize_column(df: pd.DataFrame, column: str, remove_original_column: bool = False) -> pd.DataFrame:
    """Normalizes a column that contains Json objects
    returns a new dataframe with the objects as columns.
    example, is col1 contains objects like this {"a": 1, "b": 2}
    return return separated value in ["col1_a", "col1_b"]
    """
    if column in df.columns:
        try:
            normalized_data = pd.json_normalize(df[column], sep="_")
            normalized_data = normalized_data.add_prefix(f"{column}_")

            denormalized_df = pd.concat([df, normalized_data], axis=1)

            if remove_original_column:
                denormalized_df = denormalized_df.drop(column, axis=1)

            return denormalized_df
        except Exception as e:
            print(f"Not able to normalize_column {column} check if need to create table instead", e)
            return df
    else:
        return df


def get_data_from_tiktoks(user_id: str) -> list[dict]:
    tiktoks = list(db["tiktoks_aweme"].find({"author.unique_id": user_id}))

    df = pd.DataFrame(tiktoks)

    df = normalize_column(df, "statistics")

    # Convert create_time to Mexico City Time
    df["create_time"] = pd.to_datetime(df["create_time"], unit="s").dt.tz_localize("UTC")
    df["create_time"] = df["create_time"].dt.tz_convert("America/Mexico_City")  # This is Central Time
    df["create_time"] = df["create_time"].dt.tz_localize(None)  # remove timezone

    # Additional timing analysis
    df["cat_hour"] = df["create_time"].dt.hour
    df["cat_day_of_week"] = df["create_time"].dt.day_name()

    # Calculate engagement metrics
    df["statistics_engagement"] = (
        df["statistics_comment_count"]  # Comments
        + df["statistics_digg_count"]  # Likes
        + df["statistics_share_count"]  # Total shares
        + df["statistics_whatsapp_share_count"]  # WhatsApp shares
        + df["statistics_collect_count"]  # Saves/Collections
        + df["statistics_repost_count"]  # Reposts
    ) / df["statistics_play_count"]  # Divided by views

    columns_for_frontend = [
        "aweme_id",
        "statistics_comment_count",
        "statistics_digg_count",
        "statistics_download_count",
        "statistics_play_count",
        "statistics_share_count",
        "statistics_forward_count",
        "statistics_lose_count",
        "statistics_lose_comment_count",
        "statistics_whatsapp_share_count",
        "statistics_collect_count",
        "statistics_repost_count",
        "statistics_engagement",
        "create_time",
        "cat_hour",
        "cat_day_of_week",
    ]

    return df[columns_for_frontend].to_dict(orient="records")
