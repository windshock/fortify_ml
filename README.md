Fortify의 Data Flow 데이터를 이용하여 약점 군집화하기
========
Fortify를 이용하여 취약점을 분석하면 수많은 발견사항으로 인해 수많은 시간이 소요된다. 수작업 분석 과정 중 일부라도 자동화할 수 있다면 해당 시간은 단축될 수 있다. Data Flow 유사성 판단을 자동화하여 기존 수작업 분석 시간을 1/3로 단축할 수 있는 방법을 찾아보았다.
# Fortify에서 수작업 분석 방법
Fortify 분석 결과를 수작업 분석 시 전체 코드를 모두 보면 많은 시간이 소요되어, Data flow 유사성을 참고하여 취약 여부를 판단하곤 한다.
사람의 판단에 의해 Data Flow의 유사성을 구분하는 것이 아니라 통계기법(kmeans)를 이용하여 기계적으로 구분하는 방법을 적용해보았다.
# Data Flow 데이터 추출
[Fortify SSC의 API](https://github.com/fortify/ssc-restapi-client)를 이용하면 Fortify의 Data Flow 데이터를 추출할 수 있으며, 취약점 유형 중 XSS를 대상으로 테스트하였다.
[Fortify의 TraceNode Data](https://github.com/fortify/ssc-restapi-client/blob/master/docs/TraceNodeDto.md) 중에서  데이터 중 nodeType, text만 추출하여 아래와 같이 데이터를 구성한다. 2개의 프로젝트에서 XSS와 관련된 Data flow만 추출(파일 [fortify_ml.xlsx](./data/fortify_ml.xlsx), [fortify_ml2.xlsx](./data/fortify_ml2.xlsx))하였고, 수작업으로 확인한 취약여부 데이터를 추가하였다. (file경로와 이름은 군집화하는 것에 도움이 안되는 것으로 경험 상 판단했다.)
```text
EXTERNAL_ENTRY Spring Method Mapping URL 
IN_CALL savePointJsonp(2)
IN_OUT_CALL getCallback(this : return)
RETURN Return
```
# Kmeans의 k값 결정
Fortify에 의해 발견된 취약점 중 1/3의 수를 K값으로 하면 최근 3개의 프로젝트에서 수작업으로 분류한 타입과 가장 유사하게 분류가능한 k값이 되었다.
# 한계점
위와 같은 방식으로 업무를 진행하면 아래와 같은 경우에서 오탐 케이스가 발생할 수 있다.
- Data Flow 분석만으로는 취약하나,javascript 실행 불가한 response type(json 등)이라 xss에 안전하다고 판단할 경우
- Fortify가 인지하지 못하는 sanitizer를 사용
# 관련 연구
[joern doc](https://fabs.codeminers.org/papers/2011-woot.pdf), [joern code](https://github.com/octopus-platform/joern-tools/blob/master/tools/ml/joern-knn), [joern video](https://www.youtube.com/watch?v=Uy2FrUmO-2E) : 각 함수에서 사용한 API Symbol(Topic)의 사용 패턴을 분석하고, 확인된 취약점과 근거리의 함수를 취약점 후보로 분석함
# 기타
knn 알고리즘 설명 : https://kkokkilkon.tistory.com/14,  https://tariat.tistory.com/37
kmeans 알고리즘 설명 : https://lovit.github.io/nlp/machine%20learning/2018/03/21/kmeans_cluster_labeling/