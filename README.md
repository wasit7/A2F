# A2F
grading report

#setup Excel file
The input Excel must has ID and Name in first two columns. Sub-tasks columns must be in the following format:
1. header is "subtask_maxscore_weightedscore", maxscore and weightedscorea are numbers
2. students score must not exceed maxscore
3. Sum of all weightedscores must be 100
#policy
When the number of sutendent in a class is less than 10. The grades are calculated from fixed boundaries:

80.000 < B+ <= 85.000
70.000 < B <= 80.000
60.000 < C+ <= 70.000
50.000 < C <= 60.000
45.000 < D+ <= 50.000
40.000 < D <= 45.000
00.000 < F <= 40.000

When the class is larger than or equal 10 students. The weighted score will be converted to T-score as following steps:
1. find mean (mu) and std (sigma) of the scores of the class
2. calculate T-score by using T=(x-mu)/sigma*10+70
3. Then the T-score will be bisected into grades using the same boundaries as in the fixed grading
