import type { Metadata } from "next";
import "./globals.css";

// System fonts only: next/font/google fetches at build time, and the skeleton must build offline.

export const metadata: Metadata = {
  title: "OMA",
  description: "AI study assistant",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
