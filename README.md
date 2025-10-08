# 🚀 ENIS v3.0 Agent Contracts

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](https://github.com/ANDAON-SA-DE-CV/agent-contracts)
[![DNA v3.0 Compliant](https://img.shields.io/badge/DNA-v3.0-green.svg)](https://github.com/ANDAON-SA-DE-CV/agent-contracts)
[![API First](https://img.shields.io/badge/API-First-blue.svg)](https://github.com/ANDAON-SA-DE-CV/agent-contracts)

> **Centralized API contracts, schemas, and definitions serving as Source of Truth for the ENIS v3.0 platform**

## 📋 Overview

The **Agent Contracts** repository is the foundational component of ENIS v3.0, providing centralized API contracts, schemas, and definitions that serve as the **Source of Truth** for the entire platform. This repository enables API-first development, contract-driven design, and automatic SDK generation across all ENIS services.

## 🎯 Key Features

- **📄 OpenAPI 3.0 Specifications** - Complete API documentation
- **🔧 JSON Schema Definitions** - Data validation schemas
- **⚡ Protocol Buffers (proto3)** - High-performance serialization
- **📱 TypeScript Definitions** - Type-safe development
- **🔄 Automatic SDK Generation** - Multi-language SDKs
- **✅ CI/CD Validation** - Contract testing and validation
- **🌐 Cross-Service Integration** - Unified API contracts

## 🏗️ Repository Structure

```
agent-contracts/
├── contracts/           # OpenAPI 3.0 specifications
│   ├── nops-kernel-api.yaml
│   ├── inference-service-api.yaml
│   ├── edge-agents-api.yaml
│   └── event-bus-api.yaml
├── schemas/            # JSON Schema definitions
│   ├── agent-registration.json
│   ├── inference-request.json
│   └── event-schema.json
├── proto/              # Protocol Buffers definitions
│   ├── inference.proto
│   ├── agents.proto
│   └── events.proto
├── sdks/               # Generated SDKs
│   ├── python/
│   ├── typescript/
│   ├── go/
│   └── java/
└── docs/               # Documentation
    ├── 00-master-prompts/
    └── 01-enis-complete/
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Go 1.21+
- Java 17+

### Installation

```bash
# Clone the repository
git clone https://github.com/ANDAON-SA-DE-CV/agent-contracts.git
cd agent-contracts

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Generate SDKs
make generate-sdks

# Validate contracts
make validate
```

## 📚 Documentation

- **[Master Prompts](docs/00-master-prompts/)** - Core documentation and specifications
- **[Architecture](docs/01-enis-complete/)** - Complete architecture documentation
- **[API Reference](contracts/)** - OpenAPI specifications
- **[Schema Reference](schemas/)** - JSON Schema definitions

## 🔗 Related Repositories

- **[nops-kernel](https://github.com/ANDAON-SA-DE-CV/nops-kernel)** - Network Operating Platform System
- **[inference-service](https://github.com/ANDAON-SA-DE-CV/inference-service)** - AI inference engine
- **[edge-agents](https://github.com/ANDAON-SA-DE-CV/edge-agents)** - Edge agent implementations
- **[agent-sdks](https://github.com/ANDAON-SA-DE-CV/agent-sdks)** - Multi-language SDKs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is proprietary software owned by ANDAON SA DE CV. All rights reserved. 
See the [LICENSE](LICENSE) file for details. For licensing inquiries, contact info@andaon.com.

## 🏢 About ANDAON

[ANDAON SA DE CV](https://andaon.com/) is a versatile plugin creator for Bubble with deep experience in third-party integrations. We specialize in connecting Bubble apps with external services through powerful integrations.

## 📞 Contact

- **Website**: [andaon.com](https://andaon.com/)
- **Email**: info@andaon.com
- **GitHub**: [@ANDAON-SA-DE-CV](https://github.com/ANDAON-SA-DE-CV)

---

**Built with ❤️ by ANDAON SA DE CV for ENIS v3.0**
