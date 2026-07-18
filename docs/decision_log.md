# Architecture Decision Log

이 문서는 프로젝트의 주요 기술·제품·운영 결정을 기록한다. 단순 진행 상황은 `docs/log.md`에 기록하고, 향후 구조와 구현 방향에 영향을 주는 결정은 이 문서에 남긴다.

## 작성 규칙

- 결정 ID는 `D-001`, `D-002` 형식으로 순차 증가한다.
- 상태는 `proposed`, `accepted`, `superseded`, `rejected` 중 하나를 사용한다.
- 기존 결정을 바꾸더라도 삭제하지 않고 새 결정에서 대체 관계를 명시한다.
- 코드 구현 전에 관련 결정을 먼저 추가하거나 갱신한다.
- 영향 범위에는 다시 설계하거나 재생성해야 하는 코드, 문서, 자산을 명시한다.

## Decision Template

```yaml
decision_id: D-XXX
title: 결정 제목
status: proposed | accepted | superseded | rejected
date: YYYY-MM-DD

context:
  - 결정을 필요로 한 배경

options:
  - 검토한 선택지

decision:
  - 최종 선택

reason:
  - 선택 근거

impact:
  architecture:
    - 구조 영향
  implementation:
    - 구현 영향
  operations:
    - 운영 영향
  documents:
    - 갱신 대상 문서

follow_up:
  - 후속 작업

supersedes: null
superseded_by: null
```

---

## D-001 — LangGraph 기반 워크플로 채택

```yaml
decision_id: D-001
title: LangGraph 기반 워크플로 채택
status: accepted
date: 2026-07-18

context:
  - 이모티콘 제작 과정은 다단계 생성, 검수, 재작업, 인간 승인 분기를 포함한다.
  - 프로젝트 소유자인 인간 사장이 중간 결과를 선택, 수정, 잠금, 반려할 수 있어야 한다.
  - ADK 사용 경험에서 상태 관리, 반복 호출, 컨텍스트 누적, 부모-서브 에이전트 복귀 제어에 불편이 있었다.

options:
  - Google ADK
  - LangGraph
  - 자체 Python 상태 머신

decision:
  - 워크플로 오케스트레이션 기반으로 LangGraph를 사용한다.
  - FastAPI 또는 CLI 같은 외부 인터페이스는 LangGraph 실행 계층과 분리한다.

reason:
  - 명시적인 상태 객체와 조건부 엣지를 이용해 승인·반려·재작업 흐름을 표현하기 쉽다.
  - 체크포인트와 실행 재개 구조를 인간 승인 대기 상태에 적용할 수 있다.
  - 그래프 노드와 도메인 서비스를 분리하여 테스트할 수 있다.
  - 특정 에이전트 프레임워크에 업무 로직이 종속되는 것을 줄일 수 있다.

impact:
  architecture:
    - 모든 제작 단계는 LangGraph node 또는 독립 domain service로 정의한다.
    - 인간 승인 단계는 interrupt 가능한 approval gate로 모델링한다.
    - 프로젝트 상태는 단일 typed state schema로 관리한다.
  implementation:
    - graphs, nodes, state, services 디렉터리 경계를 정의해야 한다.
    - 체크포인터와 영속 저장소를 선정해야 한다.
    - 승인 대기 후 실행 재개 테스트가 필요하다.
  operations:
    - 실행 ID와 project ID를 연결해 추적해야 한다.
    - 승인 대기 중 프로세스 재시작을 견딜 수 있어야 한다.
  documents:
    - docs/architecture.md
    - docs/setup.md
    - docs/log.md

follow_up:
  - ProjectState 초안 정의
  - owner directive schema 정의
  - approval gate 인터페이스 설계
  - 체크포인터 후보 비교

supersedes: null
superseded_by: null
```

---

## D-002 — 인간 사장을 최종 의사결정자로 유지

```yaml
decision_id: D-002
title: 인간 사장을 최종 의사결정자로 유지
status: accepted
date: 2026-07-18

context:
  - 캐릭터 종, 콘셉트, 팔레트, 대표 동작과 출시 여부는 품질 점수만으로 결정할 수 없다.
  - 자동 모드가 기본이어도 사용자가 언제든 방향을 지정하고 결과를 잠글 수 있어야 한다.

options:
  - 완전 자동 생성
  - 모든 단계 수동 승인
  - 위험도와 중요도에 따른 선택적 승인

decision:
  - 기본 운영 방식은 자동 생성 후 핵심 단계에서 인간 승인을 받는 혼합 모드로 한다.
  - 인간이 잠근 필드는 후속 AI 노드가 변경할 수 없다.
  - AI 팀장 검수는 인간 승인을 대체하지 않고 판단 자료만 제공한다.

reason:
  - 브랜드 취향과 출시 전략은 정량 평가만으로 대체하기 어렵다.
  - 초기 대표 시안 검수 후 대량 확장하는 방식이 재작업 비용을 줄인다.
  - 사용자 개입을 예외 처리로 두지 않고 시스템의 정상 흐름으로 포함할 수 있다.

impact:
  architecture:
    - owner_directives, locked_fields, pending_decisions가 ProjectState 핵심 필드가 된다.
    - 승인 결과는 승인자, 시각, 선택, 코멘트와 함께 기록한다.
  implementation:
    - approve, reject, revise, regenerate, lock 명령이 필요하다.
    - 잠금 충돌 시 자동 진행하지 않고 owner_decision_required 상태로 전환한다.
  operations:
    - 승인 대기 프로젝트를 조회하는 인터페이스가 필요하다.
    - 승인 이력과 산출물 버전을 연결해야 한다.
  documents:
    - docs/architecture.md
    - docs/log.md

follow_up:
  - 승인 게이트 상태 전이표 작성
  - owner directive JSON Schema 작성
  - 대표 4종 승인 후 나머지 세트 확장 정책 정의

supersedes: null
superseded_by: null
```
