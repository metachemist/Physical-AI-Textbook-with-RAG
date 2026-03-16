import React, { useEffect, useState } from "react";
import styles from "./ChatPanel.module.css";

const MIN_SELECTION_LENGTH = 20;

interface SelectedTextBadgeProps {
  onSelectionChange: (text: string | null) => void;
}

export default function SelectedTextBadge({ onSelectionChange }: SelectedTextBadgeProps) {
  const [selectedText, setSelectedText] = useState<string | null>(null);

  useEffect(() => {
    function handleSelectionChange() {
      const sel = window.getSelection();
      const text = sel ? sel.toString() : "";
      if (text.length >= MIN_SELECTION_LENGTH) {
        setSelectedText(text);
        onSelectionChange(text);
      } else {
        setSelectedText(null);
        onSelectionChange(null);
      }
    }

    document.addEventListener("selectionchange", handleSelectionChange);
    return () => document.removeEventListener("selectionchange", handleSelectionChange);
  }, [onSelectionChange]);

  if (!selectedText) return null;

  return (
    <div className={styles.selectionBadge}>
      <span className={styles.selectionIcon}>✦</span>
      <span className={styles.selectionText}>
        Asking about: &ldquo;{selectedText.slice(0, 60)}
        {selectedText.length > 60 ? "…" : ""}&rdquo;
      </span>
    </div>
  );
}
