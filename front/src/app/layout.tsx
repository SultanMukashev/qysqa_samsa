'use client';

import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import 'primeicons/primeicons.css';
import "primereact/resources/themes/lara-light-cyan/theme.css";
import { PrimeReactProvider } from 'primereact/api';
import { usePathname, useRouter } from 'next/navigation'; 
import { useMe } from "@/shared/store/useMe";
import { useEffect } from "react";
import HeaderUI from "@/shared/components/Header";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  
  const pathname = usePathname()  
  const isAuthRoute = pathname.includes('/auth');
  const { isAuth } = useMe()
  const router = useRouter()

  useEffect(() => {
    if (!isAuth()) {
      router.push('/auth');
    }
  }, [])

  return (
    <html lang="en">
      <PrimeReactProvider>
        <body
          className={`${geistSans.variable} ${geistMono.variable} flex antialiased h-screen w-screen`}
        >
          <div className="w-full h-full flex flex-col gap-8 items-center justify-start overflow-hidden">
            {!isAuthRoute && <HeaderUI/>}
            <div className="w-[1200px] col-6 flex-1 overflow-auto">
              {children}
            </div>
          </div>
        </body>
      </PrimeReactProvider>
    </html>
  );
}
