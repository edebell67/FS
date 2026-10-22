# WF-105 Access Review

| Principal | Non-DNA schema | Private research API | Public directory API |
|---|---:|---:|---:|
| Public/anonymous | Deny | Deny | Read approved DNA fields |
| Authenticated directory user | Deny | Deny | Read approved DNA fields |
| Researcher | Read via research service | Allow | Same public contract |
| Research service | Least-privilege read | Execute | No public publishing rights |
| Directory service | Deny | Deny | Serve DNA read models |
| Auditor | Metadata/read evidence | Read-only evidence | Read approved DNA fields |

Approval state: design approved for implementation. Production grants require database/security review and must preserve default-deny behavior.
