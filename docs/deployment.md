# AWS 무중단 배포 가이드

## 전체 아키텍처

```
인터넷
  │ 80/443
 ALB  (퍼블릭 서브넷 A/B)
  │ 8000
 ECS - FastAPI  (퍼블릭 서브넷)
  │  ├── EFS 마운트 → ChromaDB 영구 저장
  │ 11434
 EC2 - Ollama  (퍼블릭 서브넷)
```

무중단의 핵심: ALB + ECS 롤링 업데이트.  
신 버전 태스크 healthcheck 통과 → 구 버전 태스크 종료.

---

## 진행 현황

- [x] 1단계: IAM 사용자 생성
- [x] 2단계: VPC 생성
- [x] 3단계: 보안그룹 생성
- [ ] 4단계: EC2 (Ollama 서버)
- [ ] 5단계: ECR + Docker 이미지
- [ ] 6단계: EFS (ChromaDB 영구화)
- [ ] 7단계: ALB + 타겟 그룹
- [ ] 8단계: ECS 클러스터 + 서비스
- [ ] 9단계: GitHub Actions CI/CD

---

## 1단계: IAM 사용자 생성

루트 계정은 MFA 설정 후 잠궈두고, 이후 모든 작업은 IAM 사용자로 진행.

- 루트 계정 → Security credentials → MFA 활성화
- IAM → Users → `doc-qa-deploy` 생성 → `AdministratorAccess` 부여
- IAM 사용자로 재로그인

---

## 2단계: VPC 생성

리전: **서울 (ap-northeast-2)**

| 항목 | 값 | 이유 |
|---|---|---|
| Name | `doc-qa` | |
| CIDR | `10.0.0.0/16` | 65,536개 IP |
| AZ | 2개 | ALB 최소 요구사항 |
| 퍼블릭 서브넷 | 2개 | ALB, ECS, EC2 배치 |
| 프라이빗 서브넷 | 2개 | 추후 DB 추가 대비 |
| NAT Gateway | **없음** | 비용 절약, 개발 목적 |

NAT 없으므로 ECS, EC2 모두 퍼블릭 서브넷에 배치. 접근 제어는 보안그룹으로 처리.

---

## 3단계: 보안그룹 생성

트래픽이 `인터넷 → ALB → FastAPI → Ollama` 순서로만 흐르도록 체인 구성.  
소스를 IP가 아닌 보안그룹 ID로 지정 → ALB IP가 변경되어도 자동 추적.

### sg-alb (ALB용)

| 포트 | 소스 | 이유 |
|---|---|---|
| 80, 443 | `0.0.0.0/0` | 외부 사용자 진입점 |

### sg-api (FastAPI ECS용)

| 포트 | 소스 | 이유 |
|---|---|---|
| 8000 | `sg-alb` | ALB에서 오는 트래픽만 허용 |

### sg-ollama (Ollama EC2용)

| 포트 | 소스 | 이유 |
|---|---|---|
| 11434 | `sg-api` | FastAPI에서 오는 요청만 허용 |
| 22 | 내 IP | SSH 관리 접속 |

---

## 4단계 이후 (진행 예정)

이후 단계는 진행하며 추가 예정.
