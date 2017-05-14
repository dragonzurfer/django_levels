def elo_rating(mat):
	n = len(mat[0])
	ratings = []
	for i in range(n):
		ratings.append(1500)
	av_perf = 0
	rounds = len(mat)
	rank_table = {}
	for i in range(n):
			a = [ratings[i]]
			rank_table[i] = a

	for i in range(rounds):

		cur_scores = mat[i]

		score_table = {}
		for i in range(n):
			score_table[i] = cur_scores[i]
		cur_rank = 0
		count = 1

		cur_rating = 1000000
		for k in sorted(rank_table.items(),key = lambda e : e[1][0],reverse = True):
			if(cur_rating> k[1][0]):
				cur_rank = cur_rank + count
				count = 1
				cur_rating = k[1][0]
			else:
				count += 1
			k[1].append(cur_rank)   #1 - cur_rank


		cur_per = 0
		s = [(k,score_table[k]) for k in sorted(score_table,key = score_table.get)]

		for i in range(n):
			k = s[i][0]
			exp_per = (n-rank_table[k][1])*av_perf
			change = (cur_per-exp_per)
			#print(change)
			if(abs(change)>av_perf*(n/2) and av_perf!=0):
				if(change >0):
					change = av_perf*(n/2)
				else:
					change = -1*av_perf*(n/2)
			rank_table[k].append(rank_table[k][0] + change)
			if(i<n-1):
				cur_per += (s[i+1][1] - s[i][1])
		av_perf = cur_per/(n-1)
		#print(av_perf)

		for i in range(n):
			rank_table[i].pop(0)
			rank_table[i].pop(0)
	new_rating = []
	for i in range(n):
		new_rating.append(rank_table[i][0])
	return new_rating
