# AcmeDocs Data-Flow Diagram

```mermaid
flowchart TD
    subgraph Client["Untrusted client zone"]
        User["User / Tenant Admin"]
        Browser["Browser + Session"]
        User --> Browser
    end

    subgraph Edge["Public edge zone"]
        Gateway["API Gateway"]
        V1["Deprecated /api/v1"]
        V2["Current /api/v2"]
        Gateway --> V1
        Gateway --> V2
    end

    subgraph Application["Trusted application zone"]
        API["Backend API + Authorization Policy"]
        V1 -->|"TB-2"| API
        V2 -->|"TB-2"| API
    end

    subgraph Data["Protected data-services zone"]
        Database[("Database")]
        Storage[("Object Storage")]
        Audit[("Audit Logs")]
    end

    Email["TB-4: External Email Service"]

    Browser -->|"TB-1: HTTPS request and session"| Gateway
    API -->|"TB-3"| Database
    API -->|"TB-3"| Storage
    API -->|"TB-3"| Audit
    API -->|"Invitation delivery"| Email
Boundary interpretation
The browser is controlled by the user and cannot make authorization decisions.
The API gateway is an enforcement layer, but it is not the final authorization
point for business actions.
The backend policy evaluates actor, tenant, role, action and object before data
access.
Database and storage operations must use the already-authorized tenant scope.
Email delivery crosses an external dependency boundary.
/api/v1 and /api/v2 must reach the same authorization policy.
High-risk flows
Cross-tenant document lookup
Object-storage download authorization
Role and invitation changes
Support-administrator access
Organization export creation and download
Session reuse after logout or privilege downgrade
Deprecated API access
Audit-event creation
