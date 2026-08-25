import './globals.css';
import React from 'react';

export const metadata = {
  title: "Conway's Game of Life — Full-Stack Interactive Simulation",
  description: "High-performance full-stack Conway's Game of Life with Next.js HTML Canvas & FastAPI WebSockets.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <main>{children}</main>
      </body>
    </html>
  );
}
