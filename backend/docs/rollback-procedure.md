# Backend Rollback Procedure

## Platform: Render

### Steps to Roll Back to a Prior Commit

1. Open the Render dashboard: https://dashboard.render.com
2. Navigate to the `physical-ai-textbook-backend` service.
3. Click **Deploys** in the left sidebar.
4. Locate the last known-good deploy in the list.
5. Click the three-dot menu (⋮) on that deploy → **Redeploy**.
6. Render will rebuild from that specific commit's Docker image.
7. Monitor the deploy logs until you see `Application startup complete.`
8. Confirm health: `curl https://<render-service>.onrender.com/health` → HTTP 200 with all sub-checks `ok`.

### Expected Recovery Time

Target: prior version restored within **5 minutes** of initiating the redeploy.

### Dry Run Evidence

> Replace this placeholder with timestamped output from your dry-run execution.

```
[YYYY-MM-DD HH:MM:SS] Initiated redeploy of commit <sha>
[YYYY-MM-DD HH:MM:SS] Deploy logs: ...
[YYYY-MM-DD HH:MM:SS] Health check after rollback: HTTP 200
[YYYY-MM-DD HH:MM:SS] Restored latest commit: <sha>
[YYYY-MM-DD HH:MM:SS] Health check after restore: HTTP 200
Total time: X minutes Y seconds
```

### Database Rollback

If the rollback requires reverting a schema migration:

```bash
# SSH into a Render shell or run locally against Neon:
alembic downgrade -1    # or downgrade to a specific revision ID
```

Verify the schema version: `alembic current`
