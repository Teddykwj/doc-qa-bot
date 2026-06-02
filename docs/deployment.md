# AWS 무중단 배포 가이드

## 전체 아키텍처

```
인터넷
  │ 80
 ALB (퍼블릭 서브넷 A/B)
  │ 8000
 ECS Fargate - FastAPI (퍼블릭 서브넷)
  │  └── EFS 마운트 → /app/data (ChromaDB 영구 저장)
  │ 11434
 EC2 t3.micro - Ollama + tinyllama (퍼블릭 서브넷)
```

**무중단 배포 원리**: 코드 push → GitHub Actions → 새 이미지 ECR 푸시 → ECS 롤링 업데이트 → `/health` 통과 후 구 태스크 종료.

---

## 구성 리소스 요약

| 리소스 | 이름 | 설정 |
|---|---|---|
| VPC | `doc-qa-vpc` | 10.0.0.0/16, 서울 리전 |
| 퍼블릭 서브넷 | 2개 | ap-northeast-2a/b |
| 보안그룹 | `sg-alb`, `sg-api`, `sg-ollama` | 체인 방식 |
| EC2 | `doc-qa-ollama` | t3.micro, Ubuntu 24.04 |
| ECR | `doc-qa-api` | Private |
| EFS | `doc-qa-chroma` | ChromaDB 저장 |
| ALB | `doc-qa-alb` | HTTP:80 |
| 타겟그룹 | `doc-qa-tg` | HTTP:8000, /health 체크 |
| ECS 클러스터 | `doc-qa-cluster` | Fargate |
| ECS 태스크 | `doc-qa-task` | 0.25 vCPU / 0.5GB |
| ECS 서비스 | `doc-qa-service` | desired: 1 |
| IAM | `github-actions-deploy` | ECR + ECS 권한 |

---

## 배포 과정

### 1단계: IAM 사용자 생성

루트 계정은 MFA 설정 후 잠궈두고, 이후 모든 작업은 IAM 사용자로 진행.

- 루트 계정 → Security credentials → MFA 활성화
- IAM → Users → `doc-qa-deploy` 생성 → `AdministratorAccess` 부여
- IAM 사용자로 재로그인

---

### 2단계: VPC 생성

리전: **서울 (ap-northeast-2)**, VPC and more 옵션 사용.

| 항목 | 값 | 이유 |
|---|---|---|
| CIDR | `10.0.0.0/16` | 65,536개 IP |
| AZ | 2개 | ALB 최소 요구사항 |
| 퍼블릭 서브넷 | 2개 | ALB, ECS, EC2 배치 |
| 프라이빗 서브넷 | 2개 | 추후 DB 추가 대비 |
| NAT Gateway | **없음** | 비용 절약 (월 $32) |

NAT 없으므로 ECS, EC2 모두 퍼블릭 서브넷에 배치. 접근 제어는 보안그룹으로 처리.

---

### 3단계: 보안그룹 생성

트래픽이 `인터넷 → ALB → FastAPI → Ollama` 순서로만 흐르도록 체인 구성.
소스를 IP가 아닌 보안그룹 ID로 지정 → ALB IP가 변경되어도 자동 추적.

**sg-alb** (ALB용)
| 포트 | 소스 |
|---|---|
| 80, 443 | `0.0.0.0/0` |

**sg-api** (FastAPI ECS용)
| 포트 | 소스 |
|---|---|
| 8000 | `sg-alb` |
| 2049 (NFS) | `sg-api` (자기 자신) ← EFS 마운트용 |

**sg-ollama** (Ollama EC2용)
| 포트 | 소스 |
|---|---|
| 11434 | `sg-api` |
| 22 | 내 IP |

---

### 4단계: EC2 생성 (Ollama 서버)

| 항목 | 값 |
|---|---|
| AMI | Ubuntu Server 24.04 LTS |
| Instance type | t3.micro |
| 서브넷 | 퍼블릭 서브넷 1개 |
| Public IP | Enable |
| 보안그룹 | `sg-ollama` |
| 스토리지 | 16GB gp3 |

EC2 접속 후 설정:

```bash
# 스왑 추가 (t3.micro 메모리 부족 대비)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Ollama 설치
curl -fsSL https://ollama.com/install.sh | sh

# Ollama 외부 접근 허용 (기본값은 localhost만 수신)
sudo mkdir -p /etc/systemd/system/ollama.service.d/
sudo bash -c 'cat > /etc/systemd/system/ollama.service.d/override.conf << EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
EOF'
sudo systemctl daemon-reload
sudo systemctl restart ollama

# 모델 pull
ollama pull tinyllama
ollama pull nomic-embed-text
```

---

### 5단계: ECR 리포지토리 생성

ECR → Create repository → Private → 이름: `doc-qa-api`

GitHub Actions가 이미지를 빌드해서 올리므로 로컬 AWS CLI 불필요.

---

### 6단계: EFS 생성 (ChromaDB 영구화)

EFS → Create file system → Customize

| 항목 | 값 |
|---|---|
| Name | `doc-qa-chroma` |
| VPC | `doc-qa-vpc` |
| Mount targets | 퍼블릭 서브넷 2개 |
| 보안그룹 | `sg-api` |

---

### 7단계: ALB + 타겟 그룹 생성

타겟 그룹 먼저 생성:

| 항목 | 값 |
|---|---|
| Target type | IP addresses |
| 이름 | `doc-qa-tg` |
| Port | 8000 |
| Health check path | `/health` |

ALB 생성:

| 항목 | 값 |
|---|---|
| 이름 | `doc-qa-alb` |
| Scheme | Internet-facing |
| VPC | `doc-qa-vpc` |
| Subnets | 퍼블릭 서브넷 2개 |
| 보안그룹 | `sg-alb` |
| Listener | HTTP:80 → `doc-qa-tg` |

---

### 8단계: ECS 설정

**ECS 서비스 연결 역할 생성** (최초 1회, CloudShell):

```bash
aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com
```

**클러스터**: `doc-qa-cluster`, Fargate

**태스크 정의** (`doc-qa-task`):

| 항목 | 값 |
|---|---|
| Launch type | Fargate |
| CPU / Memory | 0.25 vCPU / 0.5GB |
| 이미지 | ECR URI |
| 포트 | 8000 |
| 환경변수 | `OLLAMA_BASE_URL=http://<EC2 프라이빗 IP>:11434` |
| 환경변수 | `LLM_MODEL=tinyllama` |
| 환경변수 | `EMBEDDING_MODEL=nomic-embed-text` |
| Volume | EFS `doc-qa-chroma` → `/app/data` |

**서비스** (`doc-qa-service`):

| 항목 | 값 |
|---|---|
| Launch type | Fargate |
| Desired tasks | 1 |
| 서브넷 | 퍼블릭 서브넷 2개 |
| Public IP | Enabled (ECR pull용) |
| 보안그룹 | `sg-api` |
| Load balancer | `doc-qa-alb` → `doc-qa-tg` |

---

### 9단계: GitHub Actions CI/CD

**GitHub Actions용 IAM 사용자** (CloudShell):

```bash
aws iam create-user --user-name github-actions-deploy
aws iam attach-user-policy \
  --user-name github-actions-deploy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser
aws iam attach-user-policy \
  --user-name github-actions-deploy \
  --policy-arn arn:aws:iam::aws:policy/AmazonECS_FullAccess
aws iam create-access-key --user-name github-actions-deploy
```

**GitHub Secrets 등록** (저장소 → Settings → Secrets → Actions):

| 이름 | 값 |
|---|---|
| `AWS_ACCESS_KEY_ID` | 위에서 발급한 키 |
| `AWS_SECRET_ACCESS_KEY` | 위에서 발급한 시크릿 |
| `AWS_REGION` | `ap-northeast-2` |
| `ECR_REGISTRY` | `<계정ID>.dkr.ecr.ap-northeast-2.amazonaws.com` |

계정 ID 확인: `aws sts get-caller-identity --query Account --output text`

워크플로우 파일: `.github/workflows/deploy.yml` (코드베이스에 포함)

---

## 트러블슈팅

### ECS 서비스 연결 역할 없음
```
InvalidParameterException: Unable to assume the service linked role
```
CloudShell에서 수동 생성:
```bash
aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com
```

### EFS 마운트 타임아웃
```
Mount attempt failed due to timeout after 15 sec
```
`sg-api` 보안그룹에 NFS(2049) 인바운드 규칙 누락. 소스를 `sg-api` 자기 자신으로 추가.

### t3.micro 메모리 부족
```
model requires more system memory than is available
```
스왑 2GB 추가로 해결 (4단계 참고).

### Ollama 외부 접근 불가
```
Failed to connect to Ollama
```
Ollama가 기본적으로 `127.0.0.1`만 수신. `OLLAMA_HOST=0.0.0.0` 환경변수 설정 후 재시작 (4단계 참고).

---

## 비용

| 항목 | 실행 중 | 중지 후 |
|---|---|---|
| ECS Fargate | ~$9/월 | $0 |
| EC2 t3.micro | ~$7.5/월 | $0 |
| EBS 스토리지 | ~$1.3/월 | ~$1.3/월 |
| ALB | ~$18/월 | ~$18/월 (삭제해야 $0) |
| EFS | ~$0.1/월 | ~$0.1/월 |

---

## 리소스 중지 / 재시작

### 중지 (CloudShell)

```bash
# ECS 태스크 중지
aws ecs update-service --cluster doc-qa-cluster --service doc-qa-service --desired-count 0

# EC2 중지
INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=doc-qa-ollama" \
  --query "Reservations[0].Instances[0].InstanceId" \
  --output text)
aws ec2 stop-instances --instance-ids $INSTANCE_ID

# ALB 삭제 (월 $18 절약)
ALB_ARN=$(aws elbv2 describe-load-balancers \
  --names doc-qa-alb \
  --query "LoadBalancers[0].LoadBalancerArn" \
  --output text)
aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN
```

### 재시작 (CloudShell)

```bash
# EC2 시작
INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=doc-qa-ollama" \
  --query "Reservations[0].Instances[0].InstanceId" \
  --output text)
aws ec2 start-instances --instance-ids $INSTANCE_ID
```

ALB는 콘솔에서 재생성 (7단계 참고). 생성 후 ECS 서비스에 다시 연결.

```bash
# ECS 태스크 재시작
aws ecs update-service --cluster doc-qa-cluster --service doc-qa-service --desired-count 1
```

### 상태 확인

```bash
# EC2 상태
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=doc-qa-ollama" \
  --query "Reservations[0].Instances[0].State.Name" \
  --output text

# ALB 존재 여부
aws elbv2 describe-load-balancers --names doc-qa-alb \
  --query "LoadBalancers[0].State.Code" --output text 2>&1

# API 헬스체크
curl http://<ALB DNS>/health
```
