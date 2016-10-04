"""DOC STRING."""
import pandas as pd
import cPickle as pickle


def pickleIder(df):
    """DOC STRING."""
    ider = dict(zip(df['hike_name'], df['hike_id']))
    with open('pickle/ider.pkl', 'wb') as fid:
        pickle.dump(ider, fid)


if __name__ == '__main__':
    df = pd.read_csv('data/washington_hikes_clean_noout.csv')
    df['hike_id'] = range(len(df))
    pickleIder(df)
    print "Identifier pickled"
    df.to_csv('data/washington_hikes_clean_noout.csv', index_col=0)
