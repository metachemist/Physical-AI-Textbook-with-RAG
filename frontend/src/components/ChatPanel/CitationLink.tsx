import React from "react";

export interface Citation {
  chapterId: string;
  sectionId: string;
  sourceUrl: string;
  score?: number;
}

interface CitationLinkProps {
  citation: Citation;
  index: number;
}

export default function CitationLink({ citation, index }: CitationLinkProps) {
  return (
    <a
      href={citation.sourceUrl}
      target="_blank"
      rel="noopener noreferrer"
      title={`${citation.chapterId}: ${citation.sectionId}`}
    >
      [{citation.chapterId}: {citation.sectionId}]
    </a>
  );
}
