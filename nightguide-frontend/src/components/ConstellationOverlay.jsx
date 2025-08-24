import { useRef, useEffect } from 'react';

const ConstellationOverlay = ({ imageSrc, lines = [], points = [], constellation, description }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !imageSrc) return;

    const ctx = canvas.getContext('2d');
    const img = new Image();

    img.onload = () => {
      // Set canvas size to match image
      canvas.width = img.width;
      canvas.height = img.height;

      // Draw the background image
      ctx.drawImage(img, 0, 0);

      // Draw constellation lines
      ctx.strokeStyle = '#00ffff';
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 5]);

      lines.forEach(([x1, y1, x2, y2]) => {
        const startX = x1 * img.width;
        const startY = y1 * img.height;
        const endX = x2 * img.width;
        const endY = y2 * img.height;

        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(endX, endY);
        ctx.stroke();
      });

      // Draw star points
      points.forEach((point) => {
        const x = point.x * img.width;
        const y = point.y * img.height;

        // Draw star glow
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, 15);
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.8)');
        gradient.addColorStop(0.5, 'rgba(255, 255, 255, 0.3)');
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');

        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, 15, 0, 2 * Math.PI);
        ctx.fill();

        // Draw star center
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, 2 * Math.PI);
        ctx.fill();

        // Draw star name
        if (point.name) {
          ctx.fillStyle = '#ffffff';
          ctx.font = '12px Arial';
          ctx.textAlign = 'center';
          ctx.fillText(point.name, x, y - 20);
        }
      });
    };

    img.src = imageSrc;
  }, [imageSrc, lines, points]);

  if (!imageSrc) return null;

  return (
    <div className="relative">
      <canvas
        ref={canvasRef}
        className="max-w-full h-auto rounded-lg shadow-lg"
        style={{ maxHeight: '500px' }}
      />
      {constellation && (
        <div className="absolute top-4 left-4 bg-black bg-opacity-75 text-white p-3 rounded-lg">
          <h3 className="font-bold text-lg">{constellation}</h3>
          {description && <p className="text-sm opacity-90">{description}</p>}
        </div>
      )}
    </div>
  );
};

export default ConstellationOverlay; 