/**
 * SectionToolbar — Personalize and Translate → Urdu buttons for a chapter section.
 * Auth-guarded: unauthenticated users see an inline "Sign in to use this feature" prompt.
 */
import React, { useCallback, useState } from "react";
import AuthGuard from "../AuthGuard";
import { getAuthToken } from "../AuthModal";
import styles from "./SectionToolbar.module.css";

interface SectionToolbarProps {
  /** The original markdown text of the section */
  markdown: string;
  chapterId: string;
  /** Callback invoked when the section content should change */
  onContentChange: (newMarkdown: string, label: string) => void;
  onRevert: () => void;
  isModified: boolean;
}

type ToolbarState = "idle" | "loading" | "error";

export default function SectionToolbar({
  markdown,
  chapterId,
  onContentChange,
  onRevert,
  isModified,
}: SectionToolbarProps) {
  const [state, setState] = useState<ToolbarState>("idle");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const post = useCallback(
    async (endpoint: string, body: Record<string, string>, label: string) => {
      setState("loading");
      setErrorMsg(null);
      const token = getAuthToken();
      try {
        const res = await fetch(endpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(body),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail ?? "Request failed");
        }
        if (data.validationFailed || data.formatPreservedFailed) {
          setErrorMsg("Structure validation failed — original content restored.");
          setState("error");
          return;
        }
        const newContent = data.rewrittenMarkdown ?? data.translatedMarkdown ?? markdown;
        onContentChange(newContent, label);
        setState("idle");
      } catch (err: unknown) {
        setErrorMsg((err as Error).message ?? "Something went wrong.");
        setState("error");
      }
    },
    [markdown, onContentChange]
  );

  const handlePersonalize = () =>
    post("/api/v1/personalize", { markdown, chapterId }, "Personalized");

  const handleTranslate = () =>
    post("/api/v1/translate", { markdown, targetLanguage: "urdu" }, "Urdu");

  return (
    <AuthGuard featureName="Personalize &amp; Translate">
      <div className={styles.toolbar}>
        <button
          className={styles.toolBtn}
          onClick={handlePersonalize}
          disabled={state === "loading"}
          title="Rewrite this section for your learning track"
        >
          {state === "loading" ? "…" : "Personalize"}
        </button>

        <button
          className={styles.toolBtn}
          onClick={handleTranslate}
          disabled={state === "loading"}
          title="Translate this section to Urdu"
        >
          {state === "loading" ? "…" : "اردو"}
        </button>

        {isModified && (
          <button className={styles.revertBtn} onClick={onRevert} title="Restore original content">
            Revert
          </button>
        )}

        {errorMsg && <span className={styles.errorMsg}>{errorMsg}</span>}
      </div>
    </AuthGuard>
  );
}
