# Emoticon Factory Architecture

## Vision

Emoticon Factory는 완전 자동 생성기가 아니라 '인간 사장 승인형 이모티콘 제작 회사'를 목표로 한다.

- AI 직원: 조사, 생성, 검수
- 인간 사장: 방향 결정, 승인, 출시
- 프레임워크: LangGraph

---

## Core Principles

1. 모든 중요한 결정은 승인 게이트를 통과한다.
2. 문서는 코드보다 먼저 갱신한다.
3. 모든 산출물은 버전 관리한다.
4. 정적 이모티콘과 애니메이션 이모티콘을 동일 자산 구조로 관리한다.
5. 인간의 개입은 예외가 아니라 정상적인 워크플로 상태로 취급한다.
6. 주요 설계 결정은 삭제하지 않고 결정 로그에 누적한다.

---

## Repository Layout

```text
emoticon_factory/
├── docs/
│   ├── architecture.md
│   ├── decision_log.md
│   ├── log.md
│   └── setup.md
├── app/
├── agents/
├── graphs/
├── nodes/
├── services/
├── schemas/
├── workflows/
├── assets/
├── projects/
└── tests/
```

### Directory Responsibilities

- `docs/`: 구조, 결정, 진행 내역, 설치·실행 방법의 기준 문서.
- `graphs/`: LangGraph 그래프 조립, 조건부 엣지, 실행 진입점.
- `nodes/`: 그래프 노드 함수. 상태를 입력받아 명시적인 변경값만 반환.
- `services/`: 이미지 생성, 시장조사, 파일 저장, 검증 등 프레임워크 독립 업무 로직.
- `agents/`: LLM 역할별 프롬프트, 도구 구성, 출력 계약.
- `schemas/`: 상태, 지시사항, 캐릭터, 자산, 리그, 애니메이션 스키마.
- `workflows/`: 프로젝트 유형별 그래프 설정과 승인 정책.
- `assets/`: 공용 팔레트, 템플릿, 샘플 등 버전 관리 대상 자산.
- `projects/`: 프로젝트별 산출물과 실행 상태. 운영 단계에서는 외부 저장소로 이동 가능.
- `tests/`: 상태 전이, 노드, 서비스, 그래프 통합 테스트.

---

## LangGraph Layout

```text
market_research
        ↓
concept_planning
        ↓
owner_concept_approval
        ↓
character_generation
        ↓
owner_character_approval
        ↓
pose_generation
        ↓
representative_set_approval
        ↓
layer_design
        ↓
rigging
        ↓
animation
        ↓
qa
        ↓
owner_release_approval
        ↓
release
```

AI 팀장 검수 노드는 인간 승인 전에 결과를 평가하고 수정 의견을 생성하지만, 인간의 최종 승인 권한을 대체하지 않는다.

---

## State Model

초기 `ProjectState`는 다음 정보를 가져야 한다.

```python
state = {
    "project_id": str,
    "run_id": str,
    "current_phase": str,
    "status": str,
    "automation_mode": str,
    "owner_directives": {},
    "locked_fields": [],
    "pending_decisions": [],
    "approval_history": [],
    "artifacts": [],
    "retry_counts": {},
    "errors": [],
}
```

### State Rules

- 노드는 전체 상태를 임의로 덮어쓰지 않고 변경 필드만 반환한다.
- 잠긴 필드는 AI 노드가 변경할 수 없다.
- 잠금 충돌이나 필수 승인 누락 시 `owner_decision_required` 상태로 전환한다.
- 승인 대기는 실패가 아니며 체크포인트에서 정상 중단한다.
- 모든 산출물은 생성한 노드, 버전, 입력 지시사항, 승인 상태와 연결한다.

---

## Documentation Policy

### Mandatory Documents

- `docs/architecture.md`: 현재 유효한 시스템 구조와 책임 경계.
- `docs/decision_log.md`: 주요 결정의 배경, 선택지, 영향과 대체 관계.
- `docs/log.md`: 날짜별 구현, 수정, 검증, 문제와 다음 작업.
- `docs/setup.md`: 재현 가능한 설치, 설정, 실행, 테스트 방법.

### Change Procedure

1. 구조 또는 기술 선택이 바뀌면 `decision_log.md`에 결정을 먼저 기록한다.
2. 현재 구조를 `architecture.md`에 반영한다.
3. 설치나 실행 방식이 바뀌면 `setup.md`를 갱신한다.
4. 실제 구현과 검증 결과를 `log.md`에 기록한다.
5. 문서와 코드가 불일치하면 문서가 자동으로 옳다고 가정하지 않고, 결정 로그와 실제 동작을 비교해 불일치를 수정한다.

모든 구조 변경은 위 문서를 먼저 수정한 뒤 구현한다.
