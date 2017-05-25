import pandas as pd
from make_dir import cmd_folder

train = pd.read_csv(cmd_folder + '/data/inter/train.csv')
test = pd.read_csv(cmd_folder + '/data/inter/test.csv')

media_profile = pd.read_csv(cmd_folder + '/data/raw/media_profile.csv')
music_infos = pd.read_csv(cmd_folder + '/data/raw/infos_musics.csv')

media_profile = pd.merge(music_infos,media_profile,on="media_id",how="outer")

media_profile["lyrics_explicits"] = media_profile["lyrics_explicits"].astype(float)

media_profile.loc[media_profile.loc[:,"release_date"]==30000101,"release_date"]=np.nan

media_profile["release_date"] = pd.to_datetime(media_profile["release_date"],format="%Y%m%d")

media_profile.loc[(media_profile["release_date"].dt.year<1960),"release_period"]="before 60s"
media_profile.loc[(media_profile["release_date"].dt.year>=1960) & (media_profile["release_date"].dt.year<1980),"release_period"]="60s - 80s"
media_profile.loc[(media_profile["release_date"].dt.year>=1980) & (media_profile["release_date"].dt.year<2010),"release_period"]="80s - 2010s"
media_profile.loc[(media_profile["release_date"].dt.year>=2010),"release_period"]="after 2010s"

media_profile = media_profile.merge(train[["media_id","is_listened"]].groupby("media_id").mean().reset_index(),on="media_id",how="outer")
media_profile.rename(columns={'is_listened':'mean_media_is_listened'},inplace=True)

media_profile["bpm_multiple_60"] = (((media_profile["bpm"] %60)<2) | ((media_profile["bpm"] %60)>58)).astype(float)

media_profile.drop("release_date",axis=1,inplace=True)

media_profile.to_csv(cmd_folder + '/data/inter/media_profile.csv',index=False)
