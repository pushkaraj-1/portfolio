"use client";

import { useState } from "react";

interface NavbarProps {
  activeSection: string;
  setActiveSection: (section: string) => void;
  darkMode: boolean;
  setDarkMode: (dark: boolean) => void;
}

export function Navbar({
  activeSection,
  setActiveSection,
  darkMode,
  setDarkMode,
}: NavbarProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: "about", label: "about" },
    { id: "news", label: "news" },
    { id: "publications", label: "publications" },
    { id: "projects", label: "projects" },
    { id: "experience", label: "experience & outreach" },
  ];

  const scrollToSection = (id: string) => {
    setActiveSection(id);
    setMobileMenuOpen(false);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <header
      className={`sticky top-0 z-50 backdrop-blur-md transition-colors duration-300 border-b ${
        darkMode
          ? "bg-[#121212]/90 border-neutral-800 text-neutral-200"
          : "bg-white/90 border-neutral-200 text-neutral-800"
      }`}
    >
      <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Brand Name */}
        <button
          onClick={() => scrollToSection("about")}
          className="text-lg font-semibold tracking-tight hover:opacity-80 transition-opacity text-left cursor-pointer"
        >
          Pushkaraj Baradkar
        </button>

        {/* Desktop Nav Items */}
        <nav className="hidden md:flex items-center space-x-6 text-sm font-medium">
          {navItems.map((item) => {
            const isActive = activeSection === item.id;
            return (
              <button
                key={item.id}
                onClick={() => scrollToSection(item.id)}
                className={`transition-colors cursor-pointer capitalize ${
                  isActive
                    ? darkMode
                      ? "text-cyan-400 font-semibold underline underline-offset-4"
                      : "text-blue-600 font-semibold underline underline-offset-4"
                    : darkMode
                    ? "text-neutral-400 hover:text-white"
                    : "text-neutral-600 hover:text-black"
                }`}
              >
                {isActive ? `[${item.label}]` : item.label}
              </button>
            );
          })}

          {/* Theme Switcher Button */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className={`p-2 rounded-full transition-colors cursor-pointer border ${
              darkMode
                ? "bg-neutral-800 border-neutral-700 text-yellow-400 hover:bg-neutral-700"
                : "bg-neutral-100 border-neutral-200 text-neutral-700 hover:bg-neutral-200"
            }`}
            title="Toggle light/dark theme"
            aria-label="Toggle theme"
          >
            {darkMode ? (
              <svg className="w-4 h-4 fill-current" viewBox="0 0 20 20">
                <path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4.22 2.78a1 1 0 011.415 0l.707.707a1 1 0 01-1.414 1.414l-.708-.707a1 1 0 010-1.414zm2.78 6.22a1 1 0 010 1.414l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 0zM10 16a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zm-4.22-2.78a1 1 0 010 1.414l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 0zM3 10a1 1 0 011-1h1a1 1 0 110 2H4a1 1 0 01-1-1zm2.78-6.22a1 1 0 011.414 1.414l-.707.707a1 1 0 01-1.414-1.414l.707-.707zM10 6a4 4 0 100 8 4 4 0 000-8z" />
              </svg>
            ) : (
              <svg className="w-4 h-4 fill-current" viewBox="0 0 20 20">
                <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
              </svg>
            )}
          </button>
        </nav>

        {/* Mobile controls */}
        <div className="flex md:hidden items-center space-x-3">
          <button
            onClick={() => setDarkMode(!darkMode)}
            className={`p-2 rounded-full border ${
              darkMode
                ? "bg-neutral-800 border-neutral-700 text-yellow-400"
                : "bg-neutral-100 border-neutral-200 text-neutral-700"
            }`}
            aria-label="Toggle theme"
          >
            {darkMode ? "☀️" : "🌙"}
          </button>
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-md focus:outline-none"
            aria-label="Toggle menu"
          >
            <svg className="w-6 h-6 stroke-current" fill="none" viewBox="0 0 24 24">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div
          className={`md:hidden border-b px-6 py-4 space-y-3 ${
            darkMode ? "bg-[#181818] border-neutral-800" : "bg-neutral-50 border-neutral-200"
          }`}
        >
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => scrollToSection(item.id)}
              className="block w-full text-left py-1 text-sm font-medium cursor-pointer"
            >
              {item.label}
            </button>
          ))}
        </div>
      )}
    </header>
  );
}

