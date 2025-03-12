"use client";
import { useRouter } from "next/navigation"; // ✅ Use Next.js router
import Cookies from "js-cookie";
import React, { useState, useEffect } from 'react';



const Header: React.FC = () => {
  const router = useRouter(); // ✅ Use Next.js router


    return (

      <nav className="bg-black border-gray-200 dark:bg-gray-900">
        <div className="max-w-screen-xl flex flex-wrap items-center mx-auto p-4">
    
          {/* Left-aligned Blogger title */}
          <a href="/home" className="flex items-center space-x-3">
            <span className="text-2xl font-semibold text-white">AccountingAI</span>
          </a>

          {/* Right-aligned buttons */}
          <div className="flex items-center space-x-4 ml-auto">
      
            {/* Navigation links */}
            <div className="hidden md:flex space-x-8">
              <a href="/documents/upload" className="text-white">Upload File</a>
            </div>

            {/* Mobile Menu Button */}
            <button type="button" className="md:hidden p-2 text-gray-500 rounded-lg focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:focus:ring-gray-600"
              onClick={() => {
                const menu = document.getElementById("mobile-menu");
                menu?.classList.toggle("hidden");
              }}>
              <span className="sr-only">Open main menu</span>
              <svg className="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7" />
              </svg>
            </button>
          </div>

          {/* Mobile Menu */}
          <div className="hidden w-full md:hidden mt-4" id="mobile-menu">
            <a href="/documents/upload" className="block py-2 text-white">Upload File</a>
          </div>

        </div>
      </nav>

    );
}

export default Header;