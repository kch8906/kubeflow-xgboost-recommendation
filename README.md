# kubeflow-xgboost-recommendation

이전 롯데멤버스 추천시스템 구현 공모전에서 받은 데이터와 추천시스템을 구현하기 위해 Faiss(유사도), GRU4REC(session based recommandatein), XGBoost, DNN 등 몇가지 알고리즘을 테스트 해보았었는데 GRU4REC와 XGBOOST의 TOP1의 정확도가 상당히 비슷하게 나와서
XGBOOST를 이용해서 추천시스템을 구현하는 것을 Kubeflow pipeline을 활용해서 로컬에서 구축


# ISSUE
### 해결 ISSUE
##### 1. XGBoost로 bagging 시도
https://github.com/kch8906/kubeflow-xgboost-recommendation/issues/1#issue-1368873179

##### 2. 정확도 향상 (softprob)
https://github.com/kch8906/kubeflow-xgboost-recommendation/issues/2#issue-1368887131

### 미해결 ISSUE
##### 1. kubeflow pipeline csv 데이터 문제 
https://github.com/kch8906/kubeflow-xgboost-recommendation/issues/3#issue-1369218180
