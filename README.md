# A2F
grading report

#setup Excel file
The input Excel must has ID and Name in first two columns. Sub-task columns must be in the following format:
<br>1. header is "subtask_maxscore_weightedscore", maxscore and weightedscorea are numbers
<br>2. students score must not exceed maxscore
<br>3. Sum of all weightedscores must be 100
#policy
<p>When the number of sutendents in the class is less than 10. The grades are calculated from fixed boundaries:
<br>80.000 < B+ <= 85.000
<br>70.000 < B <= 80.000
<br>60.000 < C+ <= 70.000
<br>50.000 < C <= 60.000
<br>45.000 < D+ <= 50.000
<br>40.000 < D <= 45.000
<br>00.000 < F <= 40.000

<p>When the class is larger than or equal 10 students. The score will be converted to T-score as following steps:
<br>1. find mean (mu) and std (sigma) of the scores of the class
<br>2. calculate T-score by using T=(x-mu)/sigma*10+70
<br>3. Then the T-score will be bisected into grades using the same boundaries as in the fixed grading
