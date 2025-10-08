<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
Índice

- [Master Prompt: enis-frontend-master-prompt.md – Frontend Completo v3.0](#master-prompt-enis-frontend-master-promptmd--frontend-completo-v30)
  - [🎯 CONTEXTO Y PROPÓSITO](#-contexto-y-prop%C3%93sito)
  - [🧬 HERENCIA DEL DNA v3.0](#-herencia-del-dna-v30)
    - [Voz y Personalidad](#voz-y-personalidad)
  - [🔗 DEPENDENCIAS Y CROSS-REFERENCES](#-dependencias-y-cross-references)
    - [Dependencias Obligatorias](#dependencias-obligatorias)
    - [Cross-References Arquitecturales](#cross-references-arquitecturales)
  - [📋 **ARQUITECTURA DEL REPOSITORIO**](#-arquitectura-del-repositorio)
    - [**Estructura de Directorios**](#estructura-de-directorios)
  - [🔧 **ESPECIFICACIONES TÉCNICAS**](#-especificaciones-t%C3%89cnicas)
    - [**Dashboard App**](#dashboard-app)
    - [**Developer Portal**](#developer-portal)
    - [**Studio App**](#studio-app)
    - [**Design System**](#design-system)
    - [**Shared Utilities**](#shared-utilities)
  - [🚀 **CONFIGURACIÓN Y DEPLOYMENT**](#-configuraci%C3%93n-y-deployment)
    - [**Turborepo Configuration**](#turborepo-configuration)
    - [**Package.json Workspaces**](#packagejson-workspaces)
    - [**Docker Configuration**](#docker-configuration)
  - [🧪 **TESTING**](#-testing)
    - [**Unit Tests**](#unit-tests)
    - [**Integration Tests**](#integration-tests)
  - [📊 **MÉTRICAS DE ÉXITO**](#-m%C3%89tricas-de-%C3%89xito)
    - [**Métricas Técnicas**](#m%C3%A9tricas-t%C3%A9cnicas)
    - [**Métricas de Usuario**](#m%C3%A9tricas-de-usuario)
  - [🚀 **PRÓXIMOS PASOS**](#-pr%C3%93ximos-pasos)
    - [**Inmediato (Semana 1-2)**](#inmediato-semana-1-2)
    - [**Corto Plazo (Semana 3-4)**](#corto-plazo-semana-3-4)
    - [**Mediano Plazo (Semana 5-6)**](#mediano-plazo-semana-5-6)
    - [**Largo Plazo (Mes 2+)**](#largo-plazo-mes-2)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---
doc_version: "3.0"
doc_type: "Master Prompt"
doc_author: "@andaon"
doc_date: "2025-01-21"
compliance: "DNA v3.0"
semver: "3.0.0"
master_prompt_id: "enis-frontend-master"
domain: "ENIS Frontend"
tier_applicability: ["Tier 1 SMB", "Tier 2 Professional", "Tier 3 Enterprise"]
generates: ["apps/", "packages/", "design-system/", "docs/"]
total_pages: "250-300"
dependencies:
  - "00-dna-proyecto-prompt.md"
  - "02-architecture-master-prompt.md"
  - "03-business-master-prompt.md"
  - "agent-contracts-master-prompt.md"
  - "AGENT_SDKS_MASTER_PROMPT.md"
  - "AGENT_MARKETPLACE_MASTER_PROMPT.md"
tech_stack: ["Next.js 14", "React 18", "TypeScript", "TailwindCSS", "Vite"]
pipeline_integration: "Frontend Development Orchestration (05)"
validation_script: "validate-enis-frontend-master.js"
release_status: "ready_for_production"
applications_count: 3
packages_count: 8
encoding: "UTF-8"
---

# Master Prompt: enis-frontend-master-prompt.md – Frontend Completo v3.0

## 🎯 CONTEXTO Y PROPÓSITO

**ROL:** Eres el Arquitecto Principal de Frontend de Enterprise Neural Intelligence Systems v3.0, experto en monorepos, design systems, y aplicaciones web modernas.

**TAREA:** Generar documentación técnica integral, validada y auditable para el repositorio enis-frontend, abarcando dashboard, developer portal, studio app, design system, y documentación exhaustiva del frontend.

**OBJETIVO:** Producir 250-300 páginas de documentación production-ready que sirvan como referencia definitiva para implementación, operación y evolución del frontend, manteniendo coherencia absoluta con DNA v3.0 y asegurando escalabilidad empresarial.

**CONTEXTO:** enis-frontend representa la capa de presentación completa en ENIS v3.0: un monorepo que incluye dashboard, developer portal, studio app, y un design system compartido para todas las aplicaciones.

## 🧬 HERENCIA DEL DNA v3.0

### Voz y Personalidad

```yaml
voice_inheritance:
  technical_authority: 
    - "Experto en frontend moderno"
    - "Autoridad en design systems"
    - "Especialista en monorepos"
    - "Visionario en UX/UI"
    
  tone_consistency:
    - "Profesional pero accesible"
    - "Técnicamente preciso"
    - "Orientado a producción"
    - "Pragmático y ejecutable"
    
  approach:
    - "User-first design"
    - "Component-driven development"
    - "Performance optimized"
    - "Accessibility by default"
```

## 🔗 DEPENDENCIAS Y CROSS-REFERENCES

### Dependencias Obligatorias

```yaml
dependencies_matrix:
  dna_foundation:
    source: "00-dna-proyecto-prompt.md"
    inherits:
      - "Voz y terminología"
      - "Principios arquitecturales"
      - "Valores empresariales"
      - "Paradigma tecnológico"
      
  architecture_core:
    source: "02-architecture-master-prompt.md"
    inherits:
      - "Arquitectura de frontend"
      - "Patrones de UI/UX"
      - "Diseño de componentes"
      - "Security framework"
      
  business_alignment:
    source: "03-business-master-prompt.md"
    inherits:
      - "Casos de uso empresariales"
      - "ROI metrics"
      - "Value propositions"
      - "Market positioning"
      
  contracts_foundation:
    source: "agent-contracts-master-prompt.md"
    inherits:
      - "API contracts"
      - "Service definitions"
      - "Data schemas"
      - "Integration patterns"
      
  sdk_integration:
    source: "AGENT_SDKS_MASTER_PROMPT.md"
    inherits:
      - "SDK generation patterns"
      - "Multi-language support"
      - "Developer experience"
      - "Code generation automation"
      
  marketplace_integration:
    source: "AGENT_MARKETPLACE_MASTER_PROMPT.md"
    inherits:
      - "Marketplace UI patterns"
      - "Agent catalog integration"
      - "Publishing workflows"
      - "User experience patterns"
```

### Cross-References Arquitecturales

```yaml
architectural_cross_references:
  frontend_to_backend:
    dashboard_api:
      app: "/apps/dashboard/api-integration.md"
      reference: "agent-contracts-master-prompt.md#dashboard-api-specifications"
      endpoints: ["/v1/dashboard/metrics", "/v1/dashboard/analytics", "/v1/dashboard/agents"]
      
    devportal_api:
      app: "/apps/devportal/api-integration.md"
      reference: "agent-contracts-master-prompt.md#devportal-api-specifications"
      endpoints: ["/v1/devportal/docs", "/v1/devportal/sdks", "/v1/devportal/examples"]
      
    studio_api:
      app: "/apps/studio/api-integration.md"
      reference: "agent-contracts-master-prompt.md#studio-api-specifications"
      endpoints: ["/v1/studio/agents", "/v1/studio/deploy", "/v1/studio/test"]
      
    api_client:
      package: "/packages/api-client/services.md"
      reference: "AGENT_SDKS_MASTER_PROMPT.md#typescript-sdk"
      modules: ["ApiClient", "AuthService", "ErrorHandler"]
    
  design_system_integration:
    components_overview:
      design: "/design-system/components/overview.md"
      reference: "agent-contracts-master-prompt.md#ui-component-specifications"
      components: ["Button", "Input", "Modal", "Table", "Chart"]
      
    design_tokens:
      design: "/design-system/tokens/design-tokens.md"
      reference: "agent-contracts-master-prompt.md#design-token-specifications"
      tokens: ["colors", "typography", "spacing", "shadows", "borders"]
      
    usage_patterns:
      design: "/design-system/patterns/usage-patterns.md"
      reference: "agent-contracts-master-prompt.md#ui-pattern-specifications"
      patterns: ["forms", "navigation", "data-display", "feedback"]
      
    accessibility_guidelines:
      design: "/design-system/accessibility/guidelines.md"
      reference: "agent-contracts-master-prompt.md#accessibility-specifications"
      guidelines: ["wcag-2.1", "keyboard-navigation", "screen-readers", "color-contrast"]
    
  sdk_integration:
    typescript_sdk:
      package: "/packages/api-client/typescript-sdk.md"
      reference: "AGENT_SDKS_MASTER_PROMPT.md#typescript-sdk"
      modules: ["@enis/nops-kernel", "@enis/inference-service", "@enis/edge-agents"]
      
    python_sdk:
      package: "/packages/api-client/python-sdk.md"
      reference: "AGENT_SDKS_MASTER_PROMPT.md#python-sdk"
      modules: ["enis-nops-kernel", "enis-inference-service", "enis-edge-agents"]
      
    go_sdk:
      package: "/packages/api-client/go-sdk.md"
      reference: "AGENT_SDKS_MASTER_PROMPT.md#go-sdk"
      packages: ["github.com/enis/nops-kernel", "github.com/enis/inference-service"]
    
  marketplace_integration:
    agent_catalog:
      app: "/apps/marketplace/agent-catalog.md"
      reference: "AGENT_MARKETPLACE_MASTER_PROMPT.md#catalog-module"
      features: ["search", "filter", "categories", "ratings"]
      
    agent_publishing:
      app: "/apps/marketplace/agent-publishing.md"
      reference: "AGENT_MARKETPLACE_MASTER_PROMPT.md#publishing-module"
      features: ["upload", "validation", "preview", "publish"]
      
    user_dashboard:
      app: "/apps/marketplace/user-dashboard.md"
      reference: "AGENT_MARKETPLACE_MASTER_PROMPT.md#user-dashboard"
      features: ["purchases", "subscriptions", "billing", "analytics"]
    
  shared_utilities:
    common_functions:
      package: "/packages/utils/common-functions.md"
      reference: "agent-contracts-master-prompt.md#utility-functions"
      functions: ["formatDate", "validateEmail", "debounce", "throttle"]
      
    custom_hooks:
      package: "/packages/hooks/custom-hooks.md"
      reference: "agent-contracts-master-prompt.md#react-hooks"
      hooks: ["useApi", "useAuth", "useLocalStorage", "useDebounce"]
      
    state_management:
      package: "/packages/state/state-management.md"
      reference: "agent-contracts-master-prompt.md#state-management"
      patterns: ["zustand", "context", "reducers", "selectors"]
      
    testing_utilities:
      package: "/packages/testing/testing-utilities.md"
      reference: "agent-contracts-master-prompt.md#testing-utilities"
      utilities: ["render", "mockApi", "testData", "assertions"]
    
  deployment_patterns:
    nextjs_deployment:
      deployment: "/deployment/nextjs/deployment.md"
      reference: "agent-contracts-master-prompt.md#nextjs-deployment"
      features: ["ssr", "ssg", "isr", "edge-functions"]
      
    docker_deployment:
      deployment: "/deployment/docker/deployment.md"
      reference: "agent-contracts-master-prompt.md#docker-deployment"
      features: ["multi-stage", "optimization", "security", "monitoring"]
      
    kubernetes_deployment:
      deployment: "/deployment/kubernetes/deployment.md"
      reference: "agent-contracts-master-prompt.md#kubernetes-deployment"
      features: ["horizontal-scaling", "rolling-updates", "health-checks"]
    - "/deployment/vite/build-optimization.md"
    - "/deployment/cdn/asset-optimization.md"
    - "/deployment/ci-cd/pipeline.md"
```

## 📋 **ARQUITECTURA DEL REPOSITORIO**

### **Estructura de Directorios**
```
enis-frontend/
├── apps/                       # Aplicaciones principales
│   ├── dashboard/              # ENIS Dashboard
│   │   ├── src/
│   │   │   ├── pages/          # Next.js pages
│   │   │   ├── components/     # Componentes específicos
│   │   │   ├── hooks/          # Custom hooks
│   │   │   ├── services/       # API services
│   │   │   ├── stores/         # State management
│   │   │   └── utils/          # Utilidades específicas
│   │   ├── public/             # Assets estáticos
│   │   ├── package.json
│   │   └── next.config.js
│   ├── devportal/              # Developer Portal
│   │   ├── src/
│   │   │   ├── pages/          # Next.js pages
│   │   │   ├── components/     # Componentes específicos
│   │   │   ├── hooks/          # Custom hooks
│   │   │   ├── services/       # API services
│   │   │   ├── stores/         # State management
│   │   │   └── utils/          # Utilidades específicas
│   │   ├── public/             # Assets estáticos
│   │   ├── package.json
│   │   └── next.config.js
│   └── studio/                 # Studio App
│       ├── src/
│       │   ├── components/     # React components
│       │   ├── pages/          # Page components
│       │   ├── hooks/          # Custom hooks
│       │   ├── services/       # API services
│       │   ├── stores/         # State management
│       │   ├── utils/          # Utilidades específicas
│       │   └── main.tsx        # Entry point
│       ├── public/             # Assets estáticos
│       ├── package.json
│       └── vite.config.ts
├── packages/                   # Paquetes compartidos
│   ├── ui/                     # Design system
│   │   ├── src/
│   │   │   ├── components/     # Componentes base
│   │   │   ├── tokens/         # Design tokens
│   │   │   ├── themes/         # Temas
│   │   │   └── utils/          # Utilidades del design system
│   │   ├── package.json
│   │   └── tailwind.config.js
│   ├── utils/                  # Utilidades compartidas
│   │   ├── src/
│   │   │   ├── api/            # API utilities
│   │   │   ├── auth/           # Authentication utilities
│   │   │   ├── validation/     # Validation utilities
│   │   │   └── helpers/        # Helper functions
│   │   └── package.json
│   ├── types/                  # TypeScript types
│   │   ├── src/
│   │   │   ├── api/            # API types
│   │   │   ├── auth/           # Auth types
│   │   │   ├── agents/         # Agent types
│   │   │   └── common/         # Common types
│   │   └── package.json
│   └── config/                 # Configuraciones compartidas
│       ├── src/
│       │   ├── eslint/         # ESLint configs
│       │   ├── typescript/     # TypeScript configs
│       │   ├── tailwind/       # Tailwind configs
│       │   └── vite/           # Vite configs
│       └── package.json
├── tools/                      # Herramientas de desarrollo
│   ├── build/                  # Build tools
│   ├── scripts/                # Development scripts
│   └── generators/             # Code generators
├── docs/                       # Documentación
│   ├── design-system/          # Design system docs
│   ├── components/             # Component docs
│   └── guides/                 # Development guides
├── tests/                      # Tests compartidos
│   ├── e2e/                    # End-to-end tests
│   └── visual/                 # Visual regression tests
├── package.json                # Root package.json (workspaces)
├── turbo.json                  # Turborepo config
├── tailwind.config.js          # Root Tailwind config
├── tsconfig.json               # Root TypeScript config
└── README.md
```

---

## 🔧 **ESPECIFICACIONES TÉCNICAS**

### **Dashboard App**
```typescript
// apps/dashboard/src/pages/index.tsx
import { GetServerSideProps } from 'next';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { DashboardOverview } from '@/components/dashboard/DashboardOverview';
import { useDashboard } from '@/hooks/useDashboard';

interface DashboardPageProps {
  initialData: DashboardData;
}

export default function DashboardPage({ initialData }: DashboardPageProps) {
  const { data, loading, error } = useDashboard(initialData);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <DashboardLayout>
      <DashboardOverview data={data} />
    </DashboardLayout>
  );
}

export const getServerSideProps: GetServerSideProps = async (context) => {
  try {
    const dashboardData = await fetchDashboardData();
    return {
      props: {
        initialData: dashboardData,
      },
    };
  } catch (error) {
    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    };
  }
};
```

### **Developer Portal**
```typescript
// apps/devportal/src/pages/agents/index.tsx
import { useState } from 'react';
import { PortalLayout } from '@/components/layout/PortalLayout';
import { AgentList } from '@/components/agents/AgentList';
import { AgentFilters } from '@/components/agents/AgentFilters';
import { useAgents } from '@/hooks/useAgents';

export default function AgentsPage() {
  const [filters, setFilters] = useState<AgentFilters>({});
  const { agents, loading, error, refetch } = useAgents(filters);

  return (
    <PortalLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">My Agents</h1>
          <button className="btn-primary">Create Agent</button>
        </div>
        
        <AgentFilters 
          filters={filters} 
          onFiltersChange={setFilters} 
        />
        
        <AgentList 
          agents={agents} 
          loading={loading} 
          error={error} 
          onRefresh={refetch} 
        />
      </div>
    </PortalLayout>
  );
}
```

### **Studio App**
```typescript
// apps/studio/src/components/Studio.tsx
import { useState, useEffect } from 'react';
import { Canvas } from '@/components/canvas/Canvas';
import { PropertiesPanel } from '@/components/properties/PropertiesPanel';
import { Toolbar } from '@/components/toolbar/Toolbar';
import { useStudio } from '@/hooks/useStudio';

export function Studio() {
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const { 
    nodes, 
    edges, 
    addNode, 
    updateNode, 
    deleteNode,
    addEdge,
    deleteEdge 
  } = useStudio();

  return (
    <div className="studio-container">
      <Toolbar 
        onAddNode={addNode}
        onSave={() => {}}
        onLoad={() => {}}
      />
      
      <div className="studio-content">
        <Canvas
          nodes={nodes}
          edges={edges}
          selectedNode={selectedNode}
          onNodeSelect={setSelectedNode}
          onNodeUpdate={updateNode}
          onNodeDelete={deleteNode}
          onEdgeAdd={addEdge}
          onEdgeDelete={deleteEdge}
        />
        
        <PropertiesPanel
          selectedNode={selectedNode}
          onNodeUpdate={updateNode}
        />
      </div>
    </div>
  );
}
```

### **Design System**
```typescript
// packages/ui/src/components/Button.tsx
import { forwardRef } from 'react';
import { cn } from '@/utils/cn';
import { ButtonProps } from './types';

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ 
    variant = 'primary', 
    size = 'md', 
    disabled = false, 
    loading = false,
    children, 
    className, 
    ...props 
  }, ref) => {
    const baseClasses = 'inline-flex items-center justify-center font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none';
    
    const variants = {
      primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
      secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
      outline: 'border border-gray-300 bg-transparent text-gray-700 hover:bg-gray-50 focus:ring-gray-500',
      ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-500',
      destructive: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
    };
    
    const sizes = {
      sm: 'h-8 px-3 text-sm',
      md: 'h-10 px-4 text-base',
      lg: 'h-12 px-6 text-lg',
    };

    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={cn(
          baseClasses,
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      >
        {loading && (
          <svg
            className="mr-2 h-4 w-4 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

### **Shared Utilities**
```typescript
// packages/utils/src/api/client.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { ApiError } from './errors';

export class ApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string, token?: string) {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add request logging
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        return response;
      },
      (error) => {
        // Handle API errors
        const apiError = new ApiError(
          error.response?.data?.message || error.message,
          error.response?.status || 500,
          error.response?.data
        );
        return Promise.reject(apiError);
      }
    );
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }
}
```

---

## 🚀 **CONFIGURACIÓN Y DEPLOYMENT**

### **Turborepo Configuration**
```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^lint"]
    },
    "type-check": {
      "dependsOn": ["^type-check"]
    },
    "test": {
      "dependsOn": ["^test"]
    }
  }
}
```

### **Package.json Workspaces**
```json
// package.json
{
  "name": "enis-frontend",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "type-check": "turbo type-check",
    "test": "turbo test",
    "clean": "turbo clean"
  },
  "devDependencies": {
    "turbo": "^1.10.0",
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
```

### **Docker Configuration**
```dockerfile
# Dockerfile
FROM node:18-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM base AS deps
RUN npm ci

FROM base AS builder
COPY . .
COPY --from=deps /app/node_modules ./node_modules
RUN npm run build

FROM base AS runner
ENV NODE_ENV=production
COPY --from=builder /app/apps/dashboard/.next ./apps/dashboard/.next
COPY --from=builder /app/apps/dashboard/public ./apps/dashboard/public
COPY --from=builder /app/apps/dashboard/package.json ./apps/dashboard/package.json
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000
CMD ["npm", "run", "start:dashboard"]
```

---

## 🧪 **TESTING**

### **Unit Tests**
```typescript
// tests/unit/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '@/components/Button';

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when loading', () => {
    render(<Button loading>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('shows loading spinner when loading', () => {
    render(<Button loading>Click me</Button>);
    expect(screen.getByRole('button')).toHaveClass('animate-spin');
  });
});
```

### **Integration Tests**
```typescript
// tests/integration/Dashboard.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { DashboardPage } from '@/pages/DashboardPage';
import { mockApiClient } from '@/mocks/api';

jest.mock('@/services/api', () => ({
  apiClient: mockApiClient,
}));

describe('Dashboard', () => {
  it('renders dashboard data', async () => {
    const mockData = {
      agents: [{ id: '1', name: 'Test Agent' }],
      metrics: { total: 10, active: 8 },
    };

    mockApiClient.get.mockResolvedValue(mockData);

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText('Test Agent')).toBeInTheDocument();
      expect(screen.getByText('10')).toBeInTheDocument();
    });
  });
});
```

---

## 📊 **MÉTRICAS DE ÉXITO**

### **Métricas Técnicas**
- **Performance**: < 3s initial load time
- **Core Web Vitals**: LCP < 2.5s, FID < 100ms, CLS < 0.1
- **Bundle Size**: < 500KB initial bundle
- **Accessibility**: WCAG 2.1 AA compliance

### **Métricas de Usuario**
- **User Engagement**: 80% daily active users
- **Task Completion**: 95% success rate
- **User Satisfaction**: 4.5+ rating
- **Support Tickets**: < 5% of users

---

## 🚀 **PRÓXIMOS PASOS**

### **Inmediato (Semana 1-2)**
1. ✅ Crear repositorio enis-frontend
2. ✅ Configurar Turborepo y workspaces
3. ✅ Implementar design system base

### **Corto Plazo (Semana 3-4)**
1. 🔨 Desarrollar ENIS Dashboard
2. 🔨 Desarrollar Developer Portal
3. 🔨 Configurar testing y CI/CD

### **Mediano Plazo (Semana 5-6)**
1. 🔨 Desarrollar Studio App
2. 🔨 Implementar autenticación
3. 🔨 Optimizar performance

### **Largo Plazo (Mes 2+)**
1. 🔨 Implementar PWA features
2. 🔨 Desarrollar mobile apps
3. 🔨 Expandir design system

---

*Master Prompt generado para ENIS v3.0 - ENIS Frontend - Enero 2025*
