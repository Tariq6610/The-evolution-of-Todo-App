"use client";

import { useEffect } from "react";

export default function ThemeInitializer() {
  useEffect(() => {
    // Initialize theme on app load
    const storedTheme = localStorage.getItem("theme");
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)",
    ).matches;

    // Determine the theme to use
    let themeToApply = "light"; // default
    if (storedTheme) {
      themeToApply = storedTheme;
    } else if (prefersDark) {
      themeToApply = "dark";
    }

    // Apply the theme
    document.documentElement.classList.toggle("dark", themeToApply === "dark");
  }, []);

  return null; // This component doesn't render anything
}
