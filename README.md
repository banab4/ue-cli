# ue-cli
---

Unreal Engine Editor를 AI 에이전트가 제어하기 위한 스킬 + 명세.

UE 내장 Remote Control API (HTTP :30010)를 통해 에디터를 조작한다.

## 구조

```
ue-cli/
├── README.md
├── SKILL.md               # 에이전트용 스킬 (설치 대상)
├── spec.md                # CLI 명세 (34개 커맨드)
└── scripts/               # Group 2 Python 템플릿
```

## 설치

```bash
npx skills add https://github.com/banab4/ue-cli
```

## 요구사항

- Unreal Engine 5.x (에디터 실행 중)
- `Web Remote Control` 플러그인 활성화
- `Python Editor Script Plugin` 활성화 (Group 2 사용 시)

## 아키텍처

```
에이전트 → SKILL.md 읽기 → spec.md fetch → HTTP 요청 구성 → UE Editor (:30010)
```

- **Group 1** (18개): HTTP 직통 — endpoint + parameter로 직접 호출
- **Group 2** (16개): HTTP → `ExecutePythonScript()` — Python 템플릿을 문자열로 전송
