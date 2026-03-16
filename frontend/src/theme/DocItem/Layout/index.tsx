/**
 * Swizzled DocItem/Layout — appends ChatPanel after every chapter page.
 * The chapterId is derived from the document's id (slug).
 */
import React from "react";
import Layout from "@theme-original/DocItem/Layout";
import type LayoutType from "@theme/DocItem/Layout";
import type { WrapperProps } from "@docusaurus/types";
import { useDoc } from "@docusaurus/plugin-content-docs/client";
import ChatPanel from "@site/src/components/ChatPanel";
import { JSX } from "react/jsx-runtime";

type Props = WrapperProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): JSX.Element {
  const { metadata } = useDoc();
  // Use the doc id as the chapterId (e.g. "module-1-ros2/week-01-ros2-fundamentals")
  const chapterId = metadata.id ?? metadata.slug ?? "unknown";

  return (
    <>
      <Layout {...props} />
      <ChatPanel chapterId={chapterId} />
    </>
  );
}
