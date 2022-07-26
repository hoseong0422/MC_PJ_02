# 내가 검색한 맛집이 진짜일까?
멀티캠퍼스 국비지원 데이터 사이언스/엔지니어 2번째 프로젝트로
엔지니어 분반을 선택 후 Apache Spark, Apache Airflow, Apache Kafka에 대해 배운 후
최대한 배운 내용을 프로젝트에 적용해 보려했습니다.

## 주제 선정 이유
- 우리는 부모님의 생신, 연인과의 기념일 등 특별한 날에 좋은 곳에서 식사하기 위해 맛집을 검색합니다. 하지만 막상 찾아보면 내가 찾아본 곳이 광고가 아닌 진짜 맛집인가하는 의구심을 품게 되고 직접 먹어보기 전까지는 정확하게 알 수가 없습니다. 그래서 맛집을 찾기 위해 우리가 어디에 검색해보는 것이 좋은 방법일지 찾아보기 위해 이 주제를 선정하였습니다.

## 담당 파트
- [인스타그램 크롤러 제작](https://github.com/hoseong0422/MC_PJ_02/blob/master/codes/insta_v2.py)
- Twitter API와 Apache Kafka를 이용한 실시간 피드 수집
  - [producer](https://github.com/hoseong0422/MC_PJ_02/blob/master/codes/kafka_producer.py)
  - [consumer](https://github.com/hoseong0422/MC_PJ_02/blob/master/codes/kafka_consumer.py)
- [Apache Spark를 이용한 Data Mart 구축](https://github.com/hoseong0422/MC_PJ_02/blob/master/codes/transform_and_analiysis.ipynb)
- [각 사이트별 상,하위 20개 식당 분석 및 전체 사이트별 평점 분포 분석](https://github.com/hoseong0422/MC_PJ_02/blob/master/codes/transform_and_analiysis.ipynb)

프로젝트 상세 정리 [노션](https://field-nerve-7fd.notion.site/df90cc1c05de4f61a5e1a43cb07d4c88) 페이지