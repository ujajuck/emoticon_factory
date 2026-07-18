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

---

## Repository Layout

```text
emoticon_factory/
├── docs/
├── app/
├── agents/
├── graphs/
├── schemas/
├── workflows/
├── assets/
├── projects/
└── tests/
```

---

## LangGraph Layout

```text
CEO
 ├── market_research
 ├── concept_planning
 ├── character_generation
 ├── pose_generation
 ├── layer_design
 ├── rigging
 ├── animation
 └── qa
```

---

## State Model

```python
state = {
    'project_id': str,
    'current_phase': str,
    'owner_directives': {},
    'locked_fields': [],
    'pending_decisions': [],
    'artifacts': [],
    'retry_counts': {},
}
```

---

## Mandatory Documents

- docs/architecture.md
- docs/setup.md
- docs/log.md

모든 구조 변경은 위 문서를 먼저 수정한 뒤 구현한다.
