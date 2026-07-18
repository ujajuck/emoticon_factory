# 에이전트 핸드오프 운영 가이드

이 문서는 `README.md`의 제작 파이프라인을 실제 로컬 멀티 에이전트 작업으로 실행할 때 각 단계가 어떤 입력을 받고 어떤 출력을 남겨야 하는지 정의한다. 모든 단계는 `schemas/project.schema.json`을 공통 프로젝트 상태 계약으로 사용한다.

## 공통 원칙

- 모든 에이전트는 작업 시작 시 최신 프로젝트 JSON을 읽고, 자신이 담당하는 필드만 갱신한다.
- 캐릭터 설정서, 기준 이미지, 색상 팔레트, 비율 정보, 브랜드 가이드, 금지 요소 목록은 캐릭터 동일성 유지를 위한 고정 기준으로 취급한다.
- 검수 에이전트가 `approved: false`를 반환하면 담당 팀장은 `feedback`을 이전 단계의 작업 지시로 변환한다.
- 이미지 산출물 경로는 프로젝트 루트 기준 상대 경로로 기록해 로컬 실행 환경 간 이동성을 유지한다.

## 단계별 핸드오프

| 순서 | 담당 | 입력 | 갱신 필드 | 완료 조건 |
| --- | --- | --- | --- | --- |
| 1 | 시장조사 담당 | 프로젝트 목표 | `market_research` | 타깃, 테마, 키워드가 정의됨 |
| 2 | 캐릭터 기획 담당 | `market_research` | `character.name`, `character.species`, `character.personality`, `character.style` | 타깃층에 맞는 캐릭터 정체성이 정의됨 |
| 3 | 색상 팔레트 담당 | `character`, `brand_guide` 초안 | `character.palette` | 메인, 보조, 강조 색상이 HEX로 정의됨 |
| 4 | 기획팀장 | `market_research`, `character`, `brand_guide` | `quality_gates.planning` | 기획 승인 또는 수정 피드백 작성 |
| 5 | 포즈 및 상황 기획 담당 | 승인된 기획 | `emoji_set` | 24~32개 상황과 감정이 생성됨 |
| 6 | 밑그림 담당 | `character`, `emoji_set` | `emoji_set[].assets.sketch` | 모든 항목의 스케치 경로가 기록됨 |
| 7 | 캐릭터 일관성 관리자 | 스케치, 기준 이미지 | `emoji_set[].consistency`, `quality_gates.design` | 비율 편차와 수정 필요 여부가 기록됨 |
| 8 | 선화 담당 | 승인된 스케치 | `emoji_set[].assets.outline`, `emoji_set[].assets.layers` | 외곽선 및 레이어 경로가 기록됨 |
| 9 | 채색 담당 | 레이어, `character.palette` | `emoji_set[].assets.final` | 완성 이미지 경로가 기록됨 |
| 10 | 채색 검수 담당 | 완성 이미지 | `emoji_set[].color_review`, `quality_gates.coloring` | 팔레트, 외곽선, 배경 투명성 검수가 완료됨 |
| 11 | CEO | 모든 산출물 | `project.status` | 최종 패키지 승인 및 상태가 `packaged`로 변경됨 |

## 파일 경로 규칙

권장 산출물 구조는 다음과 같다.

```text
projects/{project_slug}/
├── project.json
├── references/
│   └── base.png
├── sketches/
│   └── emoji-01.png
├── layers/
│   └── emoji-01/
│       ├── outline.png
│       ├── body.png
│       ├── face.png
│       ├── accessory.png
│       └── shadow.png
└── final/
    └── emoji-01.png
```

## 재작업 루프

1. 검수 담당자가 실패 항목과 원인을 `feedback` 또는 항목별 review 필드에 기록한다.
2. 팀장은 피드백을 구체적인 재작업 지시로 바꾼다.
3. 담당 제작 에이전트는 기존 산출물을 덮어쓰지 않고 새 버전을 생성한다.
4. 검수 담당자는 최신 버전만 승인 대상으로 삼고 이전 버전은 비교 참고용으로 보존한다.
