import pandas as pd
votes_finaux = pd.read_excel('votes_finaux.xlsx')
all_votes = pd.read_excel('votes.xlsx')
votes_finaux_result_1 = votes_finaux.iloc[: , 13:]
all_votes_result_1 = all_votes.iloc[: , 12:]
votes_finaux_id = votes_finaux.iloc[: , 8]
all_votes_id = all_votes.iloc[: , 7]
votes_finaux_result = pd.concat([votes_finaux_id, votes_finaux_result_1],axis=1)
all_votes_result = pd.concat([all_votes_id, all_votes_result_1],axis=1)
votes_finaux_result.to_excel('votes_finaux_result.xlsx')
all_votes_result.to_excel('all_votes_result.xlsx')
#print(votes_finaux_result)


