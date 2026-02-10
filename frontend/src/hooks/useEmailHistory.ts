import { useState } from "react";

const STORAGE_KEY = "email-history";

export function useEmailHistory() {
  const [emails, setEmails] = useState<string[]>(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  });

  function addEmail(email: string) {
    setEmails((prev) => {
      if (prev.includes(email)) return prev;

      const updated = [...prev, email];
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      return updated;
    });
  }

  return {
    emails,
    addEmail,
  };
}
