# ue-cli spec
---

## Group 1: HTTP 직통 (18개)

### 씬 조작 (10개)

| 기능 | 엔드포인트 | 호출 대상 |
|------|-----------|-----------|
| 액터 목록 | `PUT /object/call` | `EditorLevelLibrary.GetAllLevelActors()` |
| 액터 검색 | `PUT /object/call` | 위 결과를 필터링 |
| 액터 생성 | `PUT /object/call` | `EditorLevelLibrary.SpawnActorFromClass()` |
| 액터 삭제 | `PUT /object/call` | `EditorLevelLibrary.DestroyActor()` |
| Transform 변경 | `PUT /object/property` | WRITE_ACCESS |
| 프로퍼티 조회 | `PUT /object/describe` | 스키마 전체 |
| 프로퍼티 수정 | `PUT /object/property` | WRITE_ACCESS |
| BP 스폰 | `PUT /object/call` | `SpawnActorFromObject()` |
| 뷰포트 이동 | `PUT /object/call` | `SetViewportLocation()` |
| 스크린샷 | `PUT /object/call` | `AutomationBlueprintFunctionLibrary` |

### BP 프로퍼티 (8개)

| 기능 | 엔드포인트 | 호출 대상 |
|------|-----------|-----------|
| 컴포넌트 프로퍼티 | `PUT /object/property` | 컴포넌트 objectPath |
| 물리 설정 | `PUT /object/property` | BodyInstance |
| BP 컴파일 | `PUT /object/call` | `KismetEditorUtilities.CompileBlueprint()` |
| BP 프로퍼티 수정 | `PUT /object/property` | CDO objectPath |
| Pawn 프로퍼티 | `PUT /object/property` | Pawn 설정 |
| 메시/머티리얼 할당 | `PUT /object/property` | StaticMesh/Material |
| BP 액터 스폰 | `PUT /object/call` | `SpawnActorFromObject()` |
| BP 기본값 수정 | `PUT /object/property` | CDO 기본값 |

---

## Group 2: Python Script 경유 (16개)

실행 경로: `PUT /object/call` → `ExecutePythonScript()` → UE 내장 Python (unreal 모듈)

### BP 생성 (2개)

| 기능 | 스크립트 | unreal 모듈 |
|------|----------|-------------|
| BP 생성 | `scripts/create_bp.py` | `BlueprintFactory` → `AssetTools.create_asset()` |
| 컴포넌트 추가 | `scripts/add_component.py` | `SubobjectDataSubsystem` |

### BP 노드 그래프 (8개)

| 기능 | 스크립트 | unreal 모듈 |
|------|----------|-------------|
| 이벤트 노드 | `scripts/node_event.py` | `BlueprintEditorLibrary` |
| 함수 호출 노드 | `scripts/node_function.py` | `BlueprintEditorLibrary` |
| 변수 선언 | `scripts/node_variable.py` | `BlueprintEditorLibrary` |
| 입력 액션 노드 | `scripts/node_input.py` | `BlueprintEditorLibrary` |
| Self 레퍼런스 | `scripts/node_self.py` | `BlueprintEditorLibrary` |
| 컴포넌트 Getter | `scripts/node_component.py` | `BlueprintEditorLibrary` |
| 노드 핀 연결 | `scripts/node_connect.py` | `BlueprintEditorLibrary` |
| 노드 검색 | `scripts/node_find.py` | `BlueprintEditorLibrary` |

### UMG (6개)

| 기능 | 스크립트 | unreal 모듈 |
|------|----------|-------------|
| 위젯 BP 생성 | `scripts/umg_create.py` | `WidgetBlueprintFactory` |
| 텍스트 블록 추가 | `scripts/umg_text.py` | `WidgetTree` |
| 버튼 추가 | `scripts/umg_button.py` | `WidgetTree` |
| 뷰포트 표시 | `scripts/umg_viewport.py` | `WidgetTree` |
| 이벤트 바인딩 | `scripts/umg_event.py` | `WidgetTree` |
| 텍스트 바인딩 | `scripts/umg_text_bind.py` | `WidgetTree` |

### 프로젝트 (1개)

| 기능 | 스크립트 | unreal 모듈 |
|------|----------|-------------|
| 입력 매핑 추가 | `scripts/input_mapping.py` | `InputSettings` |
