from pytrends.request import TrendReq  # type: ignore


class GoogleTrendsMonitor:
    MAX_KEYWORDS = 5  # Google Trends API limitation

    def __init__(self, hl: str = "en-US", tz: int = 360) -> None:
        """
        Initialize the Google Trends monitor
        hl: language (default 'en-US')
        tz: timezone offset (default 360 - US CST)
        """
        self.pytrends = TrendReq(hl=hl, tz=tz)

    def get_trending_searches(self, country: str = "united_states") -> list[str] | None:
        """Get daily trending searches for a specific country"""
        try:
            trending_searches = self.pytrends.trending_searches(pn=country)
            return trending_searches
        except Exception as e:
            print(f"Error getting trending searches: {e}")
            return None

    def monitor_keywords(self, keywords: list[str], timeframe: str = "today 3-m", geo: str = "", cat: int = 0) -> dict | None:
        """
        Monitor specific keywords over time
        keywords: list of keywords to monitor (max 5 keywords due to Google's limit)
        timeframe: time frame to analyze (default: last 3 months)
        geo: geographic location (default: worldwide)
        cat: category (default: 0 - all categories)
        """
        if len(keywords) > self.MAX_KEYWORDS:
            print(f"Warning: Google Trends only allows up to {self.MAX_KEYWORDS} keywords. Using first {self.MAX_KEYWORDS}.")
            keywords = keywords[: self.MAX_KEYWORDS]

        try:
            # Build the payload
            self.pytrends.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo)

            # Get interest over time
            interest_over_time = self.pytrends.interest_over_time()

            # Get related queries
            related_queries = self.pytrends.related_queries()

            return {"interest_over_time": interest_over_time, "related_queries": related_queries}
        except Exception as e:
            print(f"Error monitoring keywords: {e}")
            return None

    def get_realtime_trends(self, keywords: list[str], lookback_hours: int = 4) -> dict | None:
        """
        Get real-time trending data for keywords
        keywords: list of keywords to monitor
        lookback_hours: number of hours to look back (default: 4)
        """
        results = {}
        timeframe = f"now {lookback_hours}-H"

        try:
            data = self.monitor_keywords(keywords, timeframe=timeframe)
            if data and "interest_over_time" in data:
                results["trend_data"] = data["interest_over_time"]

                # Calculate basic statistics
                for keyword in keywords:
                    if keyword in data["interest_over_time"]:
                        series = data["interest_over_time"][keyword]
                        results[keyword] = {"mean": series.mean(), "max": series.max(), "min": series.min(), "current": series.iloc[-1] if not series.empty else None}
            return results
        except Exception as e:
            print(f"Error getting realtime trends: {e}")
            return None


def main() -> None:
    # Example usage
    monitor = GoogleTrendsMonitor()

    # Get trending searches
    print("Daily Trending Searches:")
    trending = monitor.get_trending_searches()
    if trending is not None:
        print(trending.head())

    # Monitor specific keywords
    keywords = ["python programming", "javascript", "data science"]
    print(f"\nMonitoring keywords: {keywords}")
    results = monitor.monitor_keywords(keywords)
    if results:
        print("\nInterest over time:")
        print(results["interest_over_time"].tail())

    # Get realtime trends
    print("\nRealtime trends:")
    realtime_data = monitor.get_realtime_trends(keywords)
    if realtime_data:
        print(realtime_data)


if __name__ == "__main__":
    main()
