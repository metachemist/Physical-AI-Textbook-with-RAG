/**
 * AuthModal — sign-up (with 3-question profile) and sign-in forms.
 * Stores Bearer token in localStorage under "pai_auth_token".
 */
import React, { useCallback, useState } from "react";
import styles from "./AuthModal.module.css";

const TOKEN_KEY = "pai_auth_token";

export function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function clearAuthToken(): void {
  if (typeof window !== "undefined") localStorage.removeItem(TOKEN_KEY);
}

type View = "signin" | "signup" | "profile";

interface AuthModalProps {
  onClose: () => void;
  onAuthenticated: () => void;
}

export default function AuthModal({ onClose, onAuthenticated }: AuthModalProps) {
  const [view, setView] = useState<View>("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [pythonLevel, setPythonLevel] = useState("none");
  const [rosExperience, setRosExperience] = useState("none");
  const [aiKnowledge, setAiKnowledge] = useState("none");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSignIn = useCallback(async () => {
    setError(null);
    setLoading(true);
    try {
      const res = await fetch("/api/auth/sign-in/email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.message ?? "Invalid email or password");
        return;
      }
      const token = data.token ?? data.session?.token;
      if (token) {
        localStorage.setItem(TOKEN_KEY, token);
        onAuthenticated();
        onClose();
      } else {
        setError("Sign-in succeeded but no token was returned.");
      }
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [email, password, onAuthenticated, onClose]);

  const handleSignUp = useCallback(async () => {
    setError(null);
    setLoading(true);
    try {
      const res = await fetch("/api/auth/sign-up/email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.message ?? "Invalid email or password");
        return;
      }
      const token = data.token ?? data.session?.token;
      if (token) {
        localStorage.setItem(TOKEN_KEY, token);
        setView("profile");
      } else {
        setError("Sign-up succeeded but no token was returned.");
      }
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [email, password]);

  const handleSaveProfile = useCallback(async () => {
    setError(null);
    setLoading(true);
    const token = localStorage.getItem(TOKEN_KEY);
    try {
      const res = await fetch("/api/v1/profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          python_level: pythonLevel,
          ros_experience: rosExperience,
          ai_knowledge: aiKnowledge,
        }),
      });
      if (!res.ok) {
        setError("Could not save profile. Please try again.");
        return;
      }
      onAuthenticated();
      onClose();
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [pythonLevel, rosExperience, aiKnowledge, onAuthenticated, onClose]);

  const levels = ["none", "beginner", "intermediate", "advanced"] as const;

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <button className={styles.closeBtn} onClick={onClose} aria-label="Close">
          ×
        </button>

        {view === "signin" && (
          <>
            <h2 className={styles.title}>Sign In</h2>
            {error && <p className={styles.error}>{error}</p>}
            <label className={styles.label}>Email</label>
            <input
              className={styles.input}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
            />
            <label className={styles.label}>Password</label>
            <input
              className={styles.input}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
            <button className={styles.primaryBtn} onClick={handleSignIn} disabled={loading}>
              {loading ? "Signing in…" : "Sign In"}
            </button>
            <p className={styles.switchText}>
              No account?{" "}
              <button className={styles.linkBtn} onClick={() => setView("signup")}>
                Sign up
              </button>
            </p>
          </>
        )}

        {view === "signup" && (
          <>
            <h2 className={styles.title}>Create Account</h2>
            {error && <p className={styles.error}>{error}</p>}
            <label className={styles.label}>Email</label>
            <input
              className={styles.input}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
            />
            <label className={styles.label}>Password</label>
            <input
              className={styles.input}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="new-password"
            />
            <button className={styles.primaryBtn} onClick={handleSignUp} disabled={loading}>
              {loading ? "Creating account…" : "Sign Up"}
            </button>
            <p className={styles.switchText}>
              Have an account?{" "}
              <button className={styles.linkBtn} onClick={() => setView("signin")}>
                Sign in
              </button>
            </p>
          </>
        )}

        {view === "profile" && (
          <>
            <h2 className={styles.title}>Tell us about yourself</h2>
            <p className={styles.subtitle}>
              This helps us personalize your learning experience.
            </p>
            {error && <p className={styles.error}>{error}</p>}

            <label className={styles.label}>Python experience</label>
            <select
              className={styles.select}
              value={pythonLevel}
              onChange={(e) => setPythonLevel(e.target.value)}
            >
              {levels.map((l) => (
                <option key={l} value={l}>
                  {l.charAt(0).toUpperCase() + l.slice(1)}
                </option>
              ))}
            </select>

            <label className={styles.label}>ROS experience</label>
            <select
              className={styles.select}
              value={rosExperience}
              onChange={(e) => setRosExperience(e.target.value)}
            >
              {levels.map((l) => (
                <option key={l} value={l}>
                  {l.charAt(0).toUpperCase() + l.slice(1)}
                </option>
              ))}
            </select>

            <label className={styles.label}>AI / ML knowledge</label>
            <select
              className={styles.select}
              value={aiKnowledge}
              onChange={(e) => setAiKnowledge(e.target.value)}
            >
              {levels.map((l) => (
                <option key={l} value={l}>
                  {l.charAt(0).toUpperCase() + l.slice(1)}
                </option>
              ))}
            </select>

            <button className={styles.primaryBtn} onClick={handleSaveProfile} disabled={loading}>
              {loading ? "Saving…" : "Start Learning"}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
