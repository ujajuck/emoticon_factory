# Project Log

## 2026-07-18

### Decisions

- Framework를 ADK에서 LangGraph로 변경.
- 프로젝트 방향을 '인간 사장 승인형 이모티콘 제작 회사'로 확정.
- 문서 중심 개발 방식을 채택.
- 주요 기술·제품·운영 결정은 `docs/decision_log.md`에 별도 누적하기로 확정.

### Created

- docs/architecture.md
- docs/setup.md
- docs/log.md
- docs/decision_log.md

### Updated

- 의사결정 기록 템플릿 추가.
- D-001: LangGraph 기반 워크플로 채택.
- D-002: 인간 사장을 최종 의사결정자로 유지.

### Next Tasks

1. 프로젝트 스캐폴딩.
2. LangGraph `ProjectState` 모델 구현.
3. owner directive schema 정의.
4. 승인 게이트 상태 전이표 설계.
5. 체크포인터 및 영속 저장소 후보 비교.
6. MVP 워크플로 구현.

---

규칙:

- 기능 추가, 수정, 검증 결과는 이 파일에 날짜별로 기록한다.
- 중요한 설계 변경은 `docs/decision_log.md`에 결정 ID와 함께 기록한다.
- 기존 결정을 변경할 때는 기록을 삭제하지 않고 superseded 관계를 남긴다.
