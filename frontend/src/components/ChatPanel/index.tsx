import React, { useCallback, useEffect, useRef, useState } from "react";
import CitationLink, { Citation } from "./CitationLink";
import SelectedTextBadge from "./SelectedTextBadge";
import styles from "./ChatPanel.module.css";

type ChatState = "idle" | "submitting" | "streaming" | "complete" | "error";

interface Message {
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
}

interface ChatPanelProps {
  chapterId: string;
}

function generateSessionId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

const SESSION_KEY = "pai_chat_session_id";

function getSessionId(): string {
  if (typeof window === "undefined") return generateSessionId();
  let id = sessionStorage.getItem(SESSION_KEY);
  if (!id) {
    id = generateSessionId();
    sessionStorage.setItem(SESSION_KEY, id);
  }
  return id;
}

export default function ChatPanel({ chapterId }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [state, setState] = useState<ChatState>("idle");
  const [streamBuffer, setStreamBuffer] = useState("");
  const [lastQuestion, setLastQuestion] = useState("");
  const [activeSelectedText, setActiveSelectedText] = useState<string | null>(null);
  const [shortSelectionNotice, setShortSelectionNotice] = useState(false);
  const sessionId = useRef(getSessionId());
  const abortRef = useRef<AbortController | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamBuffer]);

  const submit = useCallback(
    async (question: string) => {
      if (!question.trim() || state === "submitting" || state === "streaming") return;

      setShortSelectionNotice(false);

      // Check selection state at submit time
      const selText = window.getSelection()?.toString() ?? "";
      const effectiveSelected = selText.length >= 20 ? selText : activeSelectedText;
      if (selText.length > 0 && selText.length < 20) {
        setShortSelectionNotice(true);
      }

      setLastQuestion(question);
      setMessages((prev) => [...prev, { role: "user", content: question }]);
      setInput("");
      setState("submitting");
      setStreamBuffer("");

      // Clear selection after submit
      window.getSelection()?.removeAllRanges();
      setActiveSelectedText(null);

      const controller = new AbortController();
      abortRef.current = controller;

      try {
        const response = await fetch("/api/v1/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: question,
            chapter_id: chapterId,
            session_id: sessionId.current,
            selected_text: effectiveSelected ?? null,
          }),
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        setState("streaming");
        const reader = response.body!.getReader();
        const decoder = new TextDecoder();
        let accumulated = "";
        let finalCitations: Citation[] = [];

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const text = decoder.decode(value, { stream: true });
          const lines = text.split("\n");

          for (const line of lines) {
            if (!line.startsWith("data: ")) continue;
            const raw = line.slice(6).trim();
            if (!raw) continue;

            try {
              const data = JSON.parse(raw);
              if (data.error) {
                throw new Error(data.error);
              }
              if (data.done) {
                finalCitations = data.citations ?? [];
                setMessages((prev) => [
                  ...prev,
                  { role: "assistant", content: accumulated, citations: finalCitations },
                ]);
                setStreamBuffer("");
                setState("complete");
                return;
              }
              if (data.delta) {
                accumulated += data.delta;
                setStreamBuffer(accumulated);
              }
            } catch (parseErr) {
              if ((parseErr as Error).message !== "Unexpected end of JSON input") {
                throw parseErr;
              }
            }
          }
        }

        // Stream ended without a `done` event — treat buffered content as the answer
        if (accumulated) {
          setMessages((prev) => [
            ...prev,
            { role: "assistant", content: accumulated, citations: finalCitations },
          ]);
          setStreamBuffer("");
        }
        setState("complete");
      } catch (err: unknown) {
        if ((err as Error).name === "AbortError") return;
        setState("error");
        setStreamBuffer("");
      }
    },
    [chapterId, activeSelectedText, state]
  );

  const retry = useCallback(() => {
    if (lastQuestion) {
      setMessages((prev) => prev.filter((_, i) => i < prev.length - 1));
      submit(lastQuestion);
    }
  }, [lastQuestion, submit]);

  const handleSelectionChange = useCallback((text: string | null) => {
    setActiveSelectedText(text);
  }, []);

  const handleKey = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit(input);
    }
  };

  return (
    <div className={styles.panel}>
      <div className={styles.header}>
        <span className={styles.title}>Ask about this chapter</span>
      </div>
      <SelectedTextBadge onSelectionChange={handleSelectionChange} />

      <div className={styles.messages}>
        {messages.map((msg, i) => (
          <div key={i} className={`${styles.message} ${styles[msg.role]}`}>
            <p className={styles.content}>{msg.content}</p>
            {msg.citations && msg.citations.length > 0 && (
              <div className={styles.citations}>
                <span className={styles.citationsLabel}>Sources: </span>
                {msg.citations.map((c, ci) => (
                  <CitationLink key={ci} citation={c} index={ci} />
                ))}
              </div>
            )}
          </div>
        ))}

        {(state === "submitting" || state === "streaming") && streamBuffer && (
          <div className={`${styles.message} ${styles.assistant} ${styles.streaming}`}>
            <p className={styles.content}>{streamBuffer}</p>
          </div>
        )}

        {state === "submitting" && !streamBuffer && (
          <div className={`${styles.message} ${styles.assistant}`}>
            <span className={styles.thinking}>Thinking…</span>
          </div>
        )}

        {state === "error" && (
          <div className={`${styles.message} ${styles.error}`}>
            <p>Something went wrong. </p>
            <button className={styles.retryBtn} onClick={retry}>
              Retry
            </button>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {shortSelectionNotice && (
        <div className={styles.shortSelectionNotice}>
          Selection too short — searching all chapters instead
        </div>
      )}

      <div className={styles.inputRow}>
        <textarea
          className={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Ask a question… (Enter to send, Shift+Enter for newline)"
          rows={2}
          disabled={state === "submitting" || state === "streaming"}
          maxLength={2000}
        />
        <button
          className={styles.sendBtn}
          onClick={() => submit(input)}
          disabled={!input.trim() || state === "submitting" || state === "streaming"}
        >
          Send
        </button>
      </div>
    </div>
  );
}
