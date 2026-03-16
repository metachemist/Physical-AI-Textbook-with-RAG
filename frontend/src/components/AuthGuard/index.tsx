/**
 * AuthGuard — wraps protected features (Personalize, Translate, Quiz, Summarize).
 * If no auth token, shows an inline "Sign in to use this feature" prompt instead.
 */
import React, { useCallback, useEffect, useState } from "react";
import AuthModal, { getAuthToken } from "../AuthModal";
import styles from "./AuthGuard.module.css";

interface AuthGuardProps {
  featureName: string;
  children: React.ReactNode;
}

export default function AuthGuard({ featureName, children }: AuthGuardProps) {
  const [hasToken, setHasToken] = useState(false);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    setHasToken(!!getAuthToken());
  }, []);

  const handleAuthenticated = useCallback(() => {
    setHasToken(true);
  }, []);

  if (hasToken) return <>{children}</>;

  return (
    <div className={styles.guard}>
      <p className={styles.message}>
        Sign in to use <strong>{featureName}</strong>.
      </p>
      <button className={styles.signInBtn} onClick={() => setShowModal(true)}>
        Sign In
      </button>
      {showModal && (
        <AuthModal
          onClose={() => setShowModal(false)}
          onAuthenticated={handleAuthenticated}
        />
      )}
    </div>
  );
}
