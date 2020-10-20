import datetime as dt
import json


class Preprocesser:
    def __init__(self, tweets_dataframe=None):
        if tweets_dataframe is None:
            raise TypeError
        self.tweets_dataframe = tweets_dataframe

    def simple_mean(self,to_json):
        tweets_dataframe = round(self.tweets_dataframe[["neg_sent", "pos_sent", "comp_sent", "polarity"]].mean(), 3)
        if to_json:
            return list(map(lambda x: json.dumps(x.tolist()),tweets_dataframe.values))
        else:
            return tweets_dataframe

    def top_10_retweets_mean(self):
        return round(self.tweets_dataframe.sort_values(by="retweets", ascending=False)[:10].mean()[["neg_sent", "pos_sent", "comp_sent", "polarity"]], 3)

    def by_date_mean(self, unix, to_json):
        tweets_dataframe_by_dates = self.tweets_dataframe[(self.tweets_dataframe["date"] + dt.timedelta(days=7)).dt.date >= dt.date.today()]
        tweets_dataframe_by_dates["date"] = tweets_dataframe_by_dates["date"].dt.floor("d")

        tweets_dataframe_by_dates = round(tweets_dataframe_by_dates[["date", "neg_sent", "pos_sent", "comp_sent", "polarity"]].groupby("date", axis=0, as_index=False).mean(), 3)
        if unix:
            tweets_dataframe_by_dates["date"] = tweets_dataframe_by_dates["date"].view('int64')/1e6
        if to_json:
            return json.dumps(tweets_dataframe_by_dates.to_dict())
        else:
            return tweets_dataframe_by_dates

