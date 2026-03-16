/**
 * Better-Auth microservice — ~50 lines
 * Exposes: POST /api/auth/sign-up/email
 *          POST /api/auth/sign-in/email
 *          POST /api/auth/sign-out
 *          GET  /api/auth/session
 */

import { betterAuth } from "better-auth";
import { serve } from "@hono/node-server";
import { Hono } from "hono";
import pg from "pg";

const { Pool } = pg;

if (!process.env.DATABASE_URL) throw new Error("DATABASE_URL is required");
if (!process.env.BETTER_AUTH_SECRET) throw new Error("BETTER_AUTH_SECRET is required");

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET,
  database: pool,
  user: {
    modelName: "users",
    fields: {
      emailVerified: "email_verified",
      createdAt: "created_at",
      updatedAt: "updated_at",
    },
  },
  account: {
    modelName: "accounts",
    fields: {
      userId: "user_id",
      accountId: "account_id",
      providerId: "provider_id",
      accessToken: "access_token",
      refreshToken: "refresh_token",
      expiresAt: "expires_at",
      createdAt: "created_at",
      updatedAt: "updated_at",
    },
  },
  session: {
    modelName: "sessions",
    expiresIn: 60 * 60 * 24,
    fields: {
      userId: "user_id",
      expiresAt: "expires_at",
      createdAt: "created_at",
      updatedAt: "updated_at",
      ipAddress: "ip_address",
      userAgent: "user_agent",
    },
  },
  verification: {
    modelName: "verification",
    fields: {
      expiresAt: "expires_at",
      createdAt: "created_at",
      updatedAt: "updated_at",
    },
  },
  emailAndPassword: {
    enabled: true,
    onSignInFailed: () => ({ message: "Invalid email or password" }),
    onSignUpFailed: () => ({ message: "Invalid email or password" }),
  },
});

const app = new Hono();

// Mount all Better-Auth routes under /api/auth
app.all("/api/auth/*", (c) => auth.handler(c.req.raw));

const PORT = parseInt(process.env.PORT ?? "3001", 10);

serve({ fetch: app.fetch, port: PORT }, () => {
  console.log(`Auth service running on port ${PORT}`);
});
