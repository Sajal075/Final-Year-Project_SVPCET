"use client";

import { QRCodeSVG } from "qrcode.react";

interface QRCodeDisplayProps {
  value: string;
  size?: number;
  level?: "L" | "M" | "Q" | "H";
}

export default function QRCodeDisplay({
  value,
  size = 256,
  level = "H",
}: QRCodeDisplayProps) {
  return (
    <div className="flex justify-center p-4 bg-white rounded-lg">
      <QRCodeSVG value={value} size={size} level={level} />
    </div>
  );
}



