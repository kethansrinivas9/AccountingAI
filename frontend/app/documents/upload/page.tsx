"use client";

import { useState } from "react";
import Header from '../../header/page';

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [statusMessage, setStatusMessage] = useState<{ text: string; type: "success" | "error" } | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
      setStatusMessage(null); // Clear previous messages when selecting a new file
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setStatusMessage({ text: "Please select a file to upload.", type: "error" });
      return;
    }

    setUploading(true);
    setStatusMessage(null);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch('http://localhost:8080/documents/upload', {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        setStatusMessage({ text: "File uploaded successfully!", type: "success" });
        setSelectedFile(null);
      } else {
        setStatusMessage({ text: "Upload failed. Try again.", type: "error" });
      }
    } catch (error) {
      console.error("Upload error:", error);
      setStatusMessage({ text: "Something went wrong.", type: "error" });
    } finally {
      setUploading(false);
    }
  };

    return (
<div>
    <Header/>
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="bg-white shadow-lg rounded-xl p-6 w-full max-w-md">
        <h1 className="text-xl font-bold text-gray-800 mb-4">Upload a File</h1>

        <label className="flex flex-col items-center justify-center border-2 border-dashed border-gray-400 rounded-lg p-6 cursor-pointer hover:bg-gray-50 transition">
          <svg className="w-10 h-10 text-gray-500 mb-2" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          <span className="text-gray-600">{selectedFile ? selectedFile.name : "Click to select a file"}</span>
          <input type="file" onChange={handleFileChange} className="hidden" />
        </label>

        <button 
          className="w-full mt-4 bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400"
          onClick={handleUpload}
          disabled={!selectedFile || uploading}
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>

        {statusMessage && (
          <p className={`mt-4 text-sm text-center ${statusMessage.type === "success" ? "text-green-600" : "text-red-600"}`} >
            {statusMessage.text}
          </p>
        )}
      </div>
    </div>
</div>
  );
}
