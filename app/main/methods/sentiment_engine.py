from flask import current_app


def analyze_sentiments(tweets_df):
    if tweets_df is None:
        return None
    if current_app.config['USE_MODEL']:
        from app import clp

        scores = clp.pipeline.predict_proba(tweets_df["text"])

        tweets_df["neg_sent"], tweets_df["pos_sent"],  = scores[:, 0], scores[:, 1]
        tweets_df["comp_sent"] = tweets_df["pos_sent"]-tweets_df["neg_sent"]
        tweets_df["polarity"] = tweets_df["comp_sent"].abs()
        for i in range(len(tweets_df)):
            print("--------------------")
            print("---TWEET TEXT : ---")
            print(tweets_df.iloc[i]["text"])
            print("---SENT ML: ---")
            print(tweets_df.iloc[i]["comp_sent"])
    else:
        from app import sia
        import numpy as np

        scores = list(map(sia.polarity_scores, tweets_df["text"]))
        scores = np.asarray(list(map(lambda x: list(x.values()), scores)))
        tweets_df["neg_sent"], tweets_df["pos_sent"], tweets_df["comp_sent"] = scores[:, 0], scores[:, 2], scores[:, 3]
        tweets_df["polarity"] = tweets_df["comp_sent"].abs()
        tweets_df = tweets_df[tweets_df["comp_sent"] != 0]

    return tweets_df


