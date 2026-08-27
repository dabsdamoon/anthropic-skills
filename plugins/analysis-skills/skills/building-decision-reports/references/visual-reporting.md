# Visual Reporting Rules

차트의 목적은 장식이 아니라 `표를 읽지 않아도 관계를 정확히 이해하게 하는 것`이다.

## 1. 메시지에 맞는 형태를 고른다

| 질문 | 권장 형태 | 주의 |
|---|---|---|
| 구성비 | 정렬 막대, 필요하면 파이 | 파이는 조각이 명시적 분모를 구성할 때만 |
| 월별 변화 | 라인 또는 단일 막대 | 모든 점 라벨보다 끝점·변곡점 라벨 우선 |
| 두 계열 비교 | 묶음 막대 | 범례 필수, 범례 순서와 막대 순서 일치 |
| 규모가 크게 다른 계열 | 독립 패널 | 패널마다 축 범위를 명시 |
| 목표 대비 실제 | 막대 + 목표선 | 실제와 계획의 시각 문법을 구분 |
| 흐름·정의 정정 | 간단한 플로차트 | 숫자 비교 차트의 대체재로 쓰지 않음 |

파이는 사용자 요청을 존중하되 다음 조건을 확인한다.

- 합이 하나의 명시적 분모가 되는가
- 조각 수가 적고 차이가 충분히 큰가
- 각 조각에 범주명, 값과 비율을 직접 붙일 공간이 있는가
- 고객군 중복이 있으면 `고유 사람 비중`으로 오해하지 않도록 분모를 캡션에 쓰는가

## 2. 제목·부제·본문의 역할을 나눈다

- **제목:** 독자가 기억해야 할 결론. 예: `산전·산후가 접점의 82.6%를 차지합니다`
- **부제:** Figure 번호, 지표, 대상, 기간, 중복·분모 조건
- **차트:** 비교와 패턴
- **자료:** 원파일, 테이블, URL
- **주의:** 중복, 축 차이, 계획값, 미반영 비용 등 오독 방지 정보

`고객군별 현황`처럼 결론이 없는 제목을 피한다. 반대로 제목에서 인과를 주장하려면 실제
설계가 인과를 지지해야 한다.

## 3. 라벨과 범례

### 단일 계열

범례를 만들지 않는다. 막대·선 가까이에 값이나 계열명을 직접 쓴다. 평균선이나 목표선은
한 번만 직접 라벨하고 같은 숫자를 축, 범례와 주석에 반복하지 않는다.

### 다중 계열

- 모든 계열을 색상표와 텍스트 범례로 식별한다.
- 범례 순서를 막대의 왼쪽→오른쪽 또는 선의 시각적 순서와 맞춘다.
- 계열명이 범례에만 있고 값이 어느 막대인지 모호하면 막대 배치를 바꾸거나 직접 라벨한다.
- 값 라벨에는 단위를 붙이거나 Y축·부제에서 단위를 한 번 명확히 선언한다.

### 값 라벨

- 막대가 적은 경영 리포트에서는 모든 막대의 정확한 값을 표시해도 좋다.
- 값이 많으면 시작·끝·최대·최소·의사결정 임계값만 표시한다.
- 동일한 숫자가 우연히 반복되더라도 각각 어느 범주에 속하는지 위치와 계열이 분명해야 한다.
- 소수점 자릿수는 의사결정 정밀도보다 많게 쓰지 않는다.

## 4. 축, 패널과 색

- 막대축은 원칙적으로 0에서 시작한다.
- Y축 제목에 단위를 쓴다.
- 서로 규모가 크게 달라 작은 계열이 사라지면 독립 패널로 나눈다.
- 독립 패널은 축이 다르다는 사실을 부제와 캡션에 쓴다.
- 같은 의미의 계열은 문서 전체에서 같은 색을 유지한다.
- 핵심 계열에 강한 색, 비교 계열에 덜 강한 색을 쓴다.
- 빨강·초록만으로 상태를 구분하지 말고 텍스트, 위치 또는 패턴을 함께 쓴다.
- 장식용 3D, 그림자, 그라디언트와 과도한 격자선을 피한다.

## 5. Markdown용 SVG

정밀한 레이아웃이 필요한 숫자 차트는 SVG가 유용하다.

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 1000 600"
     role="img"
     aria-labelledby="title desc">
  <title id="title">차트의 핵심 주제</title>
  <desc id="desc">주요 값과 관계를 설명하는 대체텍스트</desc>
  <rect width="1000" height="600" fill="#ffffff"/>
  <!-- chart -->
</svg>
```

- 고정 픽셀 `width`·`height`보다 `viewBox`로 반응형 표시를 허용한다.
- 외부 웹폰트에 의존하지 않고 시스템 한글 폰트 대체 목록을 둔다.
- Markdown에는 의미 있는 alt text와 상대경로를 쓴다.
- 자산 경로는 `report.md` 기준으로 확인한다.
- Mermaid는 흐름도에는 적합하지만 정밀한 숫자 라벨·범례 배치가 필요한 차트에는 쓰지 않는다.

## 6. 렌더링 검수

SVG를 PNG나 브라우저 화면으로 실제 렌더링한다. 다음 실패를 눈으로 찾는다.

1. 최대 막대의 값이 상단 밖으로 나감
2. 평균·목표선과 값 라벨이 겹침
3. 범례가 없거나 색과 계열명이 매칭되지 않음
4. 같은 숫자가 두 번 찍혀 어느 값인지 모호함
5. 긴 한글 범주명이 잘림
6. 패널의 서로 다른 축을 같은 척도로 오해하게 함
7. 밝은 배경에서 색 대비가 약함
8. 차트 값, 본문과 표의 값이 다름

소스 수정 후 반드시 다시 렌더링한다. 화면을 보지 않은 수정은 검수가 아니다.

## 참고 지침

- [UK Government Analysis Function: Data visualisation charts](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-charts/)
- [UK Government Analysis Function: Publishing charts](https://analysisfunction.civilservice.gov.uk/support/communicating-analysis/introduction-to-data-visualisation-e-learning/module-10-publishing-charts/)
- [UK Government Analysis Function: Colours in charts](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-colours-in-charts/)
- [Datawrapper: Customizing line charts and direct labels](https://academy.datawrapper.de/article/47-customizing-your-line-chart)
