# kubeflow-xgboost-recommendation

이전 롯데멤버스 추천시스템 구현 공모전에서 받은 데이터와 추천시스템을 구현하기 위해 Faiss(유사도), GRU4REC(session based recommandatein), XGBoost, DNN 등 몇가지 알고리즘을 테스트 해보았었는데 GRU4REC와 XGBOOST의 TOP1의 정확도가 상당히 비슷하게 나와서
XGBOOST를 이용해서 추천시스템을 구현하는 것을 Kubeflow pipeline을 활용해서 로컬에서 구축
<br>
<br>
# Train pipeline

![스크린샷 2022-09-24 18-31-09](https://user-images.githubusercontent.com/64409693/192091058-85401691-add5-41f9-910b-f350f83f2f0e.png)
<br>
1. convert-data : AWS S3에서 CSV 다운 후 json으로 변환
2. preprocess-data : 불필요한 데이터 삭제 및 merge
3. spilt-data : train, val, test data로 분할
4. train-model : xgboost 학습
5. test-model : 학습된 모델 성능 측정
6. extract-top5-10 : 상위 5, 10 추론 정확도 측정
<br>
<br>

# ISSUE <br>

##### 1. XGBoost로 bagging 시도
https://github.com/kch8906/kubeflow-xgboost-recommendation/issues/1#issue-1368873179

##### 2. 정확도 향상 (softprob)
https://github.com/kch8906/kubeflow-xgboost-recommendation/issues/2#issue-1368887131

##### 3. kubeflow pipeline csv 데이터 문제 
https://github.com/kch8906/kubeflow-xgboost-recommendation/issues/3#issue-1369218180


# schedule

##### 1. Train 노드 gpu 할당
##### 2. Mlflow 및 Seldon-core로 모델 serving
##### 3. 프로메테우스, 그라파나로 리소스 모니터링
##### 4. Github Actions CI/CD
##### 5. Feast(가능할지 미지수 - 데이터 마켓 필요)
