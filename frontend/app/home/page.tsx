'use client';
import { useState, useRef, useEffect } from "react";
import Header from '../header/page';
import { Send } from "lucide-react";

const HomePage = () => {
  
  const API_BASE_URL = process.env.PUBLIC_URL;
  console.log(API_BASE_URL);

  // Load messages from localStorage on initial render
  const [messages, setMessages] = useState<{ text: string; isUser: boolean }[]>(() => {
    // Check if we're in a browser environment (needed for Next.js)
    if (typeof window !== 'undefined') {
      const savedMessages = localStorage.getItem('chatMessages');
      return savedMessages ? JSON.parse(savedMessages) : [];
    }
    return [];
  });
  
  const [input, setInput] = useState("");
  const [isFetching, setIsFetching] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Effect to scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('chatMessages', JSON.stringify(messages));
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    setMessages((prev) => [...prev, { text: input, isUser: true }]);
    setInput("");
    setIsFetching(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/documents/query/?question=${encodeURIComponent(input)}`, {
        method: "GET",
      });

      const data = await response.json();
      typeWriterEffect(data.response);
    } catch (error) {
      console.log(error);
      typeWriterEffect("Error: Unable to fetch response.");
    }
  };

  const typeWriterEffect = (text: string) => {
    let i = 0;
    let tempText = "";
    setIsFetching(false);

    const interval = setInterval(() => {
      if (i < text.length) {
        tempText += text[i];
        setMessages((prev) => [...prev.slice(0, -1), { text: tempText, isUser: false }]);
        i++;
      } else {
        clearInterval(interval);
      }
    }, 50); // Adjust typing speed

    // Add empty bot response placeholder
    setMessages((prev) => [...prev, { text: "", isUser: false }]);
  };

  // Function to clear chat history
  const clearChat = () => {
    setMessages([]);
    localStorage.removeItem('chatMessages');
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50">
      <Header />
      <div className="flex-1 flex flex-col max-w-3xl mx-auto w-full px-4 py-2">
        {/* Messages area with clear button */}
        <div className="flex-1 overflow-y-auto mb-4 mt-2">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center">
              <div className="text-center text-slate-500">
                <h1 className="text-2xl font-medium mb-2">How can I help you today?</h1>
                <p className="text-sm">Ask me anything, or upload a document for assistance.</p>
              </div>
            </div>
          ) : (
            <>
              {/* Clear chat button */}
              <div className="flex justify-end mb-2">
                <button
                  onClick={clearChat}
                  className="text-xs text-slate-500 hover:text-purple-600 py-1 px-2"
                >
                  Clear chat
                </button>
              </div>
              <div className="space-y-6">
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex ${msg.isUser ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`rounded-lg p-4 max-w-[85%] ${
                        msg.isUser 
                          ? "bg-purple-600 text-white" 
                          : "bg-white border border-slate-200 text-slate-800"
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{msg.text}</p>
                    </div>
                  </div>
                ))}
                {isFetching && (
                  <div className="flex justify-start">
                    <div className="bg-white border border-slate-200 rounded-lg p-4">
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-purple-600 rounded-full animate-pulse"></div>
                        <div className="w-2 h-2 bg-purple-600 rounded-full animate-pulse delay-75"></div>
                        <div className="w-2 h-2 bg-purple-600 rounded-full animate-pulse delay-150"></div>
                      </div>
                    </div>
                  </div>
                )}
                {/* This invisible div is used as a reference point for scrolling */}
                <div ref={messagesEndRef} />
              </div>
            </>
          )}
        </div>

        {/* Input area */}
        <div className="sticky bottom-0 pb-4">
          <div className="relative">
            <textarea
              className="w-full border border-slate-300 rounded-xl py-3 pl-4 pr-12 min-h-[56px] max-h-[200px] resize-none focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent"
              placeholder="Type your query..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendMessage();
                }
              }}
              rows={1}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isFetching}
              className={`absolute right-3 bottom-3 p-1 rounded-md ${
                input.trim() && !isFetching
                  ? "text-purple-600 hover:bg-purple-100"
                  : "text-slate-400"
              }`}
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;