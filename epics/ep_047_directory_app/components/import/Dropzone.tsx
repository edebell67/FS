"use client";

import { useCallback, useRef, useState } from "react";
import { UploadCloud } from "lucide-react";
import clsx from "clsx";

export interface DropzoneProps {
  onFileSelected: (file: File) => void;
  disabled?: boolean;
}

const ACCEPTED_EXTENSIONS = [".csv", ".json"];

function isAcceptedFile(file: File): boolean {
  const name = file.name.toLowerCase();
  return ACCEPTED_EXTENSIONS.some((ext) => name.endsWith(ext));
}

export function Dropzone({ onFileSelected, disabled }: DropzoneProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [rejectionMessage, setRejectionMessage] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFiles = useCallback(
    (files: FileList | null) => {
      const file = files?.[0];
      if (!file) return;

      if (!isAcceptedFile(file)) {
        setRejectionMessage(`"${file.name}" isn't a .csv or .json file.`);
        return;
      }

      setRejectionMessage(null);
      onFileSelected(file);
    },
    [onFileSelected]
  );

  return (
    <div>
      <div
        role="button"
        tabIndex={disabled ? -1 : 0}
        aria-disabled={disabled}
        onClick={() => !disabled && inputRef.current?.click()}
        onKeyDown={(e) => {
          if (!disabled && (e.key === "Enter" || e.key === " ")) inputRef.current?.click();
        }}
        onDragOver={(e) => {
          e.preventDefault();
          if (!disabled) setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={(e) => {
          e.preventDefault();
          setIsDragOver(false);
          if (!disabled) handleFiles(e.dataTransfer.files);
        }}
        className={clsx(
          "flex cursor-pointer flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed px-6 py-12 text-center transition-colors",
          disabled && "cursor-not-allowed opacity-50",
          isDragOver ? "border-brand-500 bg-brand-50" : "border-slate-300 hover:border-brand-400"
        )}
      >
        <UploadCloud className="h-10 w-10 text-brand-500" aria-hidden="true" />
        <div>
          <p className="font-medium text-slate-900">Drag & drop a CSV or JSON file here</p>
          <p className="text-sm text-slate-500">or click to browse</p>
        </div>
        <input
          ref={inputRef}
          type="file"
          accept=".csv,.json,text/csv,application/json"
          className="hidden"
          disabled={disabled}
          onChange={(e) => handleFiles(e.target.files)}
        />
      </div>
      {rejectionMessage && <p className="mt-2 text-sm text-red-600">{rejectionMessage}</p>}
    </div>
  );
}
