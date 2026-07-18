# Setup Guide

## Environment

- Python 3.12+
- uv 또는 pip
- Git

---

## Clone

```bash
git clone https://github.com/ujajuck/emoticon_factory.git
cd emoticon_factory
```

---

## Virtual Environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\\Scripts\\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

---

## Planned Dependencies

```bash
pip install langgraph
pip install langchain
pip install fastapi
pip install uvicorn
pip install pydantic
```

---

## Planned Run Commands

```bash
python app/main.py
```

```bash
uvicorn app.api:app --reload
```

---

## Documentation Policy

1. 구현 전에 architecture.md를 갱신한다.
2. 작업 완료 후 log.md를 갱신한다.
3. 설치 방법 변경 시 setup.md를 갱신한다.
