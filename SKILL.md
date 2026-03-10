---
name: ue-cli
version: 0.1.0
description: "Unreal Engine: Control the editor via Remote Control API."
metadata:
  requires:
    plugins: ["Web Remote Control", "Python Editor Script Plugin"]
---
# ue-cli
---

Unreal Engine 에디터를 Remote Control API (HTTP :30010)로 제어하는 스킬.

## 전제 조건

- UE 에디터가 실행 중이어야 한다
- `Web Remote Control` 플러그인이 활성화되어 있어야 한다 (HTTP 서버 :30010)
- Group 2 명령 사용 시 `Python Editor Script Plugin`도 활성화

## 명세

전체 커맨드 명세는 아래 URL에서 fetch한다:

- **spec.md**: `https://raw.githubusercontent.com/banab4/ue-cli/main/spec.md`

## 실행 방법

### Group 1 (HTTP 직통)

spec.md의 endpoint/parameter 정보를 읽고 HTTP 요청을 직접 구성한다.

```
PUT http://localhost:30010/{endpoint}
Content-Type: application/json

{request body}
```

### Group 2 (Python Script 경유)

1. spec.md에서 해당 명령의 스크립트 경로를 확인한다
2. `https://raw.githubusercontent.com/banab4/ue-cli/main/scripts/{script}.py`를 fetch한다
3. 템플릿에 파라미터를 주입한다
4. `ExecutePythonScript()`로 UE에 전송한다:

```
PUT http://localhost:30010/object/call
{
  "objectPath": "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
  "functionName": "ExecutePythonScript",
  "parameters": {
    "PythonScript": "{스크립트 문자열}"
  }
}
```

> [!CAUTION]
> 액터 삭제, 프로퍼티 수정 등 쓰기 명령은 되돌리기가 어렵다 — 사용자 확인 필요.
